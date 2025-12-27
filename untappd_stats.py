import pandas as pd


def parse_checkins_file(input_file):
    df = pd.read_csv(input_file)

    print(f"Total number of beers: {len(df)}")

    beer_type = df["beer_type"].value_counts()

    print(f"\nTotal number of distinct styles {beer_type.count()}")
    print("Top 5 styles: ")
    for value, count in beer_type.head(5).items():
        print(f"\t{value}: {count}")

    style_groups = df['beer_type'].str.split('-').str[0].value_counts()

    print(f"\nTotal number of styles {style_groups.count()}")
    print("Top 5 styles: ")
    for value, count in style_groups.head(5).items():
        print(f"\t{value}: {count}")

    breweries = df["brewery_name"].value_counts()

    print(f"\nTotal number of breweries {breweries.count()}")
    print("Top 5 breweries: ")
    for value, count in breweries.head(5).items():
        print(f"\t{value}: {count}")

    brewery_country = df["brewery_country"].value_counts()

    print(f"\nTotal number of unique brewery countries {brewery_country.count()}")
    print("Top 5 countries: ")
    for value, count in brewery_country.head(5).items():
        print(f"\t{value}: {count}")

    venue = df["venue_name"].value_counts()
    print(f"\nTotal number of venues {venue.count()}")
    print("Top 5 venues: ")
    for value, count in venue.head(5).items():
        print(f"\t{value}: {count}")

    venue_country = df["venue_country"].value_counts()
    print(f"\nTotal number of venue countries {venue_country.count()}")
    print("Top 5 venue countries: ")
    for value, count in venue_country.head(5).items():
        print(f"\t{value}: {count}")


if __name__ == '__main__':
    from argparse import ArgumentParser
    from pathlib import Path

    arg_parser = ArgumentParser()

    arg_parser.add_argument('--checkins_file', required=True)

    args = arg_parser.parse_args()

    checkins_file = Path(args.checkins_file)

    expected_file_ext = ".csv"
    if checkins_file.suffix != expected_file_ext:
        print(f"checkins_file must be of type {expected_file_ext}")
        exit(-1)

    if not checkins_file.is_file():
        print(f"checkins_file {checkins_file} does not exist")
        exit(-1)

    print(f"Parsing {checkins_file}")

    parse_checkins_file(checkins_file)
