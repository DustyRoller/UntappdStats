import calendar
import json
from collections.abc import Callable
from pathlib import Path
from typing import Any

from dateutil.relativedelta import relativedelta

import pandas as pd
from pandas import DataFrame, Series, Timestamp
from pandas.core.groupby import DataFrameGroupBy


def parse_checkins_file(input_file: Path) -> None:
    df: DataFrame = pd.read_csv(input_file)

    # Update the dataframe as required.
    _update_dataframe(df)

    # Get the number of active years.
    first_checkin: Timestamp = df.created_at.min()
    last_checkin: Timestamp = df.created_at.max()
    active_period: relativedelta = relativedelta(last_checkin, first_checkin)
    print(f"Active for: {active_period.years} years and {active_period.months} months")

    # Get the average number of beers per year (only if years is greater than 0).
    if active_period.years > 0:
        average_beers: float = round(len(df) / active_period.years, 2)
        print(f"\nAverage number of beers per year: {average_beers}")

    # Get the busiest year.
    year_counts: Series[int] = df.created_at.dt.year.value_counts()
    busiest_year: int = year_counts.idxmax()
    busiest_count: int = year_counts.max()
    print(f"\nBusiest year: {busiest_year} - {busiest_count} check-ins")

    data_dir: Path = Path("data")

    # Get the percent of styles that there is a check-in for.
    styles: list[str] = _load_data_file(data_dir / "styles.json")
    checked_in_styles: set[str] = set(df.beer_type)

    styles_percentage: float = (len(checked_in_styles) / len(styles)) * 100
    print(f"\nPercent of styles: {round(styles_percentage, 2)}%")

    # Group the data by years.
    year_groups: DataFrameGroupBy[Any] = df.groupby(df.created_at.dt.year)

    # Get the year with the most unique styles.
    top_styles_year, max_styles_count = _get_year_max_value(year_groups, "beer_type")
    print(f"\nYear with most styles: {top_styles_year} - {max_styles_count}")

    # Get the year with most unique breweries.
    top_breweries_year, max_breweries_count = _get_year_max_value(year_groups, "brewery_name")
    print(f"\nYear with most breweries: {top_breweries_year} - {max_breweries_count}")

    # Get the year with most unique brewery countries.
    top_brewery_country_year, max_brewery_countries_count = _get_year_max_value(year_groups, "brewery_country")
    print(f"\nYear with most brewery countries: {top_brewery_country_year} - {max_brewery_countries_count}")

    # Get the year with most unique venues.
    top_venue_year, max_venue_count = _get_year_max_value(year_groups, "venue_name")
    print(f"\nYear with most venues: {top_venue_year} - {max_venue_count}")

    # Get the year with most unique venue countries.
    top_venue_country_year, max_venue_countries_count = _get_year_max_value(year_groups, "venue_country")
    print(f"\nYear with most venue countries: {top_venue_country_year} - {max_venue_countries_count}")

    # Get the percent of brewery countries that there is a check-in for.
    countries: list[str] = _load_data_file(data_dir / "countries.json")
    checked_in_countries: set[str] = set(df.brewery_country)

    brewery_countries_percentage: float = (len(checked_in_countries) / len(countries)) * 100
    print(f"\nPercent of brewery countries: {round(brewery_countries_percentage, 2)}%")

    print("\nOverall stats")

    _get_grouped_stats(df)

    print("\nYear breakdown\n")

    for year, group in year_groups:
        print(f"{year} stats")
        _get_grouped_stats(group)
        print()


def _get_grouped_stats(df: DataFrame) -> None:
    print(f"\tTotal number of beers: {len(df)}")

    # Get the number of unique beer and brewery combinations.
    num_unique_beers: int = df[['beer_name', 'brewery_name']].drop_duplicates().shape[0]
    print(f"\tTotal number of unique beers: {num_unique_beers}")

    # Get first and last check-in.
    print(f"\n\tFirst check-in: {df.created_at.min()}")
    print(f"\tLast check-in: {df.created_at.max()}")

    # Only print out if there any beers with more than one check-in.
    most_common_beers: Series[int] = df[['beer_name', 'brewery_name']].value_counts()
    if most_common_beers.iloc[0] != 1:
        print("\n\tMost checked-in beers:")
        for value, count in most_common_beers.head(5).items():
            if count == 1:
                break
            print(f"\t\t{value[0]} ({value[1]}): {count}")

    print("\n\tHighest rated beers:")
    highest_rated: DataFrame = df.nlargest(5, "rating_score")
    for _, row in highest_rated.iterrows():
        print(f"\t\t{row.beer_name} ({row.brewery_name}): {row.rating_score}")

    print("\n\tLowest rated beers:")
    lowest_rated: DataFrame = df.nsmallest(5, "rating_score")
    for _, row in lowest_rated.iterrows():
        print(f"\t\t{row.beer_name} ({row.brewery_name}): {row.rating_score}")

    # Get the average rating.
    print(f"\n\tAverage rating: {round(df.rating_score.mean(), 2)}")

    # Get the beer with the highest ABV.
    max_abv_index: int = df.beer_abv.idxmax()
    max_abv_beer: Any = df.loc[max_abv_index]
    print(f"\n\tHighest ABV: {max_abv_beer.beer_name} ({max_abv_beer.brewery_name}) - {max_abv_beer.beer_abv}%")

    # Get the average ABV.
    print(f"\n\tAverage ABV: {round(df.beer_abv.mean(), 2)}%")

    # Get the beer with the highest IBU.
    year_max_ibu_index: int = df.beer_ibu.idxmax()
    year_max_ibu_beer: Any = df.loc[year_max_ibu_index]
    print(f"\n\tHighest IBU: {year_max_ibu_beer.beer_name} ({year_max_ibu_beer.brewery_name}) - {year_max_ibu_beer.beer_ibu}")

    # Get the average IBU.
    print(f"\n\tAverage IBU: {round(df.beer_ibu.mean(), 2)}")

    _print_field_data(df, "beer_type", "distinct styles")
    _print_field_data(df, "beer_type", "grouped styles", _string_split)
    _print_field_data(df, "brewery_name", "breweries")
    _print_field_data(df, "brewery_country", "brewery countries")
    _print_field_data(df, "venue_name", "venues")
    _print_field_data(df, "venue_country", "venue countries")
    _print_field_data(df, "serving_type", "serving type")

    month_groups = df.groupby(df.created_at.dt.month)

    print("\n\tCheck-ins by month:")
    for month, group in month_groups:
        print(f"\t\t{calendar.month_name[month]}: {len(group)}")

    day_groups = df.groupby(df.created_at.dt.dayofweek)

    print("\n\tCheck-ins by day of week:")
    for day, group in day_groups:
        print(f"\t\t{calendar.day_name[day]}: {len(group)}")


def _get_year_max_value(year_groups: DataFrameGroupBy[Any], value: str) -> tuple[int, int]:
    # Get the year with the most unique styles.
    unique_styles_counts: Series[int] = year_groups[value].nunique()
    return unique_styles_counts.idxmax(), unique_styles_counts.max()


def _load_data_file(data_file_path: Path) -> list[str]:
    data: list[str] = []
    with data_file_path.open(encoding='utf-8') as f:
        data = json.load(f)

    return data


def _print_field_data(df: DataFrame, field: str, field_friendly_name: str, transform: Callable[[Series], Series] | None = None) -> None:
    series: Series[Any] = df[field] if transform is None else transform(df[field])
    counts: Series[int] = series.value_counts()

    count: int = counts.count()
    if count:
        print(f"\n\tTotal number of {field_friendly_name}: {count}")
        print(f"\tTop 5 {field_friendly_name}: ")
        for value, count in counts.head(5).items():
            print(f"\t\t{value}: {count}")


def _string_split(series: Series) -> Series:
    return series.str.split(' - ').str[0]


def _update_dataframe(df: DataFrame) -> None:
    # Update the data so that it is in a more usable state.

    # Do some initial modification of the data.
    # Convert the `created_at` data to be datetimes.
    df.created_at = pd.to_datetime(df.created_at, errors='raise')

    # Remove the venue country for `Untappd at Home` check-ins so that
    # it isn't included in the venue countries stats.
    df.loc[df.venue_name == "Untappd at Home", "venue_country"] = None


if __name__ == '__main__':
    import sys
    from argparse import ArgumentParser, Namespace

    arg_parser: ArgumentParser = ArgumentParser()
    arg_parser.add_argument('--checkins_file', required=True, type=Path)

    args: Namespace = arg_parser.parse_args()

    if not args.checkins_file.is_file():
        sys.exit(f"File does not exist: {args.checkins_file}")

    expected_file_ext: str = ".csv"
    if args.checkins_file.suffix != expected_file_ext:
        sys.exit(f"checkins_file must be a {expected_file_ext} file")

    print(f"Parsing {args.checkins_file}\n")
    parse_checkins_file(args.checkins_file)
