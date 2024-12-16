from itertools import zip_longest
from typing import List
import numpy as np

# def is_same_direction(report:List[int]) -> bool:

def is_report_safe(report: List[int]) -> bool:
    diffs = [a - b for [a, b] in zip(report, report[1:])]
    signs = [np.sign(x) for x in diffs]
    max_abs_diff = max([abs(x) for x in diffs])
    return len(set(signs)) == 1 and signs[0] != 0 and max_abs_diff <= 3

def is_report_dampener_safe(report: List[int]) -> bool:
    if is_report_safe(report):
        return True
    for drop_index in range(len(report)):
        shortened_report = report[:drop_index] + report[drop_index + 1:]
        if is_report_safe(shortened_report):
            return True

    return False

if __name__ == "__main__":
    safe_reports = 0
    with open("input.txt", "r") as f:
        for line in f.readlines():
            report = [int(x) for x in line.split(" ")]
            if is_report_dampener_safe(report):
                safe_reports += 1

    print(safe_reports)
