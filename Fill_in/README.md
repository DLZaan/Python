# Fill-in generator
This simple script allows to procedurally generate [Fill-In](https://en.wikipedia.org/wiki/Fill-In_(puzzle)) crosswords puzzles.

Example usage:
```python
>>> crossword = generate_crossword(height=5, width=5, seed=123456789)
>>> print("\n".join(["".join(row) for row in crossword["grid"]]))
.....
....#
..#.#
..#.#
#....
>>> print(crossword["words"])
['LZ', 'OM', 'RJ', 'ORWG', 'TMJW', 'UTOL', 'OMMZO', 'UORWZ', 'WWRMW']
```
# Fill-in solver
Example usage:
```python
>>> from fill_in_solver import BacktrackingSolver
>>> solver = BacktrackingSolver()
>>>with open(f"puzzle.txt") as puzzle:
>>>    print(crossword:= [list(line.strip()) for line in puzzle.readlines()])
[['.', '.', '.'], ['.', '.', '#'], ['.', '.', '.']]
>>> with open(f"word_list.txt") as word_list:
>>>    print(words:= [word.strip() for word in word_list.readlines()])
['bd', 'abc', 'bde', 'abc', 'ceg']
>>>solver.solve(crossword, words)
abc
bdf
ceg
```