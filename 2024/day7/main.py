from typing import List

def convolute(s: int, acc: int, numbers: List[int]) -> int:
    if not numbers:
        return s == acc
    else:
        return (convolute(s, acc + numbers[0], numbers[1:]) or convolute(s, acc * numbers[0], numbers[1:]) or
                convolute(s, int(str(acc) + str(numbers[0])), numbers[1:]))

if __name__ == "__main__":
    total_sum = 0
    with open("input.txt", 'r') as f:
        for line in f.readlines():
            s, numbers_str = line.split(':')
            s = int(s)
            numbers = [int(n.strip()) for n in numbers_str.split()]
            if convolute(s, numbers[0], numbers[1:]):
                total_sum = total_sum + s
    print(total_sum)