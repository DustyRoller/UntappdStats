# UntappdStats
Parses your Untappd checkins to generate stats.

## Usage

* Arguments:
  * `checkins_file` - Path to your Untappd checkins (csv) file.

```
python untappd_stats.py --checkins_file "Path/to/checkins/data.csv"
```

## Output

Script will produce overall stats followed by a year by year breakdown. Stats include:

* Date span of check-ins.
* Average number of beers per year.
* Busiest year.
* Percent of styles checked in.
* Percent of brewery countries checked in from.
* Total number of beers.
* Total number of unique beers.
* First check-in.
* Last check-in.
* Most checked-in beers.
* Highest rated beers.
* Lowest rated beers.
* Average rating.
* Highest ABV.
* Average ABV.
* Highest IBU.
* Average IBU.
* Total number of distinct styles.
* Top 5 distinct styles
* Total number of grouped styles.
* Top 5 grouped styles.
* Total number of breweries.
* Top 5 breweries.
* Total number of brewery countries.
* Top 5 brewery countries.
* Total number of venues.
* Top 5 venues.
* Total number of venue countries.
* Top 5 venue countries.
* Total number of serving type.
* Top 5 serving type.
* Check-ins by month.
* Check-ins by day of week.
