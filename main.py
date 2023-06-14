import argparse

import experiments

parser = argparse.ArgumentParser(prog="PrefixSpan")
parser.add_argument(
    "dataset",
    type=str,
    choices=["covid", "retail"],
    help="One of the two possible datasets",
)
parser.add_argument("minsup", type=int, help="The minimum support threshold")
parser.add_argument(
    "-l",
    "--logging",
    default=False,
    help="Print details during algorithm run?",
    action="store_true",
)

if __name__ == "__main__":
    args = parser.parse_args()
    experiments.singleRun(args.dataset, args.minsup, args.logging)
