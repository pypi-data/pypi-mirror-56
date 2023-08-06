from typing import NewType, Optional, Tuple, Type, TypeVar

__all__ = ["MatchPolicy", "MATCH_PREFIX", "MATCH_WILDCARD",
           "URI"]

MatchPolicy = NewType("MatchPolicy", str)
"""Match policy for URIs."""

MATCH_PREFIX = MatchPolicy("prefix")
MATCH_WILDCARD = MatchPolicy("wildcard")

T = TypeVar("T")


class URI(str):
    """WAMP URI.

    A `URI` is a subclass of `str` and can be used wherever a string would be
    expected. Apart from object identity (`id`) URIs are also completely equal
    to their string equivalent (ex: "hash(aiowamp.URI('a')) == hash('a')).

    The benefit of URIs (apart from the semantics) is that they can carry a
    `MatchPolicy` with them.
    All functions that accept a "match_policy" keyword argument will also check
    for the `.match_policy` (Note that the keyword argument will always be used
    if specified).
    """
    __slots__ = ("match_policy",)

    match_policy: Optional[MatchPolicy]

    def __new__(cls: Type[T], uri: str, *,
                match_policy: MatchPolicy = None) -> T:
        self = super().__new__(cls, uri)
        self.match_policy = match_policy
        return self

    @classmethod
    def as_uri(cls: Type[T], uri: str) -> T:
        if isinstance(uri, cls):
            return uri

        return cls(uri)

    def __repr__(self) -> str:
        if self.match_policy is not None:
            match_str = f", match_policy={self.match_policy!r}"
        else:
            match_str = ""

        return f"URI({str(self)!r}{match_str})"

    def split_components(self) -> Tuple[str]:
        return tuple(self.split("."))

    @classmethod
    def policy_match(cls, policy: MatchPolicy, uri: str, other: str) -> bool:
        if policy is None:
            return uri == other
        elif policy == MATCH_WILDCARD:
            return cls.wildcard_match(other, uri)
        elif policy == MATCH_PREFIX:
            return cls.prefix_match(other, uri)
        else:
            raise ValueError(f"unknown match policy: {policy!r}")

    @staticmethod
    def prefix_match(uri: str, prefix: str) -> bool:
        """Check whether the URI matches the prefix.

        Args:
            uri: URI to be checked.
            prefix: Prefix to check against.

        Returns:
            Whether the URI has the given prefix.
        """
        if not uri.startswith(prefix):
            return False

        try:
            next_char = uri[len(prefix)]
        except IndexError:
            return True

        return next_char == "."

    @staticmethod
    def wildcard_match(uri: str, wildcard: str) -> bool:
        """Check if the URI matches the wildcard.

        Wildcards have empty URI components which can match anything
        (apart from '.').

        Args:
            uri: URI to be checked.
            wildcard: Wildcard to check against.

        Returns:
            Whether the URI matches the wildcard.
        """
        parts = uri.split(".")
        wc_parts = wildcard.split(".")

        if len(parts) != len(wc_parts):
            return False

        for part, wc_part in zip(parts, wc_parts):
            if wc_part and wc_part != part:
                return False

        return True


# Interaction

INVALID_URI = URI("wamp.error.invalid_uri")
"""
Peer provided an incorrect URI for any URI-based attribute of WAMP message, 
such as realm, topic or procedure.
"""

NO_SUCH_PROCEDURE = URI("wamp.error.no_such_procedure")
"""
A Dealer could not perform a call, since no procedure is currently registered 
under the given URI.
"""

PROCEDURE_ALREADY_EXISTS = URI("wamp.error.procedure_already_exists")
"""
A procedure could not be registered, since a procedure with the given URI is 
already registered.
"""

NO_SUCH_REGISTRATION = URI("wamp.error.no_such_registration")
"""
A Dealer could not perform an unregister, since the given registration is not 
active.
"""

NO_SUCH_SUBSCRIPTION = URI("wamp.error.no_such_subscription")
"""
A Broker could not perform an unsubscribe, since the given subscription is not 
active.
"""

INVALID_ARGUMENT = URI("wamp.error.invalid_argument")
"""
A call failed since the given argument types or values are not acceptable to 
the called procedure. In this case the Callee may throw this error. 
Alternatively a Router may throw this error if it performed payload validation 
of a call, call result, call error or publish, and the payload did not conform 
to the requirements.
"""

RUNTIME_ERROR = URI("wamp.error.runtime_error")
"""
THIS ISN'T PART OF THE WAMP PROTOCOL.
"""

# Session Close


CLOSE_NORMAL = URI("wamp.close.normal")
"""Normal close."""

SYSTEM_SHUTDOWN = URI("wamp.close.system_shutdown")
"""The Peer is shutting down completely.
Used as a GOODBYE (or ABORT) reason.
"""

CLOSE_REALM = URI("wamp.close.close_realm")
"""The Peer wants to leave the realm - used as a GOODBYE reason."""

GOODBYE_AND_OUT = URI("wamp.close.goodbye_and_out")
"""A Peer acknowledges ending of a session - used as a GOODBYE reply reason."""

PROTOCOL_VIOLATION = URI("wamp.error.protocol_violation")
"""A Peer received invalid WAMP protocol message.
(e.g. HELLO message after session was already established) - 
used as a ABORT reply reason.
"""

# Authorization

NOT_AUTHORIZED = URI("wamp.error.not_authorized")
"""
A join, call, register, publish or subscribe failed, since the Peer is not 
authorized to perform the operation.
"""

AUTHORIZATION_FAILED = URI("wamp.error.authorization_failed")
"""
A Dealer or Broker could not determine if the Peer is authorized to perform a 
join, call, register, publish or subscribe, since the authorization operation 
itself failed. E.g. a custom authorizer did run into an error.
"""

NO_SUCH_REALM = URI("wamp.error.no_such_realm")
"""Peer wanted to join a non-existing realm.
(and the Router did not allow to auto-create the realm).
"""

NO_SUCH_ROLE = URI("wamp.error.no_such_role")
"""
A Peer was to be authenticated under a Role that does not (or no longer) exists 
on the Router. 

For example, the Peer was successfully authenticated, but the Role configured 
does not exists - hence there is some misconfiguration in the Router.
"""

# Advanced Profile

CANCELLED = URI("wamp.error.canceled")
"""A Dealer or Callee canceled a call previously issued."""

OPTION_NOT_ALLOWED = URI("wamp.error.option_not_allowed")
"""
A Peer requested an interaction with an option that was disallowed by the 
Router.
"""

NO_ELIGIBLE_CALLEE = URI("wamp.error.no_eligible_callee")
"""
A Dealer could not perform a call, since a procedure with the given URI is 
registered, but Callee Black- and Whitelisting and/or Caller Exclusion lead to 
the exclusion of (any) Callee providing the procedure.
"""

OPTION_DISALLOWED_DISCLOSE_ME = URI("wamp.error.option_disallowed.disclose_me")
"""A Router rejected client request to disclose its identity."""

NETWORK_FAILURE = URI("wamp.error.network_failure")
"""A Router encountered a network failure."""
