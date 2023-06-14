from src.PS import prefixspan
from covid_dataset import covid_loader
from retail_dataset import retail_loader

import matplotlib.pyplot as plt
from time import perf_counter

def singleRun(dataset, minsup, logging):
    if dataset == 'covid':
        db = covid_loader.load()
        ruleSet = prefixspan(db, minsup, debug=logging)
        for rule in ruleSet:
            print(rule)
    elif dataset == 'retail':
        db = retail_loader.load()
        ruleSet = prefixspan(db, minsup, debug=logging)
        for rule in ruleSet:
            print(rule)
    else:
        raise Exception("ERROR")


def graphMinSup(minsups, times, ruleCounts, title):
    plt.cla()
    plt.clf()
    plt.scatter(minsups, times)
    plt.title(title)
    plt.xlabel("Minimum Support")
    plt.ylabel("Time elapsed (s)")
    plt.show()

    plt.cla()
    plt.clf()
    plt.scatter(minsups, ruleCounts)
    plt.title(title)
    plt.xlabel("Minimum Support")
    plt.ylabel("Number of rules found")
    plt.show()

    plt.cla()
    plt.clf()
    plt.scatter(ruleCounts, times)
    plt.title(title)
    plt.xlabel("Number of rules found")
    plt.ylabel("Time elapsed (s)")
    plt.show()

def graphSize(sizes, times, ruleCounts, title):
    plt.cla()
    plt.clf()
    plt.scatter(sizes, times)
    plt.title(title)
    plt.xlabel("Size of the database")
    plt.ylabel("Time elapsed (s)")
    plt.show()

    plt.cla()
    plt.clf()
    plt.scatter(sizes, ruleCounts)
    plt.title(title)
    plt.xlabel("Size of the database")
    plt.ylabel("Number of rules found")
    plt.show()

    plt.cla()
    plt.clf()
    plt.scatter(ruleCounts, times)
    plt.title(title)
    plt.xlabel("Number of rules found")
    plt.ylabel("Time elapsed (s)")
    plt.show()

def minsupRetail():
    database = covid_loader.load()
    times = []
    minsups = []
    ruleCounts = []
    for i in range(0, 40):
        minsup = int(300 * 1.05 ** i)
        print(f'Calculating with minsup = {minsup}')

        start = perf_counter()
        ruleSet = prefixspan(database, minsup)
        stop = perf_counter()

        times.append(stop - start)
        minsups.append(minsup)
        ruleCounts.append(len(ruleSet))
    graphMinSup(minsups, times, ruleCounts, "MinSup experiment for RETAIL dataset")

def minsupCovid():
    database = covid_loader.load()
    times = []
    minsups = []
    ruleCounts = []
    for i in range(2, 20):
        minsup = int(1.4 ** i)
        print(f'Starting with minsup = {minsup}')

        start = perf_counter()
        ruleSet = prefixspan(database, minsup)
        stop = perf_counter()

        times.append(stop - start)
        minsups.append(minsup)
        ruleCounts.append(len(ruleSet))
    graphMinSup(minsups, times, ruleCounts, "MinSup experiment for COVID dataset")

def sizeCovid():
    database = covid_loader.load()
    times = []
    indices = []
    ruleCounts = []
    slices = 50
    for i in range(slices):
        index = int(len(database)*(i+1.)/slices)
        print(f'Calculating with size = {index}')

        start = perf_counter()
        ruleSet = prefixspan(database[:index], 200)
        stop = perf_counter()

        times.append(stop - start)
        indices.append(index)
        ruleCounts.append(len(ruleSet))
    graphSize(indices, times, ruleCounts, "Size experiment for COVID dataset")

def sizeRetail():
    database = retail_loader.load()
    times = []
    indices = []
    ruleCounts = []
    slices = 50
    for i in range(slices):
        index = int(len(database)*(i+1.)/slices)
        print(f'Calculating with size = {index}')

        start = perf_counter()
        ruleSet = prefixspan(database[:index], 1300)
        stop = perf_counter()

        times.append(stop - start)
        indices.append(index)
        ruleCounts.append(len(ruleSet))
    graphSize(indices, times, ruleCounts, "Size experiment for RETAIL dataset")

if __name__ == "__main__":
    sizeCovid()
    sizeRetail()
    minsupCovid()
    minsupRetail()