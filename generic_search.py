from collections import deque
from heapq import heappush, heappop
from typing import Any, Callable, Deque, Dict, Generic, List, Optional, Union


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

    def push(self, item: Any) -> None:
        return self._container.append(item)


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
        return heappop(self._container)


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

    def __repr__(self) -> str:
        return f"Node state: {self.state}"

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
        frontier: Staque = Queue()
    else:
        frontier: Staque = Stack()
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


def astar(
    initial, goal_test: Callable, successors: Callable, heuristic: Callable
) -> Optional[Node]:
    frontier: Staque = PriorityQueue()
    frontier.push(
        Node(state=initial, parent=None, cost=0.0, heuristic=heuristic(initial))
    )
    explored: Dict = {initial: 0.0}

    while not frontier.is_empty:
        current_node: Node = frontier.pop()
        current_state = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            new_cost: float = current_node.cost + 1  # assume cost of 1
            if child not in explored or new_cost < explored[child]:
                explored[child] = new_cost
                frontier.push(
                    Node(
                        state=child,
                        parent=current_node,
                        cost=new_cost,
                        heuristic=heuristic(child),
                    )
                )
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
