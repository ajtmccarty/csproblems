from collections import namedtuple
from enum import Enum
from math import sqrt
import random
from typing import Callable, List, NamedTuple, Optional

from generic_search import dfs, bfs, node_to_path


class Cell(str, Enum):
    BLOCKED = "X"
    EMPTY = " "
    GOAL = "G"
    PATH = "*"
    START = "S"


class MazeLocation(NamedTuple):
    row: int
    col: int


class Maze:
    def __init__(
        self,
        num_rows: int = 10,
        num_columns: int = 10,
        start: MazeLocation = MazeLocation(0, 0),
        goal: Optional[MazeLocation] = None,
        sparseness: float = 0.2,
    ) -> None:
        if goal is None:
            goal = MazeLocation(num_rows - 1, num_columns - 1)
        self.num_rows: int = num_rows
        self.num_columns: int = num_columns
        self.start: MazeLocation = start
        self.goal: MazeLocation = goal
        self._grid: List[List[Cell]] = [
            [Cell.EMPTY for _ in range(num_columns)] for _ in range(num_rows)
        ]
        self._randomly_fill(sparseness)
        self._grid[self.start.row][self.start.col] = Cell.START
        self._grid[self.goal.row][self.goal.col] = Cell.GOAL

    def _randomly_fill(self, sparseness: float) -> None:
        for r_ind in range(self.num_rows):
            for c_ind in range(self.num_columns):
                if random.uniform(0.0, 1.0) < sparseness:
                    self._grid[r_ind][c_ind] = Cell.BLOCKED

    def __str__(self) -> str:
        return "\n".join(["".join(row) for row in self._grid])

    def is_accessible(
        self,
        ml: Optional[MazeLocation] = None,
        x: Optional[int] = None,
        y: Optional[int] = None,
    ) -> bool:
        assert (ml is not None) or (x and y)
        if ml is None:
            ml = MazeLocation(x, y)
        if (
            ml.row >= 0
            and ml.row < self.num_rows
            and ml.col >= 0
            and ml.col < self.num_columns
            and self._grid[ml.row][ml.col] != Cell.BLOCKED
        ):
            return True
        return False

    def is_goal(self, ml: MazeLocation) -> bool:
        return self._grid[ml.row][ml.col] == Cell.GOAL

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        possibilities = {
            MazeLocation(ml.row - 1, ml.col),
            MazeLocation(ml.row + 1, ml.col),
            MazeLocation(ml.row, ml.col - 1),
            MazeLocation(ml.row, ml.col + 1),
        }
        return [poss for poss in possibilities if self.is_accessible(ml=poss)]

    def mark(self, path: List[MazeLocation]):
        for ml in path:
            if ml not in (self.start, self.goal):
                self._grid[ml.row][ml.col] = Cell.PATH

    def clear(self):
        for r_ind in range(self.num_rows):
            for c_ind in range(self.num_columns):
                if self._grid[r_ind][c_ind] == Cell.PATH:
                    self._grid[r_ind][c_ind] = Cell.EMPTY


def euclidean_distance(goal: MazeLocation) -> Callable[[MazeLocation], float]:
    def distance(ml: MazeLocation) -> float:
        xdist: int = ml.col - goal.col
        ydist: int = ml.row - goal.row
        return sqrt(xdist ** 2 + ydist ** 2)

    return distance


if __name__ == "__main__":
    m = Maze(num_rows=7, num_columns=10, sparseness=0.3)

    print("Depth first search solution")
    node = dfs(initial=m.start, goal_test=m.is_goal, successors=m.successors)
    path = node_to_path(node)
    if path:
        m.mark(path)
        print(m)
    else:
        print(m)
        print("Unsolvable")

    m.clear()
    print("Breadth first search solution")
    node = bfs(initial=m.start, goal_test=m.is_goal, successors=m.successors)
    path = node_to_path(node)
    if path:
        m.mark(path)
        print(m)
    else:
        print(m)
        print("Unsolvable")
