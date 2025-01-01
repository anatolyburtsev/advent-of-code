import re
from collections import deque
from itertools import product

digit_keypad = [
    ['7', '8', '9'],
    ['4', '5', '6'],
    ['1', '2', '3'],
    ['*', '0', 'A']
]

direct_keypad = [
    ['*', '^', 'A'],
    ['<', 'v', '>']
]

Keypad = list[list[str]]
Point = tuple[int, int]


def find_position(value: str, keypad: Keypad) -> Point:
    """
    Find the position of the given value in the keypad.
    Returns a tuple (row, col).
    """
    for r, row in enumerate(keypad):
        for c, val in enumerate(row):
            if val == value:
                return r, c
    raise ValueError(f"Value '{value}' not found in keypad.")


def find_all_shortest_paths(start_v: str, end_v: str, keypad: Keypad):
    """
    Find all shortest paths from start to end on the given keypad using DFS.
    Returns a list of paths, where each path is a list of points.
    """
    moves = [(-1, 0, '^'),  # up
             (1, 0, 'v'),  # down
             (0, -1, '<'),  # left
             (0, 1, '>')]  # right

    start = find_position(start_v, keypad)
    end = find_position(end_v, keypad)

    all_paths = []
    min_length = float('inf')

    def dfs(r: int, c: int, path: str, visited: set):
        nonlocal min_length

        if len(path) > min_length:
            return

        if (r, c) == end:
            if len(path) <= min_length:
                if len(path) < min_length:
                    all_paths.clear()
                    min_length = len(path)
                all_paths.append(path)
            return

        for dr, dc, symbol in moves:
            nr, nc = r + dr, c + dc

            # Check bounds
            if not (0 <= nr < len(keypad) and 0 <= nc < len(keypad[0])):
                continue
            # Check if it's not a gap
            if keypad[nr][nc] == '*':
                continue

            if (nr, nc) in visited:
                continue

            visited.add((nr, nc))
            dfs(nr, nc, path + symbol, visited)
            visited.remove((nr, nc))

    visited = {start}
    dfs(start[0], start[1], "", visited)

    return all_paths


def generate_combinations(options):
    return ['A'.join(comb) for comb in product(*options)]

def find_level2_paths_between_2_digits(start: str, end: str) -> list[str]:
    paths_level1 = find_all_shortest_paths(start, end, digit_keypad)
    total_path_level1 = []
    for path in paths_level1:
        path = "A" + path + "A"
        total_path_level2 = []
        for i in range(len(path) - 1):
            start2 = path[i]
            end2 = path[i + 1]
            total_path_level2.append(find_all_shortest_paths(start2, end2, direct_keypad))
        total_path_level1.append(generate_combinations(total_path_level2))

    total_path_level1 = [x + "A" for sublist in total_path_level1 for x in sublist]
    return total_path_level1

def find_level3_paths(path: str) -> list[str]:
    total_path_level3 = []
    total_path_level2 = []
    for i in range(len(path) - 1):
        start = path[i]
        end = path[i + 1]
        total_path_level2.append(find_all_shortest_paths(start, end, direct_keypad))
    total_path_level3.append(generate_combinations(total_path_level2))
    total_path_level3 = [x + "A" for sublist in total_path_level3 for x in sublist]
    return total_path_level3

def run_calculations(code: str) -> tuple[int, str]:
    level3_code = []
    for i in range(len(code) - 1):
        start = code[i]
        end = code[i + 1]
        level2_paths = find_level2_paths_between_2_digits(start, end)
        level3_paths = [find_level3_paths("A" + x) for x in level2_paths]
        level3_paths = [x for sublist in level3_paths for x in sublist]
        print(f"{level3_paths=}")
        level3_path_min_len = min([len(x) for x in level3_paths])
        min_level3_path = [x for x in level3_paths if len(x) == level3_path_min_len][0]
        level3_code.append(min_level3_path)
    level3_code = "".join(level3_code)
    return len(level3_code), level3_code

def get_result(code: str) -> int:
    l,  code_l3 = run_calculations(code)
    numbers = int(re.findall(r'\d+', code)[0])
    result = numbers * l
    print(f"{code=} {l=} {code_l3=} {result=}")
    return result

if __name__ == "__main__":
    test_codes = ['029A', '980A', '179A', '456A', '379A']
    codes = ['671A', '279A', '083A', '974A', '386A']  # 174588 is too high. Answer: 171596

    # code = "A029A"

    # level2_paths = find_level2_paths_between_2_digits("9", "A")
    # print(f"{level2_paths=}")
    # level3_paths = find_level3_paths("A" + level2_paths[3])
    # print([len(x) for x in level3_paths])
    # print(level3_paths)

    # print(run_calculations(code))
    # print(get_result(code))

    results = []
    for code in codes:
        results.append( get_result("A" + code))
    #
    print(results)
    print(sum(results))

