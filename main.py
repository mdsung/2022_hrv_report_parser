from dataclasses import asdict, fields
from functools import reduce
from pathlib import Path
from typing import Any

import pandas as pd
from tqdm import tqdm

from src.parser import FrequencyDomain, General, Nonlinear, Parser, TimeDomain

RAW_DATA_PATH = Path("data/raw")
OUTPUT_FILENAME = Path("data/processed.csv")


def get_number_from_file(filename: str) -> int:
    return int(filename.split("-")[0])


def get_time_from_file(filename: str) -> str:
    if "-1" in filename:
        return "induction"
    elif "-2" in filename:
        return "operation"
    elif "-3" in filename:
        return "emergence"


def aggregate_dicts(*args: dict[Any, Any]) -> dict[Any, Any]:
    return reduce(lambda x, y: x | y, args)


def aggregate_attributes(
    filename,
    general: General,
    timedomain: TimeDomain,
    frequencydomain: FrequencyDomain,
    nonlinear: Nonlinear,
) -> dict:
    results = {
        "file": str(filename),
        "no": get_number_from_file(filename.stem),
        "time": get_time_from_file(filename.stem),
    }
    return aggregate_dicts(
        results,
        asdict(general),
        asdict(timedomain),
        asdict(frequencydomain),
        asdict(nonlinear),
    )


def save_dataframe(dataframe: pd.DataFrame, output_filename) -> None:
    dataframe.to_csv(output_filename, index=False)


def main():
    results = []
    for file in tqdm(RAW_DATA_PATH.glob("*.html")):
        parser = Parser(file)
        results.append(aggregate_attributes(file, *parser.process()))

    save_dataframe(pd.DataFrame(results).sort_values("no"), OUTPUT_FILENAME)


if __name__ == "__main__":
    main()
