from itertools import chain
n = 8

def load():
    database = []
    with open('covid_dataset/covid.txt', 'r') as file:
        joined = "".join([line.rstrip() for line in file])
        database = [list(joined[i:i+n]) for i in range(0, len(joined), n)]
    return database

if __name__ == '__main__':
    db = load()
    for sequence in db:
        [print(item, end="") for item in sequence]
        print()