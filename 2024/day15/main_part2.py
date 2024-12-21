from collections import namedtuple
from typing import List
from enum import Enum
from copy import deepcopy
from viz import ArrayViewer

from matplotlib import pyplot as plt


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


def can_move(field: Field, point: Point, direction: Direction) -> bool:
    if direction in [Direction.UP, Direction.DOWN]:
        return can_move_vertical_v2(field, point, direction)
    else:
        return can_move_horizontal(field, point, direction)


def can_move_vertical(field: Field, point: Point, direction: Direction) -> bool:
    dy = 1 if direction == Direction.DOWN else -1

    if (direction == Direction.UP and point.y == 0) or \
            (direction == Direction.DOWN and point.y == len(field) - 1):
        return False

    current_value = field[point.y][point.x]
    pushing_value = field[point.y + dy][point.x]
    i_am_robot = current_value == "@"
    i_am_block = current_value == "["
    i_am_block_right = current_value == "]"
    if not (i_am_robot or i_am_block or i_am_block_right):
        print(
            f"got {current_value=}, {pushing_value=}, {i_am_robot=}, {i_am_block=}, {i_am_block_right=} pos: {point.x=} {point.y=}")
        raise ValueError(f"Unexpected value: {current_value}")

    match pushing_value:
        case '.':
            if i_am_block:
                if field[point.y + dy][point.x + 1] == '.':
                    return True
                # .   .[]
                # .   [].
                # .   @..
                return can_move_vertical(field, Point(point.x + 1, point.y), direction)
            return True
        case "#":
            return False
        case "[":
            return can_move_vertical(field, Point(point.x, point.y + dy), direction)
        case "]":
            if i_am_robot:
                return can_move_vertical(field, Point(point.x - 1, point.y + dy), direction)
            if i_am_block:
                return can_move_vertical(field, Point(point.x + 1, point.y + dy), direction) and \
                    can_move_vertical(field, Point(point.x, point.y + dy), direction)
            if i_am_block_right:
                raise ValueError("Impossible situation")
                return can_move_vertical(field, Point(point.x - 1, point.y + dy), direction)
        case _:
            raise ValueError(f"Unexpected value: {field[point.y + dy][point.x]}")


def can_move_vertical_v2(field: Field, point: Point, direction: Direction) -> bool:
    dy = 1 if direction == Direction.DOWN else -1

    if (direction == Direction.UP and point.y == 0) or \
            (direction == Direction.DOWN and point.y == len(field) - 1):
        return False

    current_value = field[point.y][point.x]
    pushing_value = field[point.y + dy][point.x]
    i_am_robot = current_value == "@"
    i_am_block = current_value == "["
    i_am_block_right = current_value == "]"

    if not (i_am_robot or i_am_block):
        print(
            f"got {current_value=}, {pushing_value=}, {i_am_robot=}, {i_am_block=}, {i_am_block_right=} pos: {point.x=} {point.y=}")
        raise ValueError(f"Unexpected value: {current_value}")

    if i_am_robot:
        match pushing_value:
            case '.':
                return True
            case '#':
                return False
            case '[':
                return can_move_vertical_v2(field, Point(point.x, point.y + dy), direction)
            case ']':
                return can_move_vertical_v2(field, Point(point.x - 1, point.y + dy), direction)
            case _:
                raise ValueError(f"Unexpected value: {pushing_value}")

    if i_am_block:
        pushing_right_value = field[point.y + dy][point.x + 1]
        match pushing_value:
            case '.':
                if pushing_right_value == '.':
                    return True
                if pushing_right_value == "#":
                    return False
                if pushing_right_value == '[':
                    return can_move_vertical_v2(field, Point(point.x + 1, point.y + dy), direction)
                raise ValueError("Impossible situation2")
            case '#':
                return False
            case '[':
                return can_move_vertical_v2(field, Point(point.x, point.y + dy), direction)
            case ']':
                if pushing_right_value == '#':
                    return False
                if pushing_right_value == '.':
                    return can_move_vertical_v2(field, Point(point.x - 1, point.y + dy), direction)
                if pushing_right_value == '[':
                    return can_move_vertical_v2(field, Point(point.x + 1, point.y + dy), direction) and \
                        can_move_vertical_v2(field, Point(point.x - 1, point.y + dy), direction)
                raise ValueError("Impossible situation3")

            case _:
                raise ValueError(f"Unexpected value2: {pushing_value}")


def can_move_horizontal(field: Field, point: Point, direction: Direction) -> bool:
    dx = 1 if direction == Direction.RIGHT else -1

    if (direction == Direction.LEFT and point.x == 0) or \
            (direction == Direction.RIGHT and point.x == len(field[0]) - 1):
        return False

    match field[point.y][point.x + dx]:
        case '.':
            return True
        case "#":
            return False
        case "]":
            return can_move_horizontal(field, Point(point.x + dx * 2, point.y),
                                       direction) if direction == Direction.LEFT else False
        case "[":
            return can_move_horizontal(field, Point(point.x + dx * 2, point.y),
                                       direction) if direction == Direction.RIGHT else False
        case _:
            raise ValueError(f"Unexpected value: {field[point.y][point.x + dx]}")


def push_vertically(field: Field, push_point: Point, direction: Direction) -> Point:
    dy = 1 if direction == Direction.DOWN else -1

    block_point = Point(push_point.x - 1, push_point.y + dy) if field[push_point.y + dy][
                                                                    push_point.x - 1] == '[' else Point(push_point.x,
                                                                                                        push_point.y + dy)
    if field[block_point.y][block_point.x] == '.':
        field[block_point.y][block_point.x] = '@'
        field[push_point.y][push_point.x] = '.'
        return block_point

    if (direction == Direction.UP and block_point.y == 0) or \
            (direction == Direction.DOWN and block_point.y == len(field) - 1):
        raise ValueError(f"Cannot move {direction.value} from edge")

    if field[block_point.y + dy][block_point.x] == '[':
        push_vertically(field, Point(block_point.x, block_point.y), direction)
    if field[block_point.y + dy][block_point.x] == ']':
        push_vertically(field, Point(block_point.x - 1, block_point.y), direction)
    if field[block_point.y + dy][block_point.x + 1] == '[':
        push_vertically(field, Point(block_point.x + 1, block_point.y), direction)

    move_robot = field[push_point.y][push_point.x] == '@'

    field[push_point.y][push_point.x] = '.'
    field[block_point.y][block_point.x] = '.'
    field[block_point.y][block_point.x + 1] = '.'
    field[block_point.y + dy][block_point.x] = '['
    field[block_point.y + dy][block_point.x + 1] = ']'
    if move_robot:
        field[push_point.y + dy][push_point.x] = '@'

    return Point(push_point.x, push_point.y + dy)


def push_vertically_v2(field: Field, point: Point, direction: Direction) -> Point:
    dy = 1 if direction == Direction.DOWN else -1

    current_value = field[point.y][point.x]
    pushing_value = field[point.y + dy][point.x]
    i_am_robot = current_value == "@"
    i_am_block = current_value == "["

    if not (i_am_robot or i_am_block):
        print(f"got {current_value=}, {pushing_value=}, {i_am_robot=}, {i_am_block=} pos: {point.x=} {point.y=}")
        raise ValueError(f"Unexpected value: {current_value}")

    if i_am_robot:
        match pushing_value:
            case '.':
                pass
            case '[':
                push_vertically_v2(field, Point(point.x, point.y + dy), direction)
            case ']':
                push_vertically_v2(field, Point(point.x - 1, point.y + dy), direction)
            case _:
                raise ValueError(f"Unexpected value: {pushing_value}")

        field[point.y][point.x] = '.'
        field[point.y + dy][point.x] = '@'
        return Point(point.x, point.y + dy)

    if i_am_block:
        pushing_right_value = field[point.y + dy][point.x + 1]
        match pushing_value:
            case ".":
                if pushing_right_value == ".":
                    pass
                elif pushing_right_value == "[":
                    push_vertically_v2(field, Point(point.x + 1, point.y + dy), direction)
                else:
                    raise ValueError("Impossible situation2")
            case "[":
                push_vertically_v2(field, Point(point.x, point.y + dy), direction)
            case "]":
                push_vertically_v2(field, Point(point.x - 1, point.y + dy), direction)
                if pushing_right_value == "[":
                    push_vertically_v2(field, Point(point.x + 1, point.y + dy), direction)
        field[point.y][point.x] = '.'
        field[point.y][point.x+1] = '.'
        field[point.y+dy][point.x] = '['
        field[point.y+dy][point.x+1] = ']'

def push_horizontal(field: Field, position: Point, direction: Direction) -> Point:
    dx = 1 if direction == Direction.RIGHT else -1

    if (direction == Direction.LEFT and position.x == 0) or \
            (direction == Direction.RIGHT and position.x == len(field[0]) - 1):
        raise ValueError(f"Cannot move {direction.value} from edge")

    empty_block_position = Point(position.x, position.y)
    while field[empty_block_position.y][empty_block_position.x] != '.':
        empty_block_position = Point(empty_block_position.x + dx, empty_block_position.y)

    if direction == Direction.LEFT:
        for x in range(empty_block_position.x, position.x):
            field[position.y][x] = field[position.y][x + 1]
    else:
        for x in range(empty_block_position.x, position.x, -1):
            field[position.y][x] = field[position.y][x - 1]

    field[position.y][position.x] = '.'
    return Point(position.x + dx, position.y)


def push(field: Field, position: Point, direction: Direction) -> Point:
    if direction in [Direction.UP, Direction.DOWN]:
        return push_vertically_v2(field, position, direction)
    else:
        return push_horizontal(field, position, direction)


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
            if char == "[":
                result += 100 * (y + 1) + (x + 2)
    return result


def double_field(field: Field) -> Field:
    new_field = []
    for line in field:
        new_line = []
        for char in line:
            match char:
                case "#" | ".":
                    new_line.append(char)
                    new_line.append(char)
                case "O":
                    new_line.append("[")
                    new_line.append("]")
                case "@":
                    new_line.append("@")
                    new_line.append(".")
        new_field.append(new_line)
    return new_field


if __name__ == "__main__":
    field, moves = parse_input("input.txt")
    # field = [
    #     ['.', '.', '.'],
    #     ['.', 'O', '.'],
    #     ['.', '@', '.'],
    # ]
    # show(field)

    field = double_field(field)
    # field = [
    #     ['.', '.', '.', '.'],
    #     ['.', '.', '.', '@'],
    #     ['.', '.', '[', ']'],
    #     ['.', '.', '[', ']'],
    #     ['.', '.', '.', '.'],
    #     # ['.', '.', '[', ']'],
    # ]
    # show(field)
    # robot_position = find_robot_position(field)
    # print(can_move(field, robot_position, Direction.DOWN))
    # robot_position = push(field, robot_position, Direction.DOWN)
    # show(field)
    #

    robot_position = find_robot_position(field)
    for move in moves:
        direction = Direction.valueOf(move)
        print(f"Moving {move} from {robot_position}")
        if can_move(field, robot_position, direction):
            robot_position = push(field, robot_position, direction)
        else:
            print(f"Cannot move {move}")
        # show(field)

    print("Result:", calculate_result(field))

    # viewer = ArrayViewer(slides)
    # plt.show()
