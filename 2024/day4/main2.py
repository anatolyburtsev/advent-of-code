from typing import List, Tuple


def get_line_candidates(data: List[str], v: int, h: int) -> list[str]:
    v_size = len(data)
    h_size = len(data[0])

    candidates = [
        data[v][h:h+4] if h + 4 <= h_size else None, # right
        data[v][h-3:h+1][::-1] if h - 3 >= 0 else None, # left
        "".join([data[v - i][h] for i in range(4) if v - 3 >= 0]), #up
        "".join([data[v + i][h] for i in range(4) if v + 3 < v_size]),  # down
        "".join([data[v+i][h+i] for i in range(4) if v+3 < v_size and h + 3 < h_size]), # diag right down
        "".join([data[v - i][h + i] for i in range(4) if v - 3 >=0 and h + 3 < h_size]),  # diag right down
        "".join([data[v + i][h - i] for i in range(4) if v + 3 < v_size and h - 3 >= 0]),  # diag right down
        "".join([data[v - i][h - i] for i in range(4) if v - 3 >= 0 and h - 3 >= 0]),  # diag right down
    ]

    return [x for x in candidates if x]

def get_x_candidates(data: List[str], v: int, h: int) -> List[str]:
    v_size = len(data)
    h_size = len(data[0])

    if 1 <= v < v_size - 1 and 1 <= h < h_size - 1:
        f1 = data[v-1][h-1]
        f2 = data[v-1][h+1]
        f3 = data[v][h]
        f4 = data[v+1][h-1]
        f5 = data[v+1][h+1]
        return [
            f"{f1}{f2}{f3}{f4}{f5}",
            f"{f2}{f5}{f3}{f1}{f4}",
            f"{f5}{f4}{f3}{f2}{f1}",
            f"{f4}{f1}{f3}{f5}{f2}",
        ]
    return ""


def find_x_positions(data: List[str], center: str = "X") -> List[Tuple]:
    return [(v,h)
    for v in range(len(data))
        for h in range(len(data[0])) if data[v][h] == center]



def calc_xmases(data: List[str]) -> int:
    x_positions = find_x_positions(data)
    result = 0
    for pos in x_positions:
        candidates = get_line_candidates(data, pos[0], pos[1])
        result += len(list(filter(lambda x: x == "XMAS", candidates)))
    return result


def calc_x_mases(data: List[str]) -> int:
    a_positions = find_x_positions(data, "A")
    result = 0
    for pos in a_positions:
        for candidate in get_x_candidates(data, pos[0], pos[1]):
            if candidate == "MSAMS":
                result += 1
    return result


if __name__ == "__main__":
    data = []
    with open("input.txt", 'r') as f:
        [data.append(line.strip()) for line in f.readlines()]

    print("\n".join(data))

    # print(get_candidates(data, 3, 9))
    # print(find_x_positions(data))
    # print(calc_xmases(data))
    # print(get_x_candidate(data, 1, 1))
    print(calc_x_mases(data))