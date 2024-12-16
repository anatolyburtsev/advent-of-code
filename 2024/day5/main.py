from functools import cmp_to_key
from typing import Tuple, List


def is_report_valid(report: List[str], rules: List[Tuple]) -> bool:
    number_ids = {v: k for (k, v) in enumerate(report)}

    for rule in rules:
        if rule[0] in number_ids and rule[1] in number_ids and number_ids[rule[0]] > number_ids[rule[1]]:
            return False
    return True


def fix_report_once(report: List[str], rules: List[Tuple]) -> Tuple[List[str], bool]:
    fixed_report = report[:]
    number_ids = {v: k for (k, v) in enumerate(report)}
    changes_made = False

    for rule in rules:
        left_num, right_num = rule
        if left_num not in number_ids or right_num not in number_ids:
            continue
        left_num_idx = number_ids[left_num]
        right_num_idx = number_ids[right_num]
        if left_num_idx > right_num_idx:
            fixed_report[left_num_idx] = right_num
            fixed_report[right_num_idx] = left_num
            changes_made = True

    print("AAA")
    print(f"{fixed_report}")
    return fixed_report, changes_made


from collections import defaultdict, deque


def fix_report2(report: List[str], rules: List[Tuple]) -> List[str]:
    # Create a dependency graph
    graph = defaultdict(list)
    in_degree = defaultdict(int)

    # Build graph for pages in the report only
    pages_set = set(report)
    for a, b in rules:
        if a in pages_set and b in pages_set:
            graph[a].append(b)
            in_degree[b] += 1

    # Perform topological sort
    queue = deque([node for node in report if in_degree[node] == 0])
    sorted_report = []

    while queue:
        node = queue.popleft()
        sorted_report.append(node)
        for neighbor in graph[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    # Verify all pages are sorted
    if len(sorted_report) != len(report):
        raise ValueError("Cycle detected in report dependencies")

    return sorted_report

def fix_report3(report: List[str], rules: List[Tuple]) -> List[str]:

    def compare(x, y):
        # print(f"{x} {y} {rules}")
        for rule in rules:
            if x == rule[0] and y == rule[1]:
                return 1
            elif x == rule[1] and y == rule[0]:
                return -1
        return 0
    return sorted(report, key=cmp_to_key(compare), reverse=True)

def fix_report(report: List[str], rules: List[Tuple]) -> List[str]:
    changes_made = True
    while changes_made:
        report, changes_made = fix_report_once(report[:], rules)
    return report


def process_report(report: List[str], rules: List[Tuple]) -> int:
    return int(report[len(report) // 2]) if is_report_valid(report, rules) else 0


def find_mid_valid_reports(reports: List[List[int]], rules: List[Tuple]) -> int:
    return sum([process_report(report, rules) for report in reports]
               )


def find_min_fixed_reports(reports: List[List[int]], rules: List[List[str]]) -> int:
    invalid_reports = [r for r in reports if not is_report_valid(r, rules)]
    # for report in reports:
    #     fr = fix_report3(report, rules)
        # fr1 = fix_report(report, rules)
        # fr2 = fix_report2(report, rules)
        # if fr1 != fr2:
        #     print(f"{fr1}")
        #     print(f"{fr2}")
        #     print("----------------")

    fixed_reports = [fix_report3(report, rules) for report in invalid_reports]
    print([r for r in fixed_reports if not is_report_valid(r, rules)])

    return sum(
        [int(r[len(r) // 2]) for r in fixed_reports]
    )


if __name__ == "__main__":
    rules: List[List[str]] = []
    reports: List[List[str]] = []

    with open("input.txt", "r") as f:
        for line in f.readlines():
            if "|" in line:
                a, b = line.split("|")
                rules.append((a, b.strip()))
            elif line == "\n":
                continue
            else:
                report = [x.strip() for x in line.split(",")]
                reports.append(report)

    # print(fix_report3(["61","13","29"], rules))
    # print(rules)
    # print(reports[1])
    # print(is_report_valid(reports[1], rules))
    # print(fix_report(reports[1], rules))
    print(find_min_fixed_reports(reports, rules))
    # print(find_mid_valid_reports(reports, rules))
    # print(process_report(reports[0], rules))
    #
    # rules = [
    #     (5, 3),
    #     (1, 3),
    #     (4, 2)
    # ]
    #
    # reports = [
    #     [1, 2, 3, 4, 5],
    #     [1, 2, 5, 4, 3],
    #     [1, 4, 5, 2, 3]
    # ]
    #
    # print(is_report_valid(reports[0], rules))
    # print(is_report_valid(reports[1], rules))
    # print(is_report_valid(reports[2], rules))
