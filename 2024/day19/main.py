import time
from functools import lru_cache


def parse(filename):
    with open(filename) as f:
        towels = f.readline().strip().split(", ")
        f.readline()
        designs = [x.strip() for x in f.readlines()]
        return towels, designs


towels, designs = parse("input.txt")
# towels, designs = parse("test_input.txt")


def find_starting_towels(design: str):
    return [towel for towel in towels if design.startswith(towel)]

@lru_cache(2048)
def can_create_design(design) -> int:
    # print(f"{design=}")
    if not design:
        return True
    starting_towels = find_starting_towels(design)
    return sum([can_create_design(design[len(towel):]) for towel in starting_towels])


if __name__ == "__main__":
    start_time = time.time()
    print(f"{towels=}")
    # print(f"{designs=}")
    print(can_create_design(designs[0]))

    total = 0
    for design in designs:
        print(f"Processing design: {design} at {time.strftime('%H:%M:%S')}")
        total += can_create_design(design)

    print(f"Total: {total}")
    print(f"Total execution time: {time.time() - start_time:.2f} seconds")
    # print(sum([can_create_design(towels, design) for design in designs]))
