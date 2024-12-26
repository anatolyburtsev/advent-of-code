from collections import namedtuple
from typing import List, Tuple

Field = List[List[str]]
Point = namedtuple("Point", ["x", "y"])

test = False
n = 7 if test else 71
cutover = 12 if test else 1024
filename = "test_input.txt" if test else "input.txt"

def show(data: Field, delimiter: str = '') -> None:
    for row in data:
        print(delimiter.join([str(x) for x in row]))
    print("\n")

def read_input(filename) -> List[Point]:
    with open(filename, "r") as f:
        return [Point(*([int(x) for x in line.strip().split(",")])) for line in f]

def put_holes(field: Field, points: List[Point]) -> Field:
    print(points[-1])
    for point in points:
        field[point.y][point.x] = "#"
    return field

VisitedType = dict[Point, int]

def can_move(field: Field, point: Point, direction: Tuple[int, int], visited: VisitedType) -> bool:
    dx, dy = direction
    new_x, new_y = point.x + dx, point.y + dy
    if 0 <= new_x < n and 0 <= new_y < n and field[new_y][new_x] == '.' and (new_x, new_y) not in visited:
        return True


def find_path(field: Field):
    queue = [(Point(0, 0), 0)]
    finish = Point(n-1, n-1)
    visited: VisitedType = dict()

    while queue:
        current, step_count = queue.pop(0)
        if current in visited:
            continue
        visited[current] = step_count
        if current == finish:
            return step_count
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if can_move(field, current, (dx, dy), visited):
                next_pos = Point(current.x + dx, current.y + dy)
                queue.append((next_pos, step_count + 1))

    return -1

def is_there_exit_k(obstacles):
    return lambda k: is_there_exit(k, obstacles)

def is_there_exit(k: int, obstacles: List[Point]) -> bool:
    field = [['.' for _ in range(n) ] for _ in range(n)]
    field = put_holes(field, obstacles[:k])
    step_count = find_path(field)
    return step_count > 0


def bin_search(f, lo, hi):
    while lo < hi:
        mid = (lo + hi) // 2
        if not f(mid):
            hi = mid
        else:
            lo = mid + 1
    return lo


if __name__ == "__main__":

    field = [['.' for y in range(n) ] for x in range(n)]
    # show(field)
    obstacles = read_input(filename)
    is_there_exit_fun = is_there_exit_k(obstacles)
    # res = bin_search(is_there_exit_fun, cutover, 3451)
    # print(f"Result: {res}")
    # print(obstacles[res-1])
    # print(obstacles[res])
    print(is_there_exit_fun(2911))
    print(is_there_exit_fun(2912))
    print(is_there_exit_fun(2913))

    # field = put_holes(field, obstacles[:cutover])
    # show(field)
    # step_count = find_path(field)
    # print(f"Step count: {step_count}")
