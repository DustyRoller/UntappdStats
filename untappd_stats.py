import json
from pathlib import Path
from typing import Any, Callable, Optional

from dateutil.relativedelta import relativedelta

import pandas as pd
from pandas import DataFrame, Series, Timestamp
from pandas.core.groupby import DataFrameGroupBy


def parse_checkins_file(input_file: Path) -> None:
    df: DataFrame = pd.read_csv(input_file)

    # Update the dataframe as required.
    _update_dataframe(df)

    total_num_beers: int = len(df)
    print(f"Total number of beers: {total_num_beers}")

    # Get the number of unique beer and brewery combinations.
    num_unique_beers: int = df[['beer_name', 'brewery_name']].drop_duplicates().shape[0]
    print(f"Total number of unique beers: {num_unique_beers}")

    # Get the number of active years.
    first_checkin: Timestamp = df['created_at'].min()
    last_checkin: Timestamp = df['created_at'].max()
    active_period: relativedelta = relativedelta(last_checkin, first_checkin)
    print(f"\nActive for: {active_period.years} years and {active_period.months} months")

    # Get first check-in.
    print(f"First check-in at {first_checkin.date()}")

    # Get the average number of beers per year (only if years is greater than 0).
    if active_period.years > 0:
        average_beers: float = round(total_num_beers / active_period.years, 2)
        print(f"\nAverage number of beers per year: {average_beers}")

    # Get the busiest year.
    year_counts: Series[int] = df['created_at'].dt.year.value_counts()
    busiest_year: int = year_counts.idxmax()
    busiest_count: int = year_counts.max()
    print(f"\nBusiest year was {busiest_year} with {busiest_count} check-ins")

    print("\nHighest rated beers:")
    highest_rated: DataFrame = df.nlargest(5, "rating_score")
    for _, row in highest_rated.iterrows():
        print(f"\t{row["beer_name"]} ({row["brewery_name"]}) - {row["rating_score"]}")

    print("\nLowest rated beers:")
    lowest_rated: DataFrame = df.nsmallest(5, "rating_score")
    for _, row in lowest_rated.iterrows():
        print(f"\t{row["beer_name"]} ({row["brewery_name"]}) - {row["rating_score"]}")

    # Get the beer with the highest ABV.
    max_abv_index: int = df["beer_abv"].idxmax()
    max_abv_beer: Any = df.iloc[max_abv_index]
    print(f"\nHighest ABV: {max_abv_beer["beer_name"]} ({max_abv_beer["brewery_name"]}) - {max_abv_beer["beer_abv"]}%")

    # Get the beer with the highest IBU.
    max_ibu_index: int = df["beer_ibu"].idxmax()
    max_ibu_beer: Any = df.iloc[max_ibu_index]
    print(f"\nHighest IBU: {max_ibu_beer["beer_name"]} ({max_ibu_beer["brewery_name"]}) - {max_ibu_beer["beer_ibu"]}")

    _print_field_data(df, "beer_type", "distinct styles")
    _print_field_data(df, "beer_type", "grouped styles", _string_split)

    # Get the percent of styles that there is a check in for.
    with Path("styles.json").open(encoding='utf-8') as f:
        styles: list[str] = json.load(f)

        checked_in_styles: set[str] = set(df['beer_type'])

        styles_percentage: float = (len(checked_in_styles) / len(styles)) * 100
        print(f"\nPercent of styles: {round(styles_percentage, 2)}%")

    _print_field_data(df, "brewery_name", "breweries")
    _print_field_data(df, "brewery_country", "brewery countries")

    # Get the percent of brewery countries that there is a check in for.
    with Path("countries.json").open(encoding='utf-8') as f:
        countries: list[str] = json.load(f)

        checked_in_countries: set[str] = set(df['brewery_country'])

        brewery_countries_percentage: float = (len(checked_in_countries) / len(countries)) * 100
        print(f"\nPercent of brewery countries: {round(brewery_countries_percentage, 2)}%")

    _print_field_data(df, "venue_name", "venues")
    _print_field_data(df, "venue_country", "venue countries")
    _print_field_data(df, "serving_type", "serving types")

    print("\nYear breakdown\n")

    # Group the data by years.
    year_groups: DataFrameGroupBy[Any] = df.groupby(df.created_at.dt.year)
    for year, group in year_groups:
        print(f"\n{year}")
        print(f"\t{len(group)} beers")

        print("\nHighest rated beers:")
        year_highest_rated: DataFrame = group.nlargest(5, "rating_score")
        for _, row in year_highest_rated.iterrows():
            print(f"\t{row["beer_name"]} ({row["brewery_name"]}) - {row["rating_score"]}")

        print("\nLowest rated beers:")
        year_lowest_rated: DataFrame = group.nsmallest(5, "rating_score")
        for _, row in year_lowest_rated.iterrows():
            print(f"\t{row["beer_name"]} ({row["brewery_name"]}) - {row["rating_score"]}")

        # Get the beer with the highest ABV.
        year_max_abv_index: int = group["beer_abv"].idxmax()
        year_max_abv_beer: Any = df.iloc[year_max_abv_index]
        print(f"\nHighest ABV: {year_max_abv_beer["beer_name"]} ({year_max_abv_beer["brewery_name"]}) - {year_max_abv_beer["beer_abv"]}%")

        # Get the beer with the highest IBU.
        year_max_ibu_index: int = group["beer_ibu"].idxmax()
        year_max_ibu_beer: Any = df.iloc[year_max_ibu_index]
        print(f"\nHighest IBU: {year_max_ibu_beer["beer_name"]} ({year_max_ibu_beer["brewery_name"]}) - {year_max_ibu_beer["beer_ibu"]}")

        _print_field_data(group, "beer_type", "distinct styles")
        _print_field_data(group, "beer_type", "grouped styles", _string_split)
        _print_field_data(group, "brewery_name", "breweries")
        _print_field_data(group, "brewery_country", "brewery countries")
        _print_field_data(group, "venue_name", "venues")
        _print_field_data(group, "venue_country", "venue countries")
        _print_field_data(group, "serving_type", "serving type")


def _print_field_data(df: DataFrame, field: str, field_friendly_name: str, transform: Optional[Callable[[Series], Series]] = None) -> None:
    series: Series[Any] = df[field] if transform is None else transform(df[field])
    counts: Series[int] = series.value_counts()

    print(f"\nTotal number of {field_friendly_name} {counts.count()}")
    print(f"Top 5 {field_friendly_name}: ")
    for value, count in counts.head(5).items():
        print(f"\t{value}: {count}")


def _string_split(series: Series) -> Series:
    return series.str.split('-').str[0]


def _update_dataframe(df: DataFrame) -> None:
    # Update the data so that it is in a more usable state.

    # Do some initial modification of the data.
    # Convert the `created_at` data to be datetimes.
    df['created_at'] = pd.to_datetime(df['created_at'], errors='raise')

    # Remove the venue country for `Untappd at Home` checkins so that
    # it isn't included in the venue countries stats.
    df.loc[df.venue_name == "Untappd at Home", "venue_country"] = None


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
