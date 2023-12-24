from collections import defaultdict
from types import TracebackType
from typing import Optional

from blockchain.policy.core import Policy
from blockchain.struct.trade import Trade


class AllocationError(Exception):
    pass


class Allocation:
    def __init__(self, summary_policy: Optional[Policy] = None):
        self._raw_allocation = defaultdict(lambda: 0)
        self._raw_allocation_safe_copy = None
        self._summary_policy = summary_policy

    def __enter__(self):
        self._raw_allocation_safe_copy = self._raw_allocation.copy()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ):
        if exc_type is None:
            self._raw_allocation_safe_copy = None
            return
        self._raw_allocation = self._raw_allocation_safe_copy
        self._raw_allocation_safe_copy = None

    def reduce(self, trade: Trade):
        if self._raw_allocation_safe_copy is None:
            raise AllocationError("reduce out of allocation context")
        self._raw_allocation[trade.src] -= trade.value
        self._raw_allocation[trade.dst] += trade.value
        if self._summary_policy:
            self._summary_policy.validate(self, hint=trade)

    def as_dict(self):
        return self._raw_allocation.copy()
