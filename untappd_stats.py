from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd
from pandas import DataFrame, Series


def parse_checkins_file(input_file: Path) -> None:
    df: DataFrame = pd.read_csv(input_file)

    total_num_beers: int = len(df)

    print(f"Total number of beers: {total_num_beers}")

    # Set the `created_at` data to be datetimes.
    df['created_at'] = pd.to_datetime(df['created_at'], errors='raise')
    years: Series[int] = df['created_at'].dt.year.value_counts()

    print(f"\nNumber of active years: {years.count()}")

    average_beers: float = round(total_num_beers/years.count(), 2)

    print(f"\nAverage number of beers per year: {average_beers}")

    # Only getting 1 year but still loop over the values.
    for year, count in years.head(1).items():
        print(f"\nBusiest year was: {year} with {count} checkins")

    _print_field_data(df, "beer_type", "distinct styles")
    _print_field_data(df, "beer_type", "grouped styles", _string_split)
    _print_field_data(df, "brewery_name", "breweries")
    _print_field_data(df, "brewery_country", "brewery countries")
    _print_field_data(df, "venue_name", "venues")
    _print_field_data(df, "venue_country", "venue countries")


def _print_field_data(df: DataFrame, field: str, field_friendly_name: str, transform: Optional[Callable[[Series], Series]] = None) -> None:
    series: Series[Any] = df[field] if transform is None else transform(df[field])
    counts: Series[int] = series.value_counts()

    print(f"\nTotal number of {field_friendly_name} {counts.count()}")
    print(f"Top 5 {field_friendly_name}: ")
    for value, count in counts.head(5).items():
        print(f"\t{value}: {count}")


def _string_split(series: Series) -> Series:
    return series.str.split('-').str[0]


if __name__ == '__main__':
    from argparse import ArgumentParser, Namespace

    arg_parser: ArgumentParser = ArgumentParser()

    arg_parser.add_argument('--checkins_file', required=True)

    args: Namespace = arg_parser.parse_args()

    checkins_file: Path = Path(args.checkins_file)

    expected_file_ext: str = ".csv"
    if checkins_file.suffix != expected_file_ext:
        print(f"checkins_file must be of type {expected_file_ext}")
        exit(-1)

    if not checkins_file.is_file():
        print(f"checkins_file {checkins_file} does not exist")
        exit(-1)

    print(f"Parsing {checkins_file}")

    parse_checkins_file(checkins_file)
