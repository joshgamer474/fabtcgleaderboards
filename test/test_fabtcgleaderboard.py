from scrapers import util
from scrapers import leaderboard_data
from scrapers.leaderboard_data import LeaderboardData
from scrapers.fabtcgleaderboard import FABTCGLeaderboard

# Create scraper
fabl_scraper = FABTCGLeaderboard(1)

# Scrape one page of leaderboard data
url, leaderboarddata = fabl_scraper.scrape_product_price(1, \
  save_output='fabout.txt')

print(f"url: {url}, data: {leaderboarddata}")

util.push_data_to_localdb(leaderboarddata, '~/localbackup/fabtcgleaderboardsbackuptest.json')