from __future__ import annotations

import abc
import asyncio
import contextlib
import inspect
import logging
import warnings
from typing import Any, AsyncGenerator, Awaitable, Callable, Coroutine, Generic, Mapping, Optional, Tuple, Type, \
    TypeVar, Union

import aiowamp
from .abstract import ClientABC, InvocationABC

__all__ = ["Invocation",
           "ProcedureRunnerABC", "CoroRunner", "AsyncGenRunner",
           "get_fn_runner_cls", "get_obj_runner_cls",
           "get_runner_factory"]

log = logging.getLogger(__name__)

ClientT = TypeVar("ClientT", bound=ClientABC)


class Invocation(InvocationABC[ClientT], Generic[ClientT]):
    __slots__ = ("session",
                 "__client",
                 "__done", "__interrupt",
                 "__procedure", "__request_id",
                 "__args", "__kwargs", "__details")

    session: aiowamp.SessionABC
    """Session used to send messages."""

    __client: ClientT

    __done: bool
    __interrupt: Optional[aiowamp.Interrupt]

    __procedure: aiowamp.URI
    __request_id: int

    __args: Tuple[aiowamp.WAMPType, ...]
    __kwargs: aiowamp.WAMPDict
    __details: aiowamp.WAMPDict

    def __init__(self, session: aiowamp.SessionABC, client: ClientT, msg: aiowamp.msg.Invocation, *,
                 procedure: aiowamp.URI) -> None:
        """Create a new invocation instance.

        Normally you should not create these yourself, they don't actively listen
        for incoming messages. Instead, they rely on the `aiowamp.ClientABC` to
        receive and pass them.

        Args:
            session: WAMP Session to send messages in.
            msg: Invocation message that spawned the invocation.
            procedure: Registered procedure URI.
        """
        self.session = session
        self.__client = client

        self.__done = False
        self.__interrupt = None

        self.__procedure = procedure
        self.__request_id = msg.request_id

        self.__args = tuple(msg.args) if msg.args else ()
        self.__kwargs = msg.kwargs or {}
        self.__details = msg.details

    def __getitem__(self, key: Union[int, str]) -> aiowamp.WAMPType:
        try:
            return super().__getitem__(key)
        except LookupError as e:
            if isinstance(key, int):
                msg = f"expected {key + 1} arguments, got {len(self)}"
            else:
                msg = f"missing keyword argument {key!r}"

            aiowamp.set_invocation_error(e, aiowamp.InvocationError(
                aiowamp.uri.INVALID_ARGUMENT,
                msg,
                kwargs={"key": key},
            ))
            raise e from None

    @property
    def client(self) -> ClientT:
        return self.__client

    @property
    def request_id(self) -> int:
        return self.__request_id

    @property
    def registered_procedure(self) -> aiowamp.URI:
        return self.__procedure

    @property
    def args(self) -> Tuple[aiowamp.WAMPType, ...]:
        return self.__args

    @property
    def kwargs(self) -> aiowamp.WAMPDict:
        return self.__kwargs

    @property
    def details(self) -> aiowamp.WAMPDict:
        return self.__details

    @property
    def done(self) -> bool:
        return self.__done

    @property
    def interrupt(self) -> Optional[aiowamp.Interrupt]:
        return self.__interrupt

    def __assert_not_done(self) -> None:
        if self.__done:
            raise RuntimeError(f"{self}: already completed")

    def __mark_done(self) -> None:
        self.__assert_not_done()
        self.__done = True

    async def send_progress(self, *args: aiowamp.WAMPType,
                            kwargs: aiowamp.WAMPDict = None,
                            options: aiowamp.WAMPDict = None) -> None:
        self.__assert_not_done()

        if not self.may_send_progress:
            raise RuntimeError(f"{self}: caller is unwilling to receive progress")

        # must not send progress when interrupted.
        if self.__interrupt:
            raise self.__interrupt

        options = options or {}
        options["progress"] = True

        await self.session.send(aiowamp.msg.Yield(
            self.__request_id,
            options,
            list(args) or None,
            kwargs,
        ))

    async def send_result(self, *args: aiowamp.WAMPType,
                          kwargs: aiowamp.WAMPDict = None,
                          options: aiowamp.WAMPDict = None) -> None:
        self.__mark_done()

        if options:
            # make sure we're not accidentally sending a result with progress=True
            with contextlib.suppress(KeyError):
                del options["progress"]
        else:
            options = {}

        await self.session.send(aiowamp.msg.Yield(
            self.__request_id,
            options,
            list(args) or None,
            kwargs,
        ))

    async def send_error(self, error: str, *args: aiowamp.WAMPType,
                         kwargs: aiowamp.WAMPDict = None,
                         details: aiowamp.WAMPDict = None) -> None:
        self.__mark_done()

        await self.session.send(aiowamp.msg.Error(
            aiowamp.msg.Invocation.message_type,
            self.__request_id,
            details or {},
            aiowamp.URI.as_uri(error),
            list(args) or None,
            kwargs,
        ))

    async def _receive_interrupt(self, interrupt: aiowamp.Interrupt) -> None:
        self.__interrupt = interrupt

        # if the cancel mode is killnowait the caller won't accept a response.
        if interrupt.cancel_mode == aiowamp.CANCEL_KILL_NO_WAIT:
            self.__done = True


def get_return_values(result: aiowamp.InvocationHandlerResult) \
        -> Tuple[Tuple[aiowamp.WAMPType, ...], Optional[Mapping[str, aiowamp.WAMPType]]]:
    """Unpack the return value of a invocation handler.

    Handles types according to `aiowamp.InvocationHandlerResult`.

    Args:
        result: Invocation handler result to be unpacked.

    Returns:
        2-tuple containing the positional and keyword arguments.
    """
    if isinstance(result, aiowamp.InvocationResult):
        return result.args, result.kwargs or None

    if isinstance(result, tuple):
        return result, None

    if result is None:
        return (), None

    return (result,), None


class ProcedureRunnerABC(Awaitable[None], abc.ABC):
    """Wrapper for procedure code handling results, exceptions, and interrupts.

    Creating an instance of a procedure runner is akin to starting it.
    To wait for a runner to finish it can be awaited.
    """
    __slots__ = ("invocation",
                 "_loop",
                 "__task")

    invocation: aiowamp.InvocationABC
    """Current invocation."""

    _loop: asyncio.AbstractEventLoop

    __task: asyncio.Task

    def __init__(self, invocation: aiowamp.InvocationABC) -> None:
        """
        Args:
            invocation: Invocation
        """
        self.invocation = invocation

        self._loop = asyncio.get_running_loop()
        self.__task = self._loop.create_task(self._run())

    def __str__(self) -> str:
        return f"{type(self).__qualname__}({self.invocation})"

    def __await__(self):
        return self.__task.__await__()

    @abc.abstractmethod
    async def _run(self) -> None:
        ...

    @abc.abstractmethod
    async def interrupt(self, exc: aiowamp.Interrupt) -> None:
        log.debug("%s: received interrupt %r", self, exc)

        await self.invocation._receive_interrupt(exc)

    async def _send_exception(self, e: Exception) -> None:
        """Send an exception if the invocation isn't done already.

        The exception is converted to a WAMP error.

        Args:
            e: Exception to send.
        """
        if self.invocation.done:
            log.debug("%s: already done, not sending error: %r", self, e)
            return

        err = aiowamp.exception_to_invocation_error(e)
        log.debug("%s: sending error: %r", self, err)
        await self.invocation.send_error(err.uri, *err.args or (), kwargs=err.kwargs, details=err.details)

    async def _send_progress(self, result: aiowamp.InvocationHandlerResult) -> None:
        """Send a progress message if the invocation isn't already done.

        If the caller isn't willing to receive progress results, the result is
        ignored.

        Args:
            result: Handler result to send.
        """
        if self.invocation.done:
            log.debug("%s: already done, not sending progress: %r", self, result)
            return

        if not self.invocation.may_send_progress:
            log.debug("%s: caller is unwilling to receive progress, discarding: %r", self, result)
            return

        log.debug("%s: sending progress: %r", self, result)
        args, kwargs = get_return_values(result)
        await self.invocation.send_progress(*args, kwargs=kwargs)

    async def _send_result(self, result: aiowamp.InvocationHandlerResult) -> None:
        """Send a result if the invocation isn't already done.

        Args:
            result: Handler result to send.
        """
        if self.invocation.done:
            log.debug("%s: already done, not sending result: %r", self, result)
            return

        log.debug("%s: sending result: %r", self, result)
        args, kwargs = get_return_values(result)
        await self.invocation.send_result(*args, kwargs=kwargs)


class CoroRunner(ProcedureRunnerABC):
    __slots__ = ("_coro", "_coro_task",
                 "_interrupt_fut", "_finish_fut")

    _coro: Coroutine
    _coro_task: asyncio.Task

    _interrupt_fut: asyncio.Future
    _finish_fut: asyncio.Future

    def __init__(self, invocation: aiowamp.InvocationABC, coro: Coroutine) -> None:
        super().__init__(invocation)

        self._coro = coro
        self._coro_task = self._loop.create_task(coro)

        self._interrupt_fut = self._loop.create_future()
        self._finish_fut = self._loop.create_future()

    async def __handle_interrupt(self, interrupt: aiowamp.Interrupt) -> None:
        if self._coro_task.done():
            log.debug("%s: already done, no point in interrupting", self)
            return

        self._coro_task.cancel()

        try:
            result = await self._coro.throw(type(interrupt), interrupt)
        except StopIteration as e:
            coro = self._send_result(e.value)
        except Exception as e:
            coro = self._send_exception(e)
        else:
            coro = self._send_result(result)

        await coro
        self._finish_fut.set_result(None)

    async def __handle_finish(self) -> None:
        log.debug("%s: finished", self)

        try:
            result = await self._coro_task
        except Exception as e:
            await self._send_exception(e)
        else:
            await self._send_result(result)

        self._finish_fut.set_result(None)

    async def _run(self) -> None:
        interrupted = False

        def on_interrupt(fut: asyncio.Future) -> None:
            nonlocal interrupted

            interrupted = True
            self._loop.create_task(self.__handle_interrupt(fut.result()))

        self._interrupt_fut.add_done_callback(on_interrupt)

        def on_finish(fut: asyncio.Future) -> None:
            if interrupted:
                # this is just a RuntimeError because we're awaiting an already
                # awaited coroutine.
                fut.exception()
                return

            self._interrupt_fut.remove_done_callback(on_interrupt)
            self._loop.create_task(self.__handle_finish())

        self._coro_task.add_done_callback(on_finish)

        await self._finish_fut

    async def interrupt(self, exc: aiowamp.Interrupt) -> None:
        await super().interrupt(exc)

        self._interrupt_fut.set_result(exc)


class AsyncGenRunner(ProcedureRunnerABC):
    __slots__ = ("agen",
                 "has_pending", "pending_prog",
                 "_interrupt")

    agen: AsyncGenerator

    has_pending: bool
    pending_prog: aiowamp.InvocationHandlerResult

    _interrupt: Optional[aiowamp.Interrupt]

    def __init__(self, invocation: aiowamp.InvocationABC, agen: AsyncGenerator) -> None:
        super().__init__(invocation)
        self.agen = agen

        self.has_pending = False
        # pending_prog is only set when has_pending is True, the potential
        # AttributeError is deliberate.

        self._interrupt = None

    def __repr__(self) -> str:
        return f"{type(self).__qualname__}({self.invocation!r}, {self.agen!r})"

    def __str__(self) -> str:
        return f"{type(self).__qualname__}({self.invocation})"

    def __clear_pending(self) -> None:
        self.has_pending = False
        del self.pending_prog

    async def __handle_yield(self, prog: aiowamp.InvocationHandlerResult) -> None:
        log.debug("%s: handling yield: %r", self, prog)

        if self.has_pending:
            await self._send_progress(self.pending_prog)
            self.__clear_pending()

        if isinstance(prog, aiowamp.InvocationProgress):
            # send immediately
            await self._send_progress(prog)
        elif isinstance(prog, aiowamp.InvocationResult):
            await self._send_result(prog)
        else:
            self.pending_prog = prog
            self.has_pending = True

    async def __handle_finish(self) -> None:
        log.debug("%s: handling finish", self)

        if self.has_pending:
            await self._send_result(self.pending_prog)
            self.__clear_pending()
            return

        if self.invocation.done:
            return

        warnings.warn("returned no final result, sending an empty an empty result.\n"
                      "Final yield MUST NOT be an instance of aiowamp.InvocationProgress!",
                      SyntaxWarning)
        await self.invocation.send_result()

    async def _run(self) -> None:
        try:
            async for handler_result in self.agen:
                if self._interrupt is None:
                    await self.__handle_yield(handler_result)
                    continue

                handler_result = await self.agen.athrow(type(self._interrupt), self._interrupt)
                await self._send_result(handler_result)
        except Exception as e:
            await self._send_exception(e)
        else:
            await self.__handle_finish()

    async def interrupt(self, exc: aiowamp.Interrupt) -> None:
        await super().interrupt(exc)
        self._interrupt = exc


class AwaitableRunner(ProcedureRunnerABC):
    __slots__ = ("_awaitable",)

    _awaitable: Awaitable

    def __init__(self, invocation: aiowamp.InvocationABC, awaitable: Awaitable) -> None:
        super().__init__(invocation)
        self._awaitable = awaitable

    async def _run(self) -> None:
        try:
            result = await self._awaitable
        except (asyncio.CancelledError, Exception) as e:
            await self._send_exception(e)
        else:
            await self._send_result(result)

    async def interrupt(self, exc: aiowamp.Interrupt) -> None:
        await super().interrupt(exc)

        if isinstance(self._awaitable, asyncio.Future):
            self._awaitable.cancel()


RunnerFactory = Callable[[InvocationABC], ProcedureRunnerABC]


def get_fn_runner_cls(handler: aiowamp.InvocationHandler) -> Optional[Type[ProcedureRunnerABC]]:
    if inspect.iscoroutinefunction(handler):
        return CoroRunner

    if inspect.isasyncgenfunction(handler):
        return AsyncGenRunner

    return None


def get_obj_runner_cls(value: Any) -> Type[ProcedureRunnerABC]:
    if inspect.iscoroutine(value):
        return CoroRunner

    if inspect.isasyncgen(value):
        return AsyncGenRunner

    if inspect.isawaitable(value):
        return AwaitableRunner

    raise TypeError(f"unsupported type: {type(value).__qualname__}.\n"
                    "Function must return a coroutine, async generator, or awaitable object.")


def make_lazy_factory(handler: aiowamp.InvocationHandler) -> RunnerFactory:
    def factory(invocation: InvocationABC):
        # TODO should this really bubble to the client level?
        res = handler(invocation)
        cls = get_obj_runner_cls(res)

        # TODO treat res on typeerror as result, maybe simply return this and
        #  let the caller handle it

        return cls(invocation, res)

    return factory


def get_runner_factory(handler: aiowamp.InvocationHandler) -> RunnerFactory:
    cls = get_fn_runner_cls(handler)
    if cls:
        return lambda i: cls(i, handler(i))

    return make_lazy_factory(handler)
