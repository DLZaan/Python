"""
Classes for solving fill-in crosswords puzzles.
"""

import re
from abc import ABC, abstractmethod
from copy import deepcopy


class _Gap:
    def __init__(self, row: int, column: int, length: int, vertical: bool):
        self.row = row
        self.column = column
        self.length = length
        self.vertical = vertical

    def get_gap(self, grid: list[list]) -> []:
        return (
            (grid[self.row + i][self.column] for i in range(self.length))
            if self.vertical
            else grid[self.row][self.column : (self.column + self.length)]
        )

    def fill_gap(self, grid: list[list[str]], word: str) -> None:
        if self.vertical:
            for i in range(self.length):
                grid[self.row + i][self.column] = word[i]
        else:
            for i in range(self.length):
                grid[self.row][self.column + i] = word[i]


class AbstractSolver(ABC):
    def __init__(self, separator: str = "#"):
        self.separator = separator

    @abstractmethod
    def solve(self, crossword: list[list[str]], words: [str]) -> list[list[str]]:
        pass


class BacktrackingSolver(AbstractSolver):
    def solve(self, crossword: list[list[str]], words: [str]) -> list[list[str]]:
        grid = deepcopy(crossword)

        gaps = []
        height = len(grid)
        width = len(grid[0])
        for i, row in enumerate(grid):
            for j, cell in enumerate(row):
                if self.separator != cell:
                    # vertical
                    if 0 == i or self.separator == grid[i - 1][j]:
                        length = 1
                        while (
                            i + length < height
                            and self.separator != grid[i + length][j]
                        ):
                            length += 1
                        gaps.append(_Gap(i, j, length, True))
                    # horizontal
                    if 0 == j or self.separator == row[j - 1]:
                        length = 1
                        while j + length < width and self.separator != row[j + length]:
                            length += 1
                        gaps.append(_Gap(i, j, length, False))

        gaps = list(filter(lambda gap: 1 < gap.length, gaps))

        words_dict = {}
        for word in words:
            words_dict[len(word)] = words_dict.get(len(word), []) + [
                {"word": word, "used": False}
            ]

        if self._check(grid, words_dict, gaps):
            print("\n".join(["".join(row) for row in grid]))
            return grid

    def _check(
        self,
        crossword: list[list[str]],
        words_dict: dict[int, list[dict]],
        gaps: [_Gap],
    ):
        if not gaps:
            return True
        gap = gaps[0]
        missing = "".join(gap.get_gap(crossword))
        for pos in filter(
            lambda word: (not word["used"]) and re.match(missing, word["word"]),
            words_dict[gap.length],
        ):
            pos["used"] = True
            gap.fill_gap(crossword, pos["word"])
            if self._check(crossword, words_dict, gaps[1:]):
                return True
            gap.fill_gap(crossword, missing)
            pos["used"] = False
        return False
