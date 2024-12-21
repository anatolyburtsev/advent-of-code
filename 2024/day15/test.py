import pytest
from main_part2 import find_robot_position, can_move, push, Direction


@pytest.mark.parametrize("field, expected", [
    (
            [
                ['.', '@'],
                ['.', '.'],
            ],
            [
                ['.', '.'],
                ['.', '@'],
            ]
    ),
    (
            [
                ['.', '@'],
                ['[', ']'],
                ['.', '.'],
            ],
            [
                ['.', '.'],
                ['.', '@'],
                ['[', ']'],
            ]
    ),
    (
            [
                ['.', '.'],
                ['.', '@'],
                ['[', ']'],
                ['[', ']'],
                ['.', '.'],
                ['[', ']'],
            ],
            [
                ['.', '.'],
                ['.', '.'],
                ['.', '@'],
                ['[', ']'],
                ['[', ']'],
                ['[', ']'],
            ]
    ),
    (
            [
                ['.', '.', '.'],
                ['.', '.', '@'],
                ['.', '[', ']'],
                ['[', ']', '.'],
                ['.', '.', '.'],
                ['.', '[', ']'],
            ],
            [
                ['.', '.', '.'],
                ['.', '.', '.'],
                ['.', '.', '@'],
                ['.', '[', ']'],
                ['[', ']', '.'],
                ['.', '[', ']'],
            ]
    ),
    (
            [
                ['.', '.', '.'],
                ['.', '@', '.'],
                ['.', '[', ']'],
                ['[', ']', '.'],
                ['.', '.', '.'],
                ['.', '[', ']'],
            ],
            [
                ['.', '.', '.'],
                ['.', '.', '.'],
                ['.', '@', '.'],
                ['.', '[', ']'],
                ['[', ']', '.'],
                ['.', '[', ']'],
            ]
    ),
    (
            [
                ['.', '.', '.'],
                ['.', '.', '.'],
                ['@', '[', ']'],
                ['[', ']', '.'],
                ['.', '.', '.'],
                ['.', '[', ']'],
            ],
            [
                ['.', '.', '.'],
                ['.', '.', '.'],
                ['.', '[', ']'],
                ['@', '.', '.'],
                ['[', ']', '.'],
                ['.', '[', ']'],
            ]
    ),
    (
            [
                ['[', ']', '.', '@', '.'],
                ['[', ']', '[', ']', '.'],
                ['.', '[', ']', '[', ']'],
                ['.', '.', '.', '.', '.'],
            ],
            [
                ['[', ']', '.', '.', '.'],
                ['[', ']', '.', '@', '.'],
                ['.', '.', '[', ']', '.'],
                ['.', '[', ']', '[', ']'],
            ]
    ),
])
def test_sample_parametrize(field, expected):
    robot_position = find_robot_position(field)
    assert can_move(field, robot_position, Direction.DOWN) is True
    robot_position = push(field, robot_position, Direction.DOWN)
    assert field == expected
    assert can_move(field, robot_position, Direction.DOWN) is False
