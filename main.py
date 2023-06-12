import argparse

from src.PS import prefixspan
from covid_dataset import covid_loader
from retail_dataset import retail_loader

if __name__ == "__main__":
    db = covid_loader.load()
    result = prefixspan(db, 1000)
    for d in db:
        print(d)
    print()
    for rule in result:
        print(rule)
    print(len(result))