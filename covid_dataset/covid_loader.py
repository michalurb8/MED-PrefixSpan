n = 8

def load(show=False):
    database = []
    with open("covid_dataset/covid.txt", "r") as file:
        joined = "".join([line.rstrip() for line in file])
        database = [list(joined[i : i + n]) for i in range(0, len(joined), n)]
    if show:
        for sequence in database:
            [print(item, end="") for item in sequence]
            print()
    database = database[:-1]
    return database


if __name__ == "__main__":
    db = load()