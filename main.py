from itertools import chain
from copy import copy, deepcopy


database = [
    [list("ab"), list("c"), list("a")],
    [list("ab"), list("b"), list("c")],
    [list("b"), list("c"), list("d")],
    [list("b"), list("ab"), list("c")],
]
minsup = 3

database = [
    [list("ab"), list("c"), list("a")],
    [list("a"), list("bc")],
]
minsup = 2


def check_frequent(database, pattern):  # TODO
    support = 0


def prefixspan(database, min_support, pattern=None, level=0, debug=False):
    if pattern == None:
        pattern = []
    # Count the occurrence of items in the sequences
    item_counts = {}
    for sequence in database:
        elements = set(chain(*sequence))
        for item in elements:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1

    # Filter items based on minimum support
    frequent_items = [
        item for item, count in item_counts.items() if count >= min_support
    ]
    # Generate frequent sequential patterns
    frequent_patterns = []
    for item in frequent_items:
        if debug:
            print(f"Currently at level {level} PS with database:")
            [print(d) for d in database]
            print(
                f'minsup = {min_support}, pattern so far is: {"" if pattern else "None"}',
                end=" ",
            )
            [print(p, end=" ") for p in pattern]
            print()
            print(f"Found {len(frequent_items)} frequent items:", end=" ")
            [print(k, end=" ") for k in frequent_items]
            print()
            print(f"Processing item {item}")
            print()

        projected_database = []
        for sequence in database:
            projected_sequence = []
            for i, seq_item in enumerate(sequence):
                if item in seq_item:
                    projected_sequence = deepcopy(sequence[i:])
                    while projected_sequence[0] and projected_sequence[0][0] != item:
                        projected_sequence[0] = projected_sequence[0][1:]
                    projected_sequence[0] = projected_sequence[0][1:]
                    break
            if projected_sequence:
                projected_database.append(projected_sequence)
        if debug:
            print(f"Found projected database:")
            [print(d) for d in projected_database]
            print()

        # Append new item as a new transaction:
        new_pattern = copy(pattern) + [set([item])]
        # CHECK TODO
        frequent_patterns.append(new_pattern)

        if projected_database:
            if debug:
                print(f"Going deeper with new NEW pattern {new_pattern}")
            frequent_patterns.extend(
                prefixspan(
                    projected_database, min_support, new_pattern, level + 1, debug
                )
            )
        # Insert new item into last transaction:
        if pattern and pattern[-1] and not item in pattern[-1]:
            new_pattern = copy(pattern)
            new_pattern[-1].add(item)
            # CHECK TODO
            frequent_patterns.append(new_pattern)

            if projected_database:
                if debug:
                    print(f"Going deeper with new LAST pattern {new_pattern}")
                frequent_patterns.extend(
                    prefixspan(
                        projected_database, min_support, new_pattern, level + 1, debug
                    )
                )
    if debug and level:
        print(f"Going back to level {level-1}")
    if debug and not level:
        print(f"END")
    return frequent_patterns


if __name__ == "__main__":
    p = prefixspan(database, minsup, debug=False)
    [print(pp) for pp in p]
    print()
