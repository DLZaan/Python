"""
This script runs solver tests (with benchmarking)
"""
import cProfile
import pstats

import fill_in_solver


def main():
    tests = []
    for i in range(4):
        with (
            open(f"tests/puzzle{i}.txt") as puzzle,
            open(f"tests/words{i}.txt") as words,
            open(f"tests/solution{i}.txt") as solution,
        ):
            tests.append(
                {
                    "crossword": [list(line.strip()) for line in puzzle.readlines()],
                    "words": [word.strip() for word in words.readlines()],
                    "solution": [line.strip() for line in solution.readlines()],
                }
            )

    pr = cProfile.Profile()
    solver = fill_in_solver.BacktrackingSolver()
    for i, test in enumerate(tests):
        crossword = test["crossword"]
        words = test["words"]
        solution = test["solution"]
        print(f"TEST {i}")
        print(f"Crossword size = {len(crossword)}x{len(crossword[0])}")
        print(f"Words to fill = {len(words)}")

        pr.enable()
        result = solver.solve(crossword, words)
        pr.disable()

        if len(result) != len(solution):
            print("Crossword solved with errors - wrong number of rows!")
        elif any("".join(row) != solution[i] for i, row in enumerate(result)):
            print("Crossword solved with errors - fill missmatch!")
        else:
            print("Crossword solved correctly!")
        print(f"Backtracking solver stats:")
        pstats.Stats(pr).sort_stats(pstats.SortKey.CUMULATIVE).print_stats(0.1)
        print("=" * 88)


if __name__ == "__main__":
    main()
