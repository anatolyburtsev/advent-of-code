import json
import time
from functools import cache, wraps
from pickletools import long1
from typing import List, Dict, Tuple


def timeit(func):
    @wraps(func)
    def timeit_wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f'Function {func.__name__}{args} {kwargs} Took {total_time:.4f} seconds')
        return result

    return timeit_wrapper


@cache
def evolve_stone(stone: int) -> List[int]:
    match stone:
        case 0:
            return [1]
        case n if len(str(n)) % 2 == 0:
            mid = len(str(n)) // 2
            return [int(str(n)[:mid]), int(str(n)[mid:])]
        case _:
            return [stone * 2024]


LedgerType = Dict[Tuple[int, int], int]


def build_small_ledger() -> LedgerType:
    ledger = {}
    for stone in range(10, 100):
        print(f"{stone=}")
        stones = [stone]
        for epoch in range(39):
            stones = [
                evolved_stone for stone in stones for evolved_stone in evolve_stone(stone)
            ]
            ledger[(stone, epoch)] = len(stones)

    return ledger


def build_long_ledger(ledger: LedgerType) -> LedgerType:
    MAX_ITER = 76
    for stone in range(100):
        print(f"{stone=}")
        for cur_max_epoch in range(39, MAX_ITER):
            stones = [stone]
            stones_count = 0
            for epoch in range(cur_max_epoch):
                remain_epochs = cur_max_epoch - epoch
                new_stones = []
                for st in stones:
                    if (st, remain_epochs) in ledger:
                        stones_count += ledger[(st, remain_epochs)]
                    else:
                        for evolved_stone in evolve_stone(st):
                            new_stones.append(evolved_stone)

                stones = new_stones[:]

            if (stone, cur_max_epoch) not in ledger:
                ledger[(stone, cur_max_epoch)] = len(stones) + stones_count
                # print(f"adding new value: at {stone=}, {cur_max_epoch=}, equal to {len(stones) + stones_count}")
            else:
                print(f"already exists: at {stone=}, {cur_max_epoch=}")

    return ledger


def save_ledger(ledger: LedgerType, export_filename: str):
    with open(export_filename, "w") as f:
        string_ledger = {str(k): v for k, v in ledger.items()}
        json.dump(string_ledger, f)


def load_ledger(filename: str) -> LedgerType:
    with open(filename, "r") as f:
        ledger = json.load(f)
    return {eval(k): v for k, v in ledger.items()}

def merge_ledgers(ledger1: LedgerType, ledger2: LedgerType) -> LedgerType:
    merged_ledger = ledger1.copy()
    for k, v in ledger2.items():
        if k not in merged_ledger:
            merged_ledger[k] = v
    return merged_ledger


def evolve_stone_with_ledger(ledger: LedgerType, stones: List[int]) -> int:
    max_epoch = 75
    stones_count = 0
    for epoch in range(max_epoch):
        remain_epochs = max_epoch - epoch - 1
        new_stones = []
        for st in stones:
            if (st, remain_epochs) in ledger:
                stones_count += ledger[(st, remain_epochs)]
            else:
                for evolved_stone in evolve_stone(st):
                    new_stones.append(evolved_stone)

        stones = new_stones[:]
        # print(f"{epoch=}, len: {stones_count + len(stones)} {stones=}, {stones_count=}")
    return len(stones) + stones_count

def evolve_stones(stones: List[int]) -> List[int]:
    ITER_LIMIT = 25
    for i in range(ITER_LIMIT):
        stones = [
            evolved_stone for stone in stones for evolved_stone in evolve_stone(stone)
        ]
        print(f"{i}, len: {len(stones)}, stone: {stones}")
        # print(" ".join([str(x) for x in stones]))
    return stones


if __name__ == "__main__":
    # data = [125, 17]
    data = [2, 72, 8949, 0, 981038, 86311, 246, 7636740]
    # data = [246]
    # data = [2, 0, 7, 8, 4] # 123572
    # data = [0]
    # print(len(evolve_stones(data)))
    # for i in data:
    #     print(f"{i=}, {len(evolve_stones([i]))}")

    ledger = load_ledger("long_ledger_100.json")
    print(evolve_stone_with_ledger(ledger, data))

    # small_ledger_10 = load_ledger("small_ledger.json")
    # small_ledger_100 = load_ledger("small_ledger_10_100.json")
    # ledger = merge_ledgers(small_ledger_10, small_ledger_100)
    # long_ledger_100 = build_long_ledger(ledger)
    # save_ledger(long_ledger_100, "long_ledger_100.json")

    # print(long_ledger_100)

    # print(sum(
    #     small_ledger[(n, 25)] for n in data
    # ))
