from collections import Counter

def task1(first_list, second_list):
    return sum([abs(a - b) for a, b in zip(first_list, second_list)])


if __name__ == "__main__":
    with open("input.txt", 'r') as f:
        first_list = []
        second_list = []
        for line in f.readlines():
            l, r = line.split("   ")
            first_list.append(int(l))
            second_list.append(int(r))

    # second_list = sorted(second_list)

    print(first_list, second_list)

    cnt = Counter(second_list)
    print(cnt)

    print(
        sum([n * cnt[n] for n in first_list])
    )