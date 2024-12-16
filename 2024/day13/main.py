from typing import Tuple
import re


def process(a1: int, b1: int, a2: int, b2: int, c1: int, c2: int) -> int:
    c1 += 10000000000000
    c2 += 10000000000000
    a_cost = 3
    b_cost = 1
    # ax is always >= then bx
    if a1 < a2:
        a1, a2 = a2, a1
        b1, b2 = b2, b1
        a_cost, b_cost = b_cost, a_cost

    a_max = min(int(c1 / a1), int(c2 / b1))

    a_count = a_max
    b_count = 0

    def get_position() -> Tuple[int, int]:
        return a_count * a1 + b_count * a2, a_count * b1 + b_count * b2

    costs = []

    BIG_NUMBER = 300

    while a_count >= 0:
        # print(f"{a_count=}, {b_count=}")
        b_count = int((c1 - a_count * a1) / a2)

        pos = get_position()
        print(f"{a_count=}, {b_count=}, {c1 - pos[0]}, {c2 - pos[1]}")

        if get_position() == (c1, c2):
            costs.append(a_cost * a_count + b_cost * b_count)
            print(f"Match! {a_count=}, {b_count=}")

        # if c2 - a_count * b1 > BIG_NUMBER:
        #
        #     a_count -= ((abs(c2 - pos[1]) // max(b1, b2)) - 1)
        # else:
        a_count -= 1
        print(f"{a_count=}")

    return min(costs) if costs else 0

def gcd(a: int, b: int) -> int:
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a


def parse_input(filename):
    result = []
    current_group = []

    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # Extract numbers using regex
            numbers = re.findall(r'[XY][+=](-?\d+)', line)
            numbers = [int(n) for n in numbers]
            current_group.extend(numbers)

            if len(current_group) == 6:
                result.append(tuple(current_group))
                current_group = []

    return result


def is_not_possible(ax, ay, bx, by, px, py) -> bool:
    x_gcd = gcd(ax, bx)
    y_gcd = gcd(ay, by)
    return not(px % x_gcd == 0 and py % y_gcd == 0)

def find_x0(a1: int, b1: int, a2: int, b2: int, c1: int, c2: int):
    k = a1 * b2 - a2 * b1
    c = a1 * c2 - c1 * a2
    return c / k


if __name__ == "__main__":
    inp = (26, 66, 67, 21, 10000000012748, 10000000012176)
    # print(find_x0(*inp))
    print(process(*inp))

    # print(gcd(66, 21))
    # print(10000000012176 % 3)
    # print(is_not_possible(94, 34, 22, 67, 10000000008400, 10000000005400))
    # data = parse_input("test_input.txt")
    # print(
    #     sum([process(*line) for line in data])
    # )
