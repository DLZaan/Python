"""
This script runs solver tests (with benchmarking)
"""
import cProfile
import pstats

import fill_in_solver


def main():
    tests = []
    for i in range(1):
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

    for i, test in enumerate(tests):
        crossword = test["crossword"]
        words = test["words"]
        solution = test["solution"]
        print(f"TEST {i}")
        print(f"Crossword size = {len(crossword)}x{len(crossword[0])}")
        print(f"Words to fill = {len(words)}")
        for solver in (
            fill_in_solver.BacktrackingSolver(),
            fill_in_solver.BacktrackingDiagonalSolver(),
            fill_in_solver.BacktrackingByLengthSolver(),
        ):
            pr = cProfile.Profile()
            pr.enable()
            result = solver.solve(crossword, words)
            pr.disable()
            print("-" * 88)
            print(f"{solver.__class__.__name__} stats:")
            if result is None:
                print("Correct solution cannot be found!")
            elif len(result) != len(solution):
                print("Crossword solved with errors - wrong number of rows!")
            elif any("".join(row) != solution[i] for i, row in enumerate(result)):
                print("Crossword solved with errors - fill missmatch!")
            else:
                print("Crossword solved correctly!")
            pstats.Stats(pr).sort_stats(pstats.SortKey.CUMULATIVE).print_stats(0.1)
        print("=" * 88)


if __name__ == "__main__":
    main()
