from pathlib import Path
from typing import Any, Callable, Optional

import pandas as pd
from pandas import DataFrame, Series, Timestamp


def parse_checkins_file(input_file: Path) -> None:
    df: DataFrame = pd.read_csv(input_file)

    total_num_beers: int = len(df)
    print(f"Total number of beers: {total_num_beers}")

    # Get the number of unique beer and brewery combinations.
    num_unique_beers: int = df[['beer_name', 'brewery_name']].drop_duplicates().shape[0]
    print(f"Total number of unique beers: {num_unique_beers}")

    # Convert the `created_at` data to be datetimes.
    df['created_at'] = pd.to_datetime(df['created_at'], errors='raise')

    # Get the number of active years.
    years: Series[int] = df['created_at'].dt.year
    print(f"\nNumber of active years: {years.value_counts().count()}")

    # Get first check-in.
    first_checkin: Timestamp = df['created_at'].min()
    print(f"First check-in at {first_checkin.date()}")

    # Get the average number of beers per year.
    average_beers: float = round(total_num_beers / years.nunique(), 2)
    print(f"\nAverage number of beers per year: {average_beers}")

    # Get the busiest year.
    year_counts: Series[int] = years.value_counts()
    busiest_year: int = year_counts.idxmax()
    busiest_count: int = year_counts.max()
    print(f"\nBusiest year was {busiest_year} with {busiest_count} check-ins")

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
    from sys import exit

    arg_parser: ArgumentParser = ArgumentParser()
    arg_parser.add_argument('--checkins_file', required=True, type=Path)

    args: Namespace = arg_parser.parse_args()

    if not args.checkins_file.is_file():
        exit(f"File does not exist: {args.checkins_file}")

    expected_file_ext: str = ".csv"
    if args.checkins_file.suffix != expected_file_ext:
        exit(f"checkins_file must be a {expected_file_ext} file")

    print(f"Parsing {args.checkins_file}\n")
    parse_checkins_file(args.checkins_file)
