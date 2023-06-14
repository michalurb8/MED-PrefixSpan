from itertools import groupby


def load(show=False):
    database = []
    with open("retail_dataset/retail.txt", "r") as file:
        for rawLine in file:
            stripLine = rawLine.strip()[:-3].split(" ")
            splitLine = [
                list([int(element) for element in transaction])
                for isDelimeter, transaction in groupby(
                    stripLine, lambda delimeter: delimeter == "-1"
                )
                if not isDelimeter
            ]
            database.append(splitLine)
    if show:
        for sequence in database:
            for transaction in sequence:
                for item in transaction:
                    print(item, end=" ")
                print()
            print()
    return database


if __name__ == "__main__":
    db = load(True)
