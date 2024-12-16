from collections import namedtuple, defaultdict
from typing import List, Dict
from itertools import combinations

Point = namedtuple("Point", "x y")


def project(p1: Point, p2: Point):
    return Point(2 * p1.x - p2.x, 2 * p1.y - p2.y )


def locate_antennas(data: List[List[str]]) -> Dict[str, List[Point]]:
    antennas = defaultdict(list)
    for row_idx, row in enumerate(data):
        for cell_idx, cell in enumerate(row):
            if cell != ".":
                antennas[cell] += [Point(cell_idx, row_idx)]
    return antennas


def mark_antinodes(width: int, height: int, antennas: Dict[str, List[Point]]) -> List[List[str]]:
    def is_within(p: Point) -> bool:
        return 0 <= p.x < width and 0 <= p.y < height

    result = [["." for _ in range(width)] for _ in range(height)]
    for freq in antennas.keys():
        for a1, a2 in combinations(antennas[freq], 2):
            result[a1.y][a1.x] = "*"
            result[a2.y][a2.x] = "*"

            lp, rp = a1, a2
            while True:
                new_lp = project(lp, rp)
                if is_within(new_lp):
                    result[new_lp.y][new_lp.x] = "*"
                    rp = lp
                    lp = new_lp
                else:
                    break

            lp, rp = a1, a2
            while True:
                new_rp = project(rp, lp)
                if is_within(new_rp):
                    result[new_rp.y][new_rp.x] = "*"
                    lp = rp
                    rp = new_rp
                else:
                    break

    return result

def count_antinodes(data: List[List[str]]) -> int:
    return sum(cell == "*" for row in data for cell in row)


def load_data(lines: List[str]) -> List[List[str]]:
    return [list(line.strip().replace("\n", "")) for line in lines if line]


def show(data: List[List[str]]) -> None:
    print("\n".join(["".join(line) for line in data]))


if __name__ == "__main__":
    with open("input.txt", 'r') as f:
        data = f.readlines()


    prep_data = load_data(data)
    show(prep_data)
    antinodes_map = mark_antinodes(len(prep_data[0]), len(prep_data), locate_antennas(prep_data))
    print("-------")
    show(antinodes_map)
    print(count_antinodes(antinodes_map))
