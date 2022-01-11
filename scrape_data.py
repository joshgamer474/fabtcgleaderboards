from scrapers.fabtcgleaderboard import FABTCGLeaderboard
import scrapers.util as util

# Scrape data
fabtcgleaderboard_scraper = FABTCGLeaderboard(10)
fabtcgleaderboard_results = fabtcgleaderboard_scraper.fetch_all_product_prices(_sleep=0.1)

# Push data to Kafka server
#util.push_data_to_kafka(fabtcgleaderboard_results, 'kafka.yaml', 'Kafka')

# Push data to local db
util.push_data_to_localdb(fabtcgleaderboard_results, '~/localbackup/fabtcgleaderboardsbackup.json')