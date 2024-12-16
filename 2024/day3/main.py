import re
from itertools import accumulate
from typing import List
from unicodedata import is_normalized

mul_regex = re.compile("mul\(\d{1,3},\d{1,3}\)")
mul2_regex = re.compile("mul\(\d{1,3},\d{1,3}\)|do\(\)|don\'t\(\)")

def exec_mul(mul_string: str) -> int:
    l, r = mul_string.replace("mul(", "").replace(")", "").split(",")
    return int(l) * int(r)

def filter_enables_muls(expressions: List[str]) -> List[str]:
    is_enabled = True
    result = []
    for expr in expressions:
        match expr:
            case 'don\'t()':
                is_enabled = False
            case 'do()':
                is_enabled = True
            case _:
                if is_enabled:
                    result.append(expr)
    return result


def filter_enables_muls2(expressions: List[str]) -> List[str]:
    def is_enabled(expr: str, current_state: bool) -> bool:
        match expr:
            case "do()":
                return True
            case "don't()":
                return False
            case _:
                return current_state

    states = accumulate(
        expressions, lambda current_value, expr: is_enabled(expr, current_value), initial=True
    )

    return [expr for (expr, state) in zip(expressions, states) if state and expr not in {"do()", "don't()"}]

if __name__ == "__main__":
    with open("test_input2.txt", "r") as f:
        # with open("input.txt", "r") as f:
            text = f.readline()

    exprs = mul2_regex.findall(text)
    enabled_muls = (filter_enables_muls2(exprs))
    print(sum(exec_mul(mul_exp) for mul_exp in enabled_muls))
