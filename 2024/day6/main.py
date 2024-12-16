from enum import Enum
from typing import List, Tuple
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])

class Direction(Enum):
    UP = "^"
    RIGHT = ">"
    DOWN = "v"
    LEFT = "<"

    @staticmethod
    def values():
        return [v.value for v in list(Direction)]

    @staticmethod
    def value_of(symbol: str):
        for direction in Direction:
            if direction.value == symbol:
                return direction
        raise ValueError(f"{symbol} is not a direction")

    def turn(self):
        directions = list(Direction)
        next_idx = (directions.index(self) + 1) % len(directions)
        return directions[next_idx]

VISITED = "X"
BLOCK = "#"
EMPTY = "."

def is_position_within_borders(floor: List[str], position: Point) -> bool:
    x_size = len(floor[0])
    y_size = len(floor)
    return 0 <= position.x < x_size and 0 <= position.y < y_size

class Board:

    def __init__(self, floor: List[str]):
        self.x_size = len(floor[0])
        self.y_size = len(floor)
        self.floor = floor
        self.passed_directions:List[List] = [[EMPTY] * self.x_size for _ in range(self.y_size)]
        self.position, self.direction = self.__find_position(floor)
        self.is_finished = False
        self.block_counts = 0

    def at(self, pos: Point):
        return self.floor[pos.y][pos.x]

    def direction_at(self, pos: Point) -> List[Direction]:
        return self.passed_directions[pos.y][pos.x]

    def put_direction_at(self, pos: Point, directions: List[Direction]):
        if self.passed_directions[pos.y][pos.x] == EMPTY:
            self.passed_directions[pos.y][pos.x] = directions

    def replace_at(self, pos: Point, new_symbol: str):
        self.floor[pos.y] = self.floor[pos.y][:pos.x] + new_symbol + self.floor[pos.y][pos.x+1:]


    @staticmethod
    def get_next_possible_position(position: Point, direction: Direction) -> Point:
        match direction:
            case Direction.UP:
                return Point(position.x, position.y - 1)
            case Direction.LEFT:
                return Point(position.x - 1, position.y)
            case Direction.DOWN:
                return Point(position.x, position.y + 1)
            case Direction.RIGHT:
                return Point(position.x + 1, position.y)
            case _:
                raise ValueError(f"unexpected direction {direction}")

    def is_loop_if_turn(self):
        turned_direction = self.direction.turn()
        next_position = self.position

        while True:
            next_position = self.get_next_possible_position(next_position, turned_direction)
            if not is_position_within_borders(self.floor, next_position):
                return False

            if self.at(next_position) == BLOCK:
                return False

            if self.at(next_position) == VISITED:
                return turned_direction in self.direction_at(next_position)


    def make_step(self):
        next_desired_position = self.get_next_possible_position(self.position, self.direction)

        if not is_position_within_borders(self.floor, next_desired_position):
            self.replace_at(self.position, VISITED)
            self.is_finished = True
            return

        if self.at(next_desired_position) == BLOCK:
            self.put_direction_at(self.position, [self.direction, self.direction.turn()])
            self.direction = self.direction.turn()
            self.replace_at(self.position, self.direction.value)
            return

        if self.at(next_desired_position) in [EMPTY, VISITED]:
            self.put_direction_at(self.position, [self.direction])



            # if self.at(next_desired_position) == VISITED and self.direction_at(next_desired_position) == self.direction.turn():
            if self.is_loop_if_turn():
                self.block_counts += 1

            current_symbol = self.at(self.position)
            self.replace_at(self.position, VISITED)
            self.replace_at(next_desired_position, current_symbol)
            self.position = next_desired_position
            return
        raise ValueError(f"unexpected behavior at {self.at(next_desired_position)}")

    def count_steps(self):
        return sum(1 for row in self.floor for cell in row if cell == VISITED)

    def __find_position(self, floor):
        for v in range(len(floor)):
            for h in range(len(floor[0])):
                if floor[v][h] in Direction.values():
                    return Point(h, v), Direction.value_of(floor[v][h])

    def __repr__(self):
        # Create a string representation of the floor (the board)
        board_state = "\n".join(
            [f"{''.join(row)}" for row in self.floor]
        )

        # Create a string representation of the passed_direction with 'U', 'D', 'L', 'R' for directions
        passed_direction_state = "\n".join(
            [''.join(
                direction.name[0] if isinstance(direction, Direction) else '.'
                for direction in row
            ) for row in self.passed_directions]
        )

        # Return the final formatted string with both the floor and passed directions
        return (
            f"Board({self.x_size}x{self.y_size}):\n{board_state}\n"
            f"Directions:\n{passed_direction_state}\n"
            f"Position: {self.position}, Direction: {self.direction.value}\n\n"
        )

if __name__ == "__main__":
    # print(Direction.values())
    with open("input.txt", "r") as f:
        floor = [x.strip() for x in f.readlines()]

    # floor = [
    #     ".#..",
    #     ".^.#",
    #     "....",
    #     "....",
    #     "..#."
    # ]

    b = Board(floor)
    # print(b)

    # b.make_step()
    # b.make_step()
    # print(b)
    # i = 0
    while not b.is_finished:
        b.make_step()
        # print(f"{i=}")
        # i += 1
        # print(b)

    # ....#.....
    # .........#
    # ..........
    # ..#.......
    # .......#..
    # ..........
    # .#.O^.....
    # ......OO#.
    # #.........
    # ......#...

    print(b.block_counts)
    # print(b)

    # print(b.count_steps())

    # print(Direction.DOWN.turn())

    # print(make_step(floor, Point(9, 0), Direction.RIGHT))
