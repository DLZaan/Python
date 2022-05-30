"""
This script runs solver tests (with benchmarking)
"""
import cProfile
import pstats

import fill_in_generator
import fill_in_solver

OUTPUT_WIDTH = 88


def main():
    tests = []
    for i in range(6):
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

    solvers = [
        fill_in_solver.BacktrackingLinearSolver(),
        fill_in_solver.BacktrackingDiagonalSolver(),
        fill_in_solver.BacktrackingByLengthSolver(),
        fill_in_solver.BFCLinearSolver(),
        fill_in_solver.BFCDiagonalSolver(),
        fill_in_solver.BFCByLengthSolver(),
    ]

    for i, test in enumerate(tests):
        crossword = test["crossword"]
        words = test["words"]
        solution = test["solution"]
        print(f"TEST {i}")
        print(f"Crossword size = {len(crossword)}x{len(crossword[0])}")
        print(f"Words to fill = {len(words)}")
        for solver in solvers:
            print("-" * OUTPUT_WIDTH)
            pr = cProfile.Profile()
            pr.enable()
            result = solver.solve(crossword, words)
            pr.disable()
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
        print("=" * OUTPUT_WIDTH)


def add_test(i, height, width, seed, sparsity):
    grid = fill_in_generator.generate_grid(height, width, seed, sparsity)
    crossword = fill_in_generator.fill_crossword(grid, seed)
    words_list = fill_in_generator.extract_words(crossword)
    with open(f"tests/puzzle{i}.txt", "w") as puzzle:
        puzzle.write("\n".join(["".join(row) for row in grid]))
    with open(f"tests/solution{i}.txt", "w") as solution:
        solution.write("\n".join(["".join(row) for row in crossword]))
    with open(f"tests/words{i}.txt", "w") as words:
        words.writelines(word + "\n" for word in words_list)


if __name__ == "__main__":
    main()
