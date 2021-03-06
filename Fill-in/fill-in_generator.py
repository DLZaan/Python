# -*- coding: utf-8 -*-
"""
This script allows to procedurally generate fill-in crosswords puzzles.

TO DO:
    - remove one-char fields with preservation of sparcity factor    
"""

import string
import random

def generate_crossword(height = 10, width = 10, seed = None, sparcity = 75, alphabet = string.ascii_uppercase, separator = "#", gap = "."):
    """Create crossword and return empty grid and list of words to put in
    :param height: number of rows in puzzle <1, 1000>
    :param width: number of columns in puzzle <1, 1000>
    :param seed: number used as seed in RNG
    :param sparcity: percentage of grid to fill with characters (0, 100)
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
    if not 0 < sparcity < 100:
        raise ValueError("Incorrect sparcity")
    if not alphabet.isascii():
        raise TypeError("Alphabet has to be ASCII string")
    if separator in alphabet or gap in alphabet:
        raise TypeError("Alphabet cannot contain separator nor gap")
    if not (separator.isascii() and len(separator)==1):
        raise TypeError("Separator has to be single character")
    if not (gap.isascii() and len(gap)==1):
        raise TypeError("Gap has to be single character")
    if separator==gap:
        raise ValueError("Separator cannot be equal to gap character")
        
    grid = generate_grid(height, width, seed, sparcity, separator, gap)
    
    crossword = fill_crossword(grid, seed, alphabet, gap)
        
    words = extract_words(crossword, separator)
    
    return {"grid": grid, "words": words}

def generate_grid(height = 10, width = 10, seed = None, sparcity = 75, separator = "#", gap = "."):
    """Create empty grid as base for crossword
    :param height: number of rows in puzzle <1, 1000>
    :param width: number of columns in puzzle <1, 1000>
    :param seed: number used as seed in RNG
    :param sparcity: percentage of grid to fill with characters (0, 100)
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
    if not 0 < sparcity < 100:
        raise ValueError("Incorrect sparcity")
    if not (separator.isascii() and len(separator)==1):
        raise TypeError("Separator has to be single character")
    if not (gap.isascii() and len(gap)==1):
        raise TypeError("Gap has to be single character")
    if separator==gap:
        raise ValueError("Separator cannot be equal to gap character")
        
    random.seed(seed)    

    grid = [[gap for x in range(width)] for y in range(height)]
    for stop in random.sample(range(0, height * width), (100 - sparcity)*(height * width)//100):
        grid[stop//width][stop%width] = separator
    
    return grid

def fill_crossword(grid, seed = None, alphabet = string.ascii_uppercase, gap = "."):
    """Replace gaps in grid with random character from alphabet
    :param grid: list of list of characters, base for crossword
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
    if not (gap.isascii() and len(gap)==1):
        raise TypeError("Gap has to be single character")
        
    random.seed(seed)

    crossword = [[(char if gap != char else alphabet[random.randrange(len(alphabet))]) for char in row] for row in grid]
    
    return crossword

def extract_words(crossword, separator = "#"):
    """List words needed to colve the crossword
    :param crossword: puzzle to extract words from
    :param separator: character used as BLANK
    :raise ValueError: if arguments have incorrect value
    :raise TypeError: if arguments have incorrect type
    :returns: list of words serted from shortest to longest alphabetically
    """
    if (type(crossword) is not list) or (False in [type(row) is list for row in crossword]):
        raise TypeError("Incorrect type of crossword")
    height = len(crossword)
    width = len(crossword[0])
    if (False in [len(row) == width for row in crossword]):
        raise ValueError("Crossword is not matrix")
    if not (separator.isascii() and len(separator)==1):
        raise TypeError("Separator has to be single character")
    
    words = []
    for i in range(height):
        for j in range(width):
            #vertical
            if (0==i or separator==crossword[i-1][j]) and separator!=crossword[i][j]:
                length = 1
                while i + length < height and separator!=crossword[i+length][j]:
                    length+=1
                if 1 < length:
                    words.append("".join([crossword[i+x][j] for x in range(length)]))
            #horizontal
            if (0==j or separator==crossword[i][j-1]) and separator!=crossword[i][j]:
                length = 1
                while j + length < width and separator!=crossword[i][j+length]:
                    length+=1
                if 1 < length:
                    words.append("".join(crossword[i][j:(j+length)]))
                    
    words.sort(key = lambda word:(len(word),word))
    
    return words
