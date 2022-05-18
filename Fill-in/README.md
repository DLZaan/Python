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