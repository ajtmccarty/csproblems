from typing import Any, Generic, List, Optional


class Stack:
    def __init__(self) -> None:
        self._container: List = []

    @property
    def is_empty(self) -> bool:
        return bool(self._container)

    def push(self, item: Any) -> None:
        self._container.append(item)

    def pop(self) -> Any:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


class Node:
    def __init__(
        self,
        state: Any,
        parent: Optional["Node"],
        cost: float = 0.0,
        heuristic: float = 0.0,
    ) -> None:
        self.state: Any = state
        self.parent: Optional["Node"] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic

    def __lt__(self, other: "Node") -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)
