from abc import ABC, abstractmethod
from typing import Generic, Optional, TypeVar


POLICY_SUBJECT = TypeVar("POLICY_SUBJECT")
HINT = TypeVar("HINT")


class Policy(Generic[POLICY_SUBJECT, HINT], ABC):
    @abstractmethod
    def validate(self, subject: POLICY_SUBJECT, hint: Optional[HINT] = None) -> None:
        ...

    def type(self) -> str:
        return self.__class__.__qualname__
