from typing import List


def count_in_line(line: str, search_term: str) -> int:
    # line - "ABCDE" len - 5
    # searchTerm - "CDE" - len 3
    # loop from 0 to 2
    # print(f"{line=}")
    counter = 0
    for start_idx in range(len(line) - len(search_term) + 1):
        if line[start_idx:start_idx + len(search_term)] == search_term:
            counter += 1
    # print(f"{counter=}")
    return counter

def count_horizontal(data: List[str], searchTerm: str) -> int:
    return sum(
        [count_in_line(line, searchTerm) for line in data]
    )

def __get_vertical_slice(data: List[str], idx: int) -> str:
    return "".join([line[idx] for line in data])

def __get_left_diagonal_slice(data: List[str], idx: int) -> str:
#     ABC
#     DEF
#     i = 0 -> "D" (1, 0)
#     i = 1 -> "AE" (0, 0)
#     i = 2 -> "BF" (0, 1)
#     i = 3 -> "C"  (0, 2)
    v_size = len(data)
    h_size = len(data[0])
    (i, j) = (max(0, v_size - idx - 1), max(0, min(h_size, idx - h_size + 2)))
    result = []
    while i < v_size and j < h_size:
        result.append(data[i][j])
        i += 1
        j += 1
    return "".join(result)


def __get_right_diagonal_slice(data: List[str], idx: int) -> str:
#     ABC
#     DEF
#     i = 0 -> "A" (0, 0)
#     i = 1 -> "BD" (0, 1)
#     i = 2 -> "CE" (0, 2)
#     i = 3 -> "F"  (1, 2)
    v_size = len(data) # 2
    h_size = len(data[0]) # 3
    (i, j) = (max(0, idx - h_size + 1), min(h_size - 1, idx))
    result = []
    while 0 <= i < v_size and 0 <= j:
        result.append(data[i][j])
        i += 1
        j -= 1
    return "".join(result)


def count_vertical(data: List[str], searchTerm: str) -> int:
    return sum(
        [count_in_line(
            __get_vertical_slice(data, idx),
            searchTerm
        )  for idx in range(len(data))]
    )

def count_left_horizontal(data: List[str], searchTerm: str) -> int:
    return sum(
        [count_in_line(
            __get_left_diagonal_slice(data, idx),
            searchTerm
        ) for idx in range(len(data) + len(data[0]) - 1)]
    )

def count_right_horizontal(data: List[str], searchTerm: str) -> int:
    return sum(
        [count_in_line(
            __get_right_diagonal_slice(data, idx),
            searchTerm
        ) for idx in range(len(data) + len(data[0]) - 1)]
    )


def find_word(data: List[str], search_term: str) -> int:
    vc = count_vertical(data, search_term)
    hc = count_horizontal(data, search_term)
    lhc =  count_left_horizontal(data, search_term)
    rhc = count_right_horizontal(data, search_term)
    print(f"{vc=} {hc=} {lhc=} {rhc=}")
    return sum([vc, hc, lhc, rhc ])

if __name__ == "__main__":
    data = []
    with open("test_input.txt", 'r') as f:
        [data.append(line.strip()) for line in f.readlines()]
    #
    # print(data)
    # print(count_horizontal(data, "XMAS"))
    # print(count_horizontal(data, "SAMX"))
    # print(count_vertical(data, "XMAS"))
    # print(count_vertical(data, "SAMX"))
    # print(count_left_horizontal(data, "XMAS"))
    # print(count_left_horizontal(data, "SAMX"))
    # print(__get_left_diagonal_slice(data, 0))
    # print(__get_left_diagonal_slice(data, 1))
    # print(__get_left_diagonal_slice(data, 2))
    # print(__get_left_diagonal_slice(data, 3))
    # print(__get_left_diagonal_slice(data, 4))
    # print(__get_right_diagonal_slice(["ABC", "DEF"], 0))
    # print(__get_right_diagonal_slice(["ABC", "DEF"], 1))
    # print(__get_right_diagonal_slice(["ABC", "DEF"], 2))
    # print(__get_right_diagonal_slice(["ABC", "DEF"], 3))
    print(a := find_word(data, "XMAS"))
    print(b := find_word(data, "SAMX"))
    print(a + b)
