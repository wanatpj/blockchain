from abc import abstractmethod
from typing import Generic, Optional, TypeVar


POLICY_SUBJECT = TypeVar("POLICY_SUBJECT")
HINT = TypeVar("HINT")


class Policy(Generic[POLICY_SUBJECT, HINT]):
    @abstractmethod
    def validate(self, subject: POLICY_SUBJECT, hint: Optional[HINT] = None) -> None:
        ...
