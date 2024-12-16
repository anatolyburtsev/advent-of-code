from math import gcd


# Extended Euclidean Algorithm to find one solution
def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x1, y1 = extended_gcd(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    return g, x, y


# Solve a single Diophantine equation a*x + b*y = c
def solve_diophantine(a, b, c):
    g, x0, y0 = extended_gcd(abs(a), abs(b))
    if c % g != 0:  # No solution exists
        return None
    # Scale the particular solution by c / g
    x0 *= c // g
    y0 *= c // g
    if a < 0: x0 = -x0
    if b < 0: y0 = -y0
    # General solution: x = x0 + k * (b / g), y = y0 - k * (a / g)
    return g, x0, y0


# Find all positive integer solutions
def find_positive_solutions(a1, b1, c1, a2, b2, c2):
    solutions = []
    g1, x1, y1 = solve_diophantine(a1, b1, c1)
    g2, x2, y2 = solve_diophantine(a2, b2, c2)

    if g1 is None or g2 is None:
        return solutions  # No solutions

    # Iterate over k1, k2 ranges to find valid solutions
    for k1 in range(-1000000, 1000000):  # Adjust range as needed
        x = x1 + k1 * b1 // g1
        y = y1 - k1 * a1 // g1
        if x > 0 and y > 0:  # Positive solution
            # Check against second equation
            if a2 * x + b2 * y == c2:
                solutions.append((x, y))
    return solutions

if __name__ == "__main__":
    # inp = (26, 66, 67, 21, 10000000012748, 10000000012176)
    # print(find_x0(*inp))
    # print(find_positive_solutions(*inp))

    solutions = find_positive_solutions(94, 34, 22, 67, 8400, 5400)
    print("Solutions:", solutions)