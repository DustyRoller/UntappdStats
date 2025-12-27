import pandas as pd

df = pd.read_csv('checkins_data.csv')

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
