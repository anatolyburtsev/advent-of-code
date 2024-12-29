from collections import Counter
from functools import lru_cache

def read_and_parse(filename: str) -> list[list[str]]:
    """
    Read the maze from a file and return it as a 2D list with borders removed.
    """
    with open(filename, 'r') as f:
        data = f.read()

    # Parse the raw data into a 2D list
    maze = [list(line) for line in data.strip().splitlines()]

    # Remove top and bottom rows
    maze = maze[1:-1]

    # Remove first and last character from each row
    maze = [row[1:-1] for row in maze]

    return maze


def show(data: list[list[str]], delimiter: str = '') -> None:
    for row in data:
        print(delimiter.join([str(x) for x in row]))
    print("\n")


Field = list[list[str]]
FieldDistToEnd = list[list[int | None]]

Point = tuple[int, int]


def at(field: Field, p: Point) -> str:
    return field[p[1]][p[0]]


def find_start(field: Field) -> Point:
    for y, line in enumerate(field):
        for x, char in enumerate(line):
            if char == 'S':
                return x, y
    raise ValueError("No start found")


def find_end(field: Field) -> Point:
    for y, line in enumerate(field):
        for x, char in enumerate(line):
            if char == 'E':
                return x, y
    raise ValueError("No end found")

def find_all_distances(field: Field) -> tuple[FieldDistToEnd, dict[Point, Point]]:
    s = find_end(field)
    visited = set()
    dist_to_end: FieldDistToEnd = [[None for _ in range(len(field[0]))] for _ in range(len(field))]
    successor: dict[Point, Point] = {}

    queue = [(s, 0)]
    while queue:
        (x, y), distance = queue.pop(0)
        if (x, y) in visited:
            continue
        dist_to_end[y][x] = distance
        visited.add((x, y))

        if at(field, (x, y)) == "S":
            continue

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if not (0 <= x + dx < len(field[0]) and 0 <= y + dy < len(field)):
                continue
            if (x + dx, y + dy) in visited:
                continue
            next_position_value = at(field, (x + dx, y + dy))

            match next_position_value:
                case '.' | "S":
                    queue.append(((x + dx, y + dy), distance + 1))
                    successor[(x + dx, y + dy)] = (x, y)
                case 'E':
                    raise ValueError(f"Unexpected value: {next_position_value}")
                case '#':
                    continue
                case _:
                    raise ValueError(f"Unexpected value: {next_position_value}")
    return dist_to_end, successor


def backtrack_path(successor):
    path = []
    current = find_start(field)
    while current != find_end(field):
        path.append(current)
        current = successor[current]
    return path

def next_positions(x: int, y: int, cheat_enabled: bool, visited: set[Point]) -> list[Point]:
        next_steps = []
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if not (0 <= x + dx < len(field[0]) and 0 <= y + dy < len(field)):
                continue
            if (x + dx, y + dy) in visited:
                continue
            next_position_value = at(field, (x + dx, y + dy))

            match (next_position_value, cheat_enabled):
                case ('.', _) | ('E', _):
                    next_steps.append((x + dx, y + dy))
                case ('#', True):
                    next_steps.append((x + dx, y + dy))
                case ('#', False):
                    continue
                case ('S', _):
                    continue
                case _:
                    raise ValueError(f"Unexpected value: {next_position_value}")

        return next_steps

def get_next_cheating_positions(current: Point, visited: set[Point]) -> list[Point]:
        next_positions_1 = next_positions(current[0], current[1], True, visited)
        next_positions_2 = [next_positions(np[0], np[1], True, visited) for np in next_positions_1]
        next_positions_2_flat = set([pos for sublist in next_positions_2 for pos in sublist])
        next_positions_2_flat_possible = [p for p in next_positions_2_flat if at(field, p) != '#']
        return next_positions_2_flat_possible

def is_point_within(p: Point, field: Field) -> bool:
    return 0 <= p[0] < len(field[0]) and 0 <= p[1] < len(field)

def get_next_cheating_positions_v2(current: Point, field: Field, size: int, visited: set[Point]) -> list[Point]:
    points = []
    for i in range(size + 1):
        for j in range(i + 1):
            points += list(set([
                (current[0] + j, current[1] + size - i),
                (current[0] - j, current[1] + size - i),
                (current[0] + j, current[1] - size + i),
                (current[0] - j, current[1] - size + i),
            ]))
    points = [p for p in points if is_point_within(p, field) and at(field, p) != '#' and p not in visited]
    return points

if __name__ == "__main__":
    field = read_and_parse("input.txt")

    dist_to_end, successor = find_all_distances(field)

    path = backtrack_path(successor)
    # for p in path:
    #     field[p[1]][p[0]] = 'O'

    path_length = len(path)
    print(f"{path_length=}")
    #
    # ps = get_next_cheating_positions_v2((4, 4), field, 7, set())
    # for p in ps:
    #     field[p[1]][p[0]] = "*"
    # show(field)

    visited = set()
    distances = {}
    threshold = 100
    for step_no, p in enumerate(path):
        visited.add(p)
        possible_next_positions = get_next_cheating_positions_v2(p, field, 20, visited)
        for np in possible_next_positions:
            cheating_distance = abs(p[0] - np[0]) + abs(p[1] - np[1])
            new_path_length = step_no + dist_to_end[np[1]][np[0]] + cheating_distance
            if new_path_length + threshold <= path_length:
                distance_value = path_length - new_path_length
                if (p, np) not in distances or distances[(p, np)] < distance_value:
                    distances[(p, np)] = distance_value

    print(
        sum(
            v >= threshold for v in distances.values()
        )
    )
#
