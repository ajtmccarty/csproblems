from collections import deque
from heapq import heappush, heappop
from typing import Any, Callable, Deque, Generic, List, Optional, Union


StackOrQueue: Union["Stack", "Queue"]


class Staque:
    def __init__(self) -> None:
        self._container: List = []

    @property
    def is_empty(self) -> bool:
        return len(self._container) == 0

    def __repr__(self) -> str:
        return repr(self._container)

    def push(self, item: Any) -> None:
        raise NotImplementedError

    def pop(self) -> Any:
        raise NotImplementedError


class Stack(Staque):
    def pop(self) -> Any:
        return self._container.pop()

    def __repr__(self) -> str:
        return repr(self._container)


class Queue(Staque):
    def __init__(self) -> None:
        self._container: Deque = Deque()

    def push(self, item: Any) -> None:
        self._container.append(item)

    def pop(self) -> Any:
        return self._container.popleft()


class PriorityQueue(Staque):
    def push(self, item: Any) -> None:
        heappush(self._container, item)

    def pop(self) -> Any:
        heappop(self._container)


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


def dfs(initial: Any, goal_test: Callable, successors: Callable) -> Optional[Node]:
    return xfs(initial, goal_test, successors, breadth_first=False)


def bfs(initial: Any, goal_test: Callable, successors: Callable) -> Optional[Node]:
    return xfs(initial, goal_test, successors, breadth_first=True)


def xfs(
    initial: Any, goal_test: Callable, successors: Callable, breadth_first: bool = True
) -> Optional[Node]:
    if breadth_first:
        frontier: StackOrQueue = Queue()
    else:
        frontier: StackOrQueue = Stack()
    frontier.push(Node(state=initial, parent=None))
    explored: set = set(initial)

    while not frontier.is_empty:
        current_node: Node = frontier.pop()
        current_state = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(state=child, parent=current_node))
    return None


def node_to_path(node: Node) -> List:
    if not node:
        return []
    path: List = [node.state]
    parent: Node = node.parent
    while parent:
        path.append(parent.state)
        parent = parent.parent
    path.reverse()
    return path
