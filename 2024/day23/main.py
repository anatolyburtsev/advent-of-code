from collections import defaultdict
from typing import List, Tuple

Edge = tuple[str, str]
Connections = dict[str, list[str]]

def load_data(filename) -> list[Edge]:
    with open(filename, "r") as f:
        lines = [x.strip() for x in f.readlines()]
        return [tuple(x.split("-")) for x in lines]


def find_triplets(connection: Edge, connections: Connections) -> list[tuple[str, ...]]:
    a, b = connection
    all_nodes = connections.keys()
    result = []
    for c in all_nodes:
        if c in [a, b]:
            continue
        if a in connections[c] and b in connections[c]:
            result.append(tuple(sorted([a, b, c])))
    return result


def extend_click(click: tuple[str], connections: Connections) -> list[tuple[str, ...]] | None:
    common_nodes = set(connections[click[0]])
    for node in click[1:]:
        common_nodes &= set(connections[node])
    if not common_nodes:
        return None

    return [tuple(sorted(list(click) + [extra_node])) for extra_node in common_nodes]

def extend_clicks(clicks: list[tuple[str]], connections: Connections) -> list[tuple[str, ...]]:
    print(f"Start extending {len(clicks)} clicks of size {len(clicks[0])}")
    extended_clicks = []
    for click in clicks:
        extended = extend_click(click, connections)
        if extended is not None:
            extended_clicks.extend(extended)
    extended_clicks = list(set(extended_clicks))
    if len(extended_clicks) == 1:
        print(",".join(sorted(extended_clicks[0])))
    print(f"Extended to {len(extended_clicks)} clicks of size {len(extended_clicks[0])}")
    return extended_clicks


if __name__ == "__main__":
    data = load_data("input.txt")
    # data = load_data("test_input.txt")

    connections = defaultdict(list)
    for a, b in data:
        connections[a].append(b)
        connections[b].append(a)

    interconnected_triplets: set[tuple[str, str, str]] = set()
    for connection in data:
        if (connected_triplet := find_triplets(connection, connections)) is not None:
            interconnected_triplets |= set(connected_triplet)

    print(len(interconnected_triplets))

    klins = list(interconnected_triplets)
    while klins:
        klins = extend_clicks(klins, connections)


