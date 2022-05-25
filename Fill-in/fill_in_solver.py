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

    def get_gap(self, grid: list[list]) -> [str]:
        return (
            (grid[self.row + i][self.column] for i in range(self.length))
            if self.vertical
            else grid[self.row][self.column : self.column + self.length]
        )

    def fill_gap(self, grid: list[list[str]], word: str) -> None:
        if self.vertical:
            for i in range(self.length):
                grid[self.row + i][self.column] = word[i]
        else:
            grid[self.row][self.column : self.column + self.length] = list(word)


class AbstractSolver(ABC):
    def __init__(self, separator: str = "#"):
        self.separator = separator

    @abstractmethod
    def solve(self, crossword: list[list[str]], words: [str]) -> list[list[str]]:
        pass

    def get_gaps(self, crossword: list[list[str]]) -> list[_Gap]:
        gaps = []
        height = len(crossword)
        width = len(crossword[0])
        for i, row in enumerate(crossword):
            for j, cell in enumerate(row):
                if self.separator == cell:
                    continue
                # vertical
                if 0 == i or self.separator == crossword[i - 1][j]:
                    length = 1
                    while (
                        i + length < height
                        and self.separator != crossword[i + length][j]
                    ):
                        length += 1
                    gaps.append(_Gap(i, j, length, True))
                # horizontal
                if 0 == j or self.separator == row[j - 1]:
                    length = 1
                    while j + length < width and self.separator != row[j + length]:
                        length += 1
                    gaps.append(_Gap(i, j, length, False))
        return list(filter(lambda gap: 1 < gap.length, gaps))


class BacktrackingSolver(AbstractSolver):
    """Basic solver, processes gaps row by row, starting from upper left corner"""
    @staticmethod
    def group_words(words):
        words_dict = {}
        for word in words:
            words_dict[len(word)] = words_dict.get(len(word), []) + [
                {"word": word, "used": False}
            ]
        return words_dict

    def solve(self, crossword: list[list[str]], words: [str]) -> list[list[str]]:
        grid = deepcopy(crossword)
        if self._check(grid, self.group_words(words), self.get_gaps(grid)):
            return grid

    def _check(
        self,
        crossword: list[list[str]],
        words_dict: dict[int, list[dict]],
        gaps: [_Gap],
    ) -> bool:
        if not gaps:
            return True
        gap = gaps[0]
        missing = "".join(gap.get_gap(crossword))
        for option in filter(
            lambda word: (not word["used"]) and re.match(missing, word["word"]),
            words_dict[gap.length],
        ):
            option["used"] = True
            gap.fill_gap(crossword, option["word"])
            if self._check(crossword, words_dict, gaps[1:]):
                return True
            gap.fill_gap(crossword, missing)
            option["used"] = False
        return False


class BacktrackingDiagonalSolver(BacktrackingSolver):
    """Processes gaps diagonally, starting from upper left corner"""
    def solve(self, crossword: list[list[str]], words: [str]) -> list[list[str]]:
        grid = deepcopy(crossword)
        gaps = sorted(self.get_gaps(grid), key=lambda gap: gap.row + gap.column)
        if self._check(grid, self.group_words(words), gaps):
            return grid


class BacktrackingByLengthSolver(BacktrackingSolver):
    """Processes gaps starting from longest"""
    def solve(self, crossword: list[list[str]], words: [str]) -> list[list[str]]:
        grid = deepcopy(crossword)
        gaps_by_length = {}
        for gap in self.get_gaps(grid):
            gaps_by_length[gap.length] = gaps_by_length.get(gap.length, []) + [gap]
        gaps = []
        for length in sorted(gaps_by_length, reverse=True):
            if 1 == len(gaps_by_length[length]):
                gaps = gaps_by_length[length] + gaps
            else:
                gaps += gaps_by_length[length]
        if self._check(grid, self.group_words(words), gaps):
            return grid
