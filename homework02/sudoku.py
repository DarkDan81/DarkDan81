import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    """Вывод Судоку"""
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    result = []
    x = 0
    for i in range(n):
        results = []
        for j in range(n):
            results.append(values[x])
            x += 1
        result.append(results)
    return result


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    n = pos[0]
    return grid[n]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    result = []
    n = pos[1]
    for i in grid:
        result.append(str(i[n]))
    return result


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    result = []
    row = (pos[0] // 3) + 1
    col = (pos[1] // 3) + 1
    for i in range(3):
        x = grid[(row * 3) - 3 + i]
        for j in range(3):
            result.append(str(x[(col * 3) - 3 + j]))
    return result


def find_empty_positions(
    grid: tp.List[tp.List[str]],
) -> tp.Optional[tp.Tuple[int, int]]:
    n = len(grid)
    for i in range(n):
        for j in range(n):
            if grid[i][j] == ".":
                return i, j
    return None


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    values = set("123456789")
    return values - set(get_row(grid, pos)) - set(get_col(grid, pos)) - set(get_block(grid, pos))


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    empty_pos = find_empty_positions(grid)
    if empty_pos is None:
        return grid
    else:
        possble_vallue = find_possible_values(grid, empty_pos)
        for i in possble_vallue:
            grid[empty_pos[0]][empty_pos[1]] = i
            if solve(grid):
                return grid
            grid[empty_pos[0]][empty_pos[1]] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    # TODO: Add doctests with bad puzzles
    for i in range(len(solution)):
        for j in range(len(solution)):
            if solution[i][j] == ".":
                return False
            if len(set(get_row(solution, (i, j)))) != 9:
                return False
            if len(set(get_col(solution, (i, j)))) != 9:
                return False
            if len(set(get_block(solution, (i, j)))) != 9:
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    """Генерация судоку заполненного на N элементов

    >>> grid = generate_sudoku(40)
    >>> sum(1 for row in grid for e in row if e == '.')
    41
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(1000)
    >>> sum(1 for row in grid for e in row if e == '.')
    0
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    >>> grid = generate_sudoku(0)
    >>> sum(1 for row in grid for e in row if e == '.')
    81
    >>> solution = solve(grid)
    >>> check_solution(solution)
    True
    """
    grid = solve([["."] * 9 for _ in range(9)])
    while grid is None:
        grid = solve([["."] * 9 for _ in range(9)])
    count = 0
    while count < 81 - N:
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if grid[i][j] != ".":
            grid[i][j] = "."
            count += 1
    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)
