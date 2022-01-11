# FABTCG Leaderboard Scraper
The FABTCG Leaderboard scraper scrapes https://fabtcg.com/leaderboards/ once per day and backs up the data in a parseable json format for other uses.

## Prerequisites
* Python 3

## How to use
```python run.py```

## Increase the number of pages of data scraped
Increase the value ```FABTCGLeaderboard(10)``` in ```/scrape_data.py``` to your desired number of results.
Note: 50 results are posted per page as of 1/10/2022.

## Running a test scrape
```python -m test.test_fabtcgleaderboard```