from enum import Enum


class Device(Enum):
    LOCK = 1
    KEY = 2


def parse(schema: list[str]) -> tuple[Device, list[int]]:
    device = Device.LOCK if schema[0] == "#####" else Device.KEY
    heights = list()
    for j in range(len(schema[0])):
        hash_counter = 0
        for i in range(1, len(schema) - 1):
            if schema[i][j] == "#":
                hash_counter += 1
        heights.append(hash_counter)
    return device, heights


def load_data(filename: str) -> list[tuple[Device, list[int]]]:
    with open(filename, "r") as f:
        lines = f.readlines()
        devices = [parse([x.strip() for x in lines[i:i+7]]) for i in range(0, len(lines), 8)]
        return devices

def separate(devices: list[tuple[Device, list[int]]]) -> tuple[list[list[int]], list[list[int]]]:
    keys = [x[1] for x in devices if x[0] == Device.KEY]
    locks = [x[1] for x in devices if x[0] == Device.LOCK]
    return keys, locks

def find_matches(keys:  list[list[int]], locks: list[list[int]]) -> list[tuple[int, int]]:
    matches = list()
    for i, key in enumerate(keys):
        for j, lock in enumerate(locks):
            matched = True
            for column in range(5):
                if key[column] + lock[column] > 5:
                    matched = False
                    break
            if matched:
                matches.append((i, j))
    return matches

if __name__ == "__main__":
    lock1 = """#####
.####
.####
.####
.#.#.
.#...
.....""".split("\n")

    key1 = """.....
#....
#....
#...#
#.#.#
#.###
#####""".split("\n")
    # print(ex1)
    # print(parse(key1))

    data = load_data("input.txt")
    k, l = separate(data)

    matches = find_matches(k, l)
    print(len(matches))
    # print(data)
    # print(k)
    # print(l)
