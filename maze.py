from collections import namedtuple
from enum import Enum
import random
from typing import List, NamedTuple, Optional


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
        self._grid: List[List[Cell]] = [[Cell.EMPTY for _ in range(num_columns)] for _ in range(num_rows)]
        self._randomly_fill(sparseness)
        self._grid[self.start.row][self.start.col] = Cell.START
        self._grid[self.goal.row][self.goal.col] = Cell.GOAL


    def _randomly_fill(self, sparseness: float) -> None:
        for r_ind in range(self.num_rows):
            for c_ind in range(self.num_columns):
                if random.uniform(0.0, 1.0) < sparseness:
                    self._grid[r_ind][c_ind] = Cell.BLOCKED

    def __str__(self) -> str:
        return "\n".join([
            "".join(row) for row in self._grid
        ])

    def is_accessible(self, ml: Optional[MazeLocation] = None, x: Optional[int] = None, y: Optional[int] = None) -> bool:
        assert (ml is not None) or (x and y)
        if ml is None:
            ml = MazeLocation(x, y)
        if ml.row >= 0 and ml.row < self.num_rows and ml.col >= 0 and ml.col < self.num_columns and self._grid[ml.row][ml.col] != Cell.BLOCKED:
            return True
        return False

    def successors(self, ml: MazeLocation) -> List[MazeLocation]:
        possibilities = [
            MazeLocation(ml.row - 1, ml.col),
            MazeLocation(ml.row + 1, ml.col),
            MazeLocation(ml.row, ml.col - 1),
            MazeLocation(ml.row, ml.col + 1),

        ]
        return [
            poss for poss in possibilities
            if self.is_accessible(ml=poss)
        ]

if __name__ == "__main__":
    m = Maze()
    print(m)
    print(m.successors(MazeLocation(0, 0)))
    print(m.successors(MazeLocation(9, 9)))
