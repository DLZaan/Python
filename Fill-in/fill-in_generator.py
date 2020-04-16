# -*- coding: utf-8 -*-
"""
This script allows to procedurally generate fill-in crossword.

TO DO:
    - remove one-char fields with preservation of sparcity factor    
"""

import string
import random

def generate(height = 10, width = 10, seed = None, sparcity = 75, alphabet = string.ascii_uppercase, separator = "#", gap = "."):
    """Create crossword and return empty grid and list of words to put in
    :param height: number of rows in puzzle <1, 1000>
    :param width: number of columns in puzzle <1, 1000>
    :param seed: number used as seed in RNG
    :param sparcity: percentage of grid to fill with characters <1, 99>
    :param alphabet: string of characters used to generate crossword
    :param separator: character used as BLANK
    :param gap: character used to indicate space to fill
    :raise ValueError: if arguments have incorrect value
    :raise TypeError: if arguments have incorrect type
    :returns: {"puzzle": puzzle, "words": words} empty crossword and list of words needed to solve it
    """
    if not 1 <= height <= 1000:
        raise ValueError("Incorrect height")
    if not 1 <= width <= 1000:
        raise ValueError("Incorrect width")
    if not 1 <= sparcity < 100:
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
        
    random.seed(seed)    
    unique_alphabet = "".join(set(alphabet))

    crossword = [[unique_alphabet[random.randrange(len(unique_alphabet))] for j in range(width)] for i in range(height)]
    for stop in random.sample(range(0, height * width), (100 - sparcity)*(height * width)//100):
        crossword[stop//width][stop%width] = separator
        
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
        
    for i in range(height):
        for j in range(width):
            if separator != crossword[i][j]:
                crossword[i][j] = gap
    
    return {"puzzle": crossword, "words": words}
