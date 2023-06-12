from itertools import chain
from copy import deepcopy
from typing import List
import numpy as np

def getSupportNew(database: List, item, new: bool, debug: bool = False) -> int:
    support = 0
    for sequence in database:
        for seqItem in sequence[new:]:
            if item in seqItem:
                support += 1
                break
    if debug:
        print(f"Calculated support is {support} for item {item}, NEW item, database:")
        [print(d) for d in database]
        print()
    return support


def getSupportLast(database: List, item, debug: bool = False) -> int:
    support = 0
    for sequence in database:
        if item in sequence[0]:
            support += 1
    if debug:
        print(f"Calculated support is {support} for item {item}, LAST item, database:")
        [print(d) for d in database]
        print()

    return support


def prefixspan(
    database: List,
    minsup: int,
    pattern: List = None,
    level: int = 0,
    debug: bool = False,
) -> List:
    if pattern == None:
        pattern = []
    # Count the occurrence of items in the sequences
    itemCounts = {}
    for sequence in database:
        elements = np.unique(list(chain(*sequence)))
        for item in elements:
            if item in itemCounts:
                itemCounts[item] += 1
            else:
                itemCounts[item] = 1

    # Filter items based on minimum support
    frequentItems = [item for item, count in itemCounts.items() if count >= minsup]
    # Generate frequent sequential patterns
    frequentPatterns = []
    for item in frequentItems:
        if debug:
            print(f"Currently at level {level} PS with database:")
            [print(d) for d in database]
            print(
                f'minsup = {minsup}, pattern so far is: {"" if pattern else "None"}',
                end=" ",
            )
            [print(p, end=" ") for p in pattern]
            print()
            print(f"Found {len(frequentItems)} frequent items:", end=" ")
            [print(k, end=" ") for k in frequentItems]
            print()
            print(f"Processing item {item}")
            print()

        newBranch = False
        lastBranch = False

        # Append new item as a new transaction:
        newPattern = deepcopy(pattern) + [[item]]
        newBranch = getSupportNew(database, item, level > 0, debug) >= minsup

        # Insert new item into last transaction:
        if pattern and pattern[-1] and not item in pattern[-1]:
            lastPattern = deepcopy(pattern)
            lastPattern[-1].append(item)
            lastBranch = getSupportLast(database, item, debug) >= minsup

        projectedDatabase = []
        if newBranch or lastBranch:
            for sequence in database:
                projectedSequence = []
                for i, seqItem in enumerate(sequence):
                    if item in seqItem:
                        projectedSequence = deepcopy(sequence[i:])
                        while projectedSequence[0] and projectedSequence[0][0] != item:
                            projectedSequence[0] = projectedSequence[0][1:]
                        projectedSequence[0] = projectedSequence[0][1:]
                        break
                if projectedSequence:
                    projectedDatabase.append(projectedSequence)
            if debug:
                print(f"Found projected database:")
                [print(d) for d in projectedDatabase]
                print()

        if newBranch:
            frequentPatterns.append(newPattern)
            if debug:
                print(f"Adding pattern {newPattern}")
            if projectedDatabase:
                if debug:
                    print(f"Going deeper with new NEW pattern {newPattern}")
                frequentPatterns.extend(
                    prefixspan(projectedDatabase, minsup, newPattern, level + 1, debug)
                )

        if lastBranch:
            frequentPatterns.append(lastPattern)
            if debug:
                print(f"Adding pattern {lastPattern}")

            if projectedDatabase:
                if debug:
                    print(f"Going deeper with new LAST pattern {lastPattern}")
                frequentPatterns.extend(
                    prefixspan(projectedDatabase, minsup, lastPattern, level + 1, debug)
                )



    if debug and level:
        print(f"Going back to level {level-1}")
    if debug and not level:
        print(f"END")
    return frequentPatterns

if __name__ == "__main__":
    database = [
        [list("ab"), list("c"), list("a")],
        [list("ab"), list("b"), list("c")],
        [list("b"), list("c"), list("d")],
        [list("b"), list("ab"), list("c")],
    ]
    minsup = 3
    p = prefixspan(database, minsup)
    [print(pp) for pp in p]