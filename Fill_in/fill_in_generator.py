"""
This script allows to procedurally generate fill-in crosswords puzzles.

TO DO:
    - preserve sparsity factor when removing one-char fields (mainly for low sparsity)
"""

import random
import string


def generate_crossword(
    height: int = 10,
    width: int = 10,
    seed: int = None,
    sparsity: int = 75,
    alphabet: str = string.ascii_uppercase,
    separator: str = "#",
    gap: str = ".",
) -> dict:
    """Create crossword and return empty grid and list of words to put in.

    :param height: number of rows in puzzle <1, 1000>
    :param width: number of columns in puzzle <1, 1000>
    :param seed: number used as seed in RNG
    :param sparsity: percentage of grid to fill with characters (0, 100)
    :param alphabet: string of characters used to generate crossword
    :param separator: character used as BLANK
    :param gap: character used to indicate space to fill
    :raise ValueError: if arguments have incorrect value
    :raise TypeError: if arguments have incorrect type
    :returns: {"grid": grid, "words": words} empty crossword and list of words needed to solve it
    """
    if not 1 <= height <= 1000:
        raise ValueError("Incorrect height")
    if not 1 <= width <= 1000:
        raise ValueError("Incorrect width")
    if not 0 < sparsity < 100:
        raise ValueError("Incorrect sparsity")
    if not alphabet.isascii():
        raise TypeError("Alphabet has to be ASCII string")
    if separator in alphabet or gap in alphabet:
        raise TypeError("Alphabet cannot contain separator nor gap")
    if not (separator.isascii() and len(separator) == 1):
        raise TypeError("Separator has to be single character")
    if not (gap.isascii() and len(gap) == 1):
        raise TypeError("Gap has to be single character")
    if separator == gap:
        raise ValueError("Separator cannot be equal to gap character")

    grid = generate_grid(height, width, seed, sparsity, separator, gap)
    crossword = fill_crossword(grid, seed, alphabet, gap)
    words = extract_words(crossword, separator)
    return {"grid": grid, "words": words}


def generate_grid(
    height: int = 10,
    width: int = 10,
    seed: int = None,
    sparsity: int = 75,
    separator: str = "#",
    gap: str = ".",
) -> list[list[str]]:
    """Create empty grid as base for crossword.

    :param height: number of rows in puzzle <1, 1000>
    :param width: number of columns in puzzle <1, 1000>
    :param seed: number used as seed in RNG
    :param sparsity: percentage of grid to fill with characters (0, 100)
    :param separator: character used as BLANK
    :param gap: character used to indicate space to fill
    :raise ValueError: if arguments have incorrect value
    :raise TypeError: if arguments have incorrect type
    :returns: empty grid
    """
    if not 1 <= height <= 1000:
        raise ValueError("Incorrect height")
    if not 1 <= width <= 1000:
        raise ValueError("Incorrect width")
    if not 0 < sparsity < 100:
        raise ValueError("Incorrect sparsity")
    if not (separator.isascii() and len(separator) == 1):
        raise TypeError("Separator has to be single character")
    if not (gap.isascii() and len(gap) == 1):
        raise TypeError("Gap has to be single character")
    if separator == gap:
        raise ValueError("Separator cannot be equal to gap character")

    random.seed(seed)

    # generate
    grid = [[gap for _ in range(width)] for _ in range(height)]
    for stop in random.sample(
        range(0, height * width), (100 - sparsity) * height * width // 100
    ):
        grid[stop // width][stop % width] = separator

    # _check and eliminate solo gaps
    for i in range(height):
        for j in range(width):
            if (
                gap == grid[i][j]
                and (0 == i or separator == grid[i - 1][j])
                and (0 == j or separator == grid[i][j - 1])
                and (height == i + 1 or separator == grid[i + 1][j])
                and (width == j + 1 or separator == grid[i][j + 1])
            ):
                grid[i][j] = separator

    return grid


def fill_crossword(
    grid: list[list[str]],
    seed: int = None,
    alphabet: str = string.ascii_uppercase,
    gap: str = ".",
) -> list[list[str]]:
    """Replace gaps in grid with random character from alphabet.

    :param grid: list of lists of characters, base for crossword
    :param seed: number used as seed in RNG
    :param alphabet: string of characters used to generate crossword
    :param gap: character used to indicate space to fill
    :raise ValueError: if arguments have incorrect value
    :raise TypeError: if arguments have incorrect type
    :returns: filled crossword
    """
    if (type(grid) is not list) or (False in [type(row) is list for row in grid]):
        raise TypeError("Incorrect type of crossword")
    if not alphabet.isascii():
        raise TypeError("Alphabet has to be ASCII string")
    if gap in alphabet:
        raise TypeError("Alphabet cannot contain gap")
    if not (gap.isascii() and len(gap) == 1):
        raise TypeError("Gap has to be single character")

    random.seed(seed)

    crossword = [
        [(char if gap != char else random.choice(list(alphabet))) for char in row]
        for row in grid
    ]

    return crossword


def extract_words(crossword: list[list[str]], separator: str = "#"):
    """List words needed to solve the crossword.

    :param crossword: puzzle to extract words from
    :param separator: character used as BLANK
    :raise ValueError: if arguments have incorrect value
    :raise TypeError: if arguments have incorrect type
    :returns: list of words sorted from shortest to longest alphabetically
    """
    if not type(crossword) is list and all(type(row) is list for row in crossword):
        raise TypeError("Incorrect type of crossword")
    height = len(crossword)
    width = len(crossword[0])
    if any(len(row) != width for row in crossword):
        raise ValueError("Crossword is not matrix")
    if not (separator.isascii() and len(separator) == 1):
        raise TypeError("Separator has to be single character")

    words = []
    for i, row in enumerate(crossword):
        for j, cell in enumerate(row):
            if separator != cell:
                # vertical
                new_words = []
                if 0 == i or separator == crossword[i - 1][j]:
                    length = 1
                    while i + length < height and separator != crossword[i + length][j]:
                        length += 1
                    new_words.append([crossword[i + x][j] for x in range(length)])
                # horizontal
                if 0 == j or separator == row[j - 1]:
                    length = 1
                    while j + length < width and separator != row[j + length]:
                        length += 1
                    new_words.append(row[j : (j + length)])
                words += ["".join(word) for word in new_words if 1 < len(word)]

    words.sort(key=lambda word: (len(word), word))
    return words
