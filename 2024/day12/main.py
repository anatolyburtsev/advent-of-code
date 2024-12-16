from collections import namedtuple, deque
from dataclasses import dataclass
from typing import List


class Field:
    def __init__(self, data: List[List[str]]):
        self.data = data
        # 0 - not visited
        # 1 - in queue
        # 2 - visited
        self.traverse_map: List[List[int]] = [[0] * len(data[0]) for _ in range(len(data))]
        self.vertical_fence_map: List[List[int]] = []
        self.horizontal_fence_map: List[List[int]] = []
        self.cleanup_fences()

    def cleanup_fences(self):
        self.vertical_fence_map = [[0] * (len(data[0]) + 1) for _ in range(len(data) + 1)]
        self.horizontal_fence_map = [[0] * (len(data[0]) + 1) for _ in range(len(data) + 1)]

    def build_fences(self, value: str, x: int, y:int) -> int:
        fences_added = 0
        # upper fence
        if self.at(x, y-1) != value and self.horizontal_fence_map[y][x] == 0:
            fences_added += 1
            dx = 0
            while self.at(x + dx, y) == value and self.at(x + dx, y - 1) != value:
                self.horizontal_fence_map[y][x + dx] = 1
                dx += 1
            dx = -1
            while self.at(x + dx, y) == value and self.at(x + dx, y - 1) != value:
                self.horizontal_fence_map[y][x + dx] = 1
                dx -= 1

        # down fence
        if self.at(x, y+1) != value and self.horizontal_fence_map[y+1][x] == 0:
            fences_added += 1
            dx = 0
            while self.at(x + dx, y) == value and self.at(x + dx, y + 1) != value:
                self.horizontal_fence_map[y+1][x + dx] = 1
                dx += 1
            dx = -1
            while self.at(x + dx, y) == value and self.at(x + dx, y + 1) != value:
                self.horizontal_fence_map[y+1][x + dx] = 1
                dx -= 1

        # left fence
        if self.at(x-1, y) != value and self.vertical_fence_map[y][x] == 0:
            fences_added += 1
            dy = 0
            while self.at(x, y + dy) == value and self.at(x-1, y+dy) != value:
                self.vertical_fence_map[y + dy][x] = 1
                dy += 1
            dy = -1
            while self.at(x, y + dy) == value and self.at(x-1, y+dy) != value:
                self.vertical_fence_map[y + dy][x] = 1
                dy -= 1


        # right fence
        if self.at(x+1, y) != value and self.vertical_fence_map[y][x+1] == 0:
            fences_added += 1
            dy = 0
            while self.at(x, y + dy) == value and self.at(x + 1, y + dy) != value:
                self.vertical_fence_map[y + dy][x+1] = 1
                dy += 1
            dy = -1
            while self.at(x, y + dy) == value and self.at(x + 1, y + dy) != value:
                self.vertical_fence_map[y + dy][x+1] = 1
                dy -= 1

        # print(f"at {x=} {y=} {fences_added=}")
        return fences_added


    def at(self, x: int, y: int) -> str|None:
        if x < 0 or y < 0 or y >= len(self.data) or x >= len(self.data[0]):
            return None
        return self.data[y][x]

    def visit(self, x: int, y: int):
        self.traverse_map[y][x] = 2

    def is_visited(self, x, y):
        if x < 0 or y < 0 or y >= len(self.traverse_map) or x >= len(self.traverse_map[0]):
            return True
        return self.traverse_map[y][x] == 2

    def is_queued(self, x: int, y: int) -> bool:
        if x < 0 or y < 0 or y >= len(self.traverse_map) or x >= len(self.traverse_map[0]):
            return True
        return self.traverse_map[y][x] == 1

    def count_borders(self, value, x, y) -> int:
        result = 0
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if self.at(x + dx, y + dy) != value: ##
                result += 1
        return result

    def bfs(self, x: int, y: int) -> (int, int):
        area = 0
        perimeter = 0
        fences = 0
        queue = deque()
        region_value = self.at(x, y)
        self.cleanup_fences()

        queue.append((x, y))
        while len(queue) > 0:
            [x, y] = queue.pop()
            self.visit(x, y)
            fences += self.build_fences(region_value, x, y)
            area += 1
            perimeter += self.count_borders(region_value, x, y)
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_x = x + dx
                new_y = y + dy
                if self.at(new_x, new_y) == region_value and not self.is_visited(new_x, new_y) and not self.is_queued(new_x, new_y):
                    self.traverse_map[new_y][new_x] = 1
                    queue.append((new_x, new_y))

        return area, perimeter, fences

    def bfs_all(self):
        result = list()
        for y in range(len(self.data)):
            for x in range(len(self.data[0])):
                if not self.is_visited(x, y):
                    result.append(self.bfs(x, y))
        print(f"{result=}")
        return result

    def calculate_price(self):
        return sum(
            area * fences for (area, _, fences) in self.bfs_all()
        )


def show(data: List[List[str]]):
    result = ("\n".join("".join(str(line)) for line in data)) + "\n"
    print(result)
    return result



if __name__ == "__main__":
    with open("input.txt", "r") as f:
        data = [list(l.strip()) for l in f.readlines()]

    show(data)
    f = Field(data)
    # print(f"{f.build_fences("B", 1, 1)=}")
    # print(f"{f.build_fences("C", 1, 2)=}")
    # print(f.traverse_map)
    # print(f.bfs(1, 2))
    # show(f.horizontal_fence_map)
    # show(f.vertical_fence_map)
    # show(f.traverse_map)
    print(f.calculate_price())
    # show(f.data)
    # print(f)
