"""
This script runs solver tests (with benchmarking)
"""
import cProfile

import fill_in_solver


def main():
    tests = []
    for i in range(4):
        with open(f"tests/puzzle{i}.txt") as puzzle, open(
            f"tests/words{i}.txt"
        ) as words:
            tests.append(
                {
                    "crossword": [list(line.strip()) for line in puzzle.readlines()],
                    "words": [word.strip() for word in words.readlines()],
                }
            )

    backtracking = fill_in_solver.BacktrackingSolver()

    for i, test in enumerate(tests):
        crossword = test["crossword"]
        words = test["words"]
        print(f"TEST {i}")
        print(f"Crossword size = {len(crossword)}x{len(crossword[0])}")
        print(f"Words to fill = {len(words)}")
        print(f"Backtracking solver stats:")
        cProfile.runctx("backtracking.solve(crossword, words)", globals(), locals())
        print("=" * 88)


if __name__ == "__main__":
    main()
