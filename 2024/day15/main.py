from collections import namedtuple
from typing import List
from enum import Enum


class Direction(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    @staticmethod
    def valueOf(char: str) -> 'Direction':
        if char == '^':
            return Direction.UP
        elif char == 'v':
            return Direction.DOWN
        elif char == '<':
            return Direction.LEFT
        elif char == '>':
            return Direction.RIGHT
        else:
            raise ValueError(f"Invalid direction character: {char}")


Field = List[List[str]]


def parse_input(filename: str) -> tuple[Field, list[str]]:
    with open(filename, 'r') as file:
        # Read all lines and remove trailing whitespace
        lines = [line.strip() for line in file.readlines()]

        field_lines = []
        instructions = []
        is_field = True
        for line in lines:
            if not line:
                is_field = False
                continue

            if is_field:
                field_lines.append(line)
            else:
                instructions.append(line)
        # Split into field and instructions (last non-empty line)
        # field_lines = [line for line in lines if line]  # Remove empty lines
        # instructions = field_lines[-1]
        # field_lines = field_lines[:-1]  # Remove instructions line

        # Remove border lines (top and bottom)
        field_lines = field_lines[1:-1]

        # Remove left and right borders and convert to list of lists
        field = [list(line[1:-1]) for line in field_lines]

        # Convert instructions into list of characters
        instructions = list([x for l in instructions for x in l])

        return field, instructions


Point = namedtuple("Point", ["x", "y"])


def push(field: Field, point: Point, direction: Direction) -> Point:
    dx, dy = {
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0)
    }[direction]

    # Check if we're at the edge
    if (direction == Direction.UP and point.y == 0) or \
            (direction == Direction.DOWN and point.y == len(field) - 1) or \
            (direction == Direction.LEFT and point.x == 0) or \
            (direction == Direction.RIGHT and point.x == len(field[0]) - 1):
        return point

    # Check if there's a wall in the direction
    if field[point.y + dy][point.x + dx] == "#":
        return point

    def find_empty_block(point: Point) -> Point | None:
        current_point = point
        while (0 <= current_point.y + dy < len(field)) and \
                (0 <= current_point.x + dx < len(field[0])):
            current_point = Point(current_point.x + dx, current_point.y + dy)
            if field[current_point.y][current_point.x] == "#":
                return None
            if field[current_point.y][current_point.x] == ".":
                return current_point
        return None

    empty_block = find_empty_block(point)
    if not empty_block:
        return point
    else:
        field[empty_block.y][empty_block.x] = "O"
        field[point.y][point.x] = "."
        field[point.y + dy][point.x + dx] = "@"
        return Point(point.x + dx, point.y + dy)


def show(field: Field):
    print("\n".join(["".join(line) for line in field]) + "\n")


def find_robot_position(field: Field) -> Point:
    for y, line in enumerate(field):
        for x, char in enumerate(line):
            if char == "@":
                return Point(x, y)
    raise ValueError("No robot found")


def calculate_result(field: Field) -> int:
    result = 0
    for y, line in enumerate(field):
        for x, char in enumerate(line):
            if char == "O":
                result += 100 * (y + 1) + (x + 1)
    return result


if __name__ == "__main__":
    field, moves = parse_input("input.txt")
    # field = [
    #     ['.', '.', '.'],
    #     ['.', 'O', '.'],
    #     ['.', '@', '.'],
    # ]
    show(field)
    print(moves)

    robot_position = find_robot_position(field)
    for move in moves:
        direction = Direction.valueOf(move)
        print(f"Moving {move} from {robot_position}")
        robot_position = push(field, robot_position, direction)
        print(f"Moved to {robot_position}")
        show(field)

    print("Result:", calculate_result(field))

    # push(field, Point(1, 2), Direction.UP)
    # show(field)
    # push(field, Point(1, 1), Direction.DOWN)
    # show(field)
    # push(field, Point(1, 2), Direction.UP)
    # show(field)
