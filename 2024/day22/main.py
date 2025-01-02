import json
from collections import defaultdict

from tqdm import tqdm
from multiprocessing import Pool
from functools import partial


def read_data(filename) -> list[int]:
    with open(filename, "r") as f:
        return [int(line.strip()) for line in f.readlines()]


def mix(a: int, b: int) -> int:
    return a ^ b


def prune(x: int) -> int:
    return x % 16777216


def evolve_secret(x: int) -> int:
    v1 = x * 64
    x = mix(v1, x)
    x = prune(x)
    v4 = x // 32
    x = mix(v4, x)
    x = prune(x)
    v5 = x * 2048
    x = mix(v5, x)
    x = prune(x)
    return x


def evolve_n_times(x: int, n: int) -> int:
    for _ in range(n):
        x = evolve_secret(x)
    return x


def evolve_multi_n_times(xs: list[int], n: int) -> list[int]:
    return [evolve_n_times(x, n) for x in xs]


def evolve_n_times_v2(x: int, n: int) -> tuple[list[int], list[int]]:
    result = []
    diffs = [None]
    for _ in range(n):
        result.append(x % 10)
        x = evolve_secret(x)
    for i in range(len(result) - 1):
        diffs.append(result[i + 1] - result[i])
    return result, diffs

Prices = list[int]
PriceDiffs = list[int]
PriceData = tuple[Prices, PriceDiffs]

def load_data(filename) -> dict[int, PriceData]:
    with open(filename, "r") as f:
        return json.load(f)

def find_price(data: PriceData, pattern: list[int]) -> int:
    prices, diffs = data
    for i in range(len(prices) - len(pattern)):
        if diffs[i:i+len(pattern)] == pattern:
            return prices[i+len(pattern) - 1]


def calculate_sum(data: list[int], calc_data: PriceData, seq: list[int]) -> int:
    s = 0
    for i in data:
        x = find_price(calc_data[str(i)], seq)
        if x:
            s += x
    return s

def process_sequence(seq, data, calc_data, current_max=0):
    s = calculate_sum(data, calc_data, seq)
    if s > current_max:
        return (s, seq)
    return (current_max, None)


def parallel_process(seqs, data, calc_data, num_processes=None):
    max_sum = 0
    max_sum_seq = None

    # Create a partial function with fixed arguments
    process_func = partial(process_sequence, data=data, calc_data=calc_data, current_max=max_sum)

    # Create a process pool
    with Pool(processes=num_processes) as pool:
        # Process sequences in parallel with progress bar
        for result in tqdm(pool.imap(process_func, seqs), total=len(seqs), desc="Processing"):
            current_sum, current_seq = result
            if current_sum > max_sum:
                max_sum = current_sum
                max_sum_seq = current_seq
                print(f"current: {max_sum=}, {max_sum_seq=}")

    return max_sum, max_sum_seq

def merge(d1: dict, d2: dict) -> dict:
    merged = {}
    for key in set(d1) | set(d2):
        merged[key] = d1.get(key, 0) + d2.get(key, 0)
    return merged

if __name__ == "__main__":
    # N = 2000
    # result = {}
    # for n in data:
    #     cost, diffs = evolve_n_times_v2(n, N)
    #     result[n] = (cost, diffs)
    #
    # with open("data.json", "w") as f:
    #     json.dump(result, f)

    data = read_data("input.txt")
    calc_data = load_data("data.json")
    # data = [1, 2, 3, 2024]
    # calc_data = load_data("test_data.json")

    # print(calculate_sum(data, calc_data, [-2,1,-1,3]))




    price_sums = dict()

    total = len(calc_data)
    j = 0
    for (prices, diffs) in calc_data.values():
        print(f"{j}/{total}")
        merchant_dict = dict()
        j += 1
        for i in range(len(prices) - 4):
            merchant_dict[tuple(diffs[i:i+4])] = prices[i+3]

        price_sums = merge(price_sums, merchant_dict)

    max_v = -1
    max_k = None
    for k,v in price_sums.items():
        if v > max_v:
            max_v = v
            max_k = k
            print(f"upd: {max_k=} {max_v=}")
    print(f"final: {max_k=} {max_v=}")

    # verify
    print(calculate_sum(data, calc_data, [2, 0, -1, 2]))

