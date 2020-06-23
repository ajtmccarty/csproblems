from typing import Any, Generic, List


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
