def load():
    database = []
    with open('retail_dataset/retail.txt', 'r') as file:
        database = [list(line.rstrip()) for line in file]
    return database

if __name__ == '__main__':
    db = load()
    for sequence in db:
        [print(item, end="") for item in sequence]
        print()