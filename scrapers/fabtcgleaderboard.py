from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from _typeshed import NoneType
from scrapers.scraper import Scraper
import scrapers.util as util
import queue

NUM_ROWS_PER_PAGE = 50

class FABTCGLeaderboard(Scraper):
  def __init__(self, num_of_pages=5):
    super().__init__(num_of_pages)

  # Scrapes a single product's price(s) from website for a given product_id
  def scrape_product_price(self, page_num, save_output=''):
    url = f"https://fabtcg.com/leaderboards/?page={page_num}"
    soup, cookies = util.get_soup(url)
    if (save_output != ''):
      # Save soup
      util.save_soup(soup, save_output)

    # Scrape data from leaderboard page
    leaderboard_data = util.parse_soup_leaderboard(soup, 'div', 'block-table')

    return url, leaderboard_data

  # Fetches and prints a product's price(s) for a given yaml product_dict object
  # Puts result into return_queue if fetch was successful
  def fetch_product_prices(self, page_num, return_queue):
    url = ''
    try:
      url, leaderboard_data = self.scrape_product_price(page_num)
      print(f"Found data for page {page_num}, url: {url}, data: {leaderboard_data}")
      #util.print_formatted_prices(set, title, lowest_price)
      #all_prices = [lowest_price]
      for data in leaderboard_data:
        print(f"putting leaderboard data: {data}")
        return_queue.put(data)
      #product_data = ProductData(url, name, set, all_prices, util.get_date())
      #return_queue.put(product_data)
    except Exception as err:
      print(f"Failed to get data for page: {page_num}, url: {url}, error: {err}")

  # Fetches, prints, and returns all products' price(s) with a given _sleep in between
  def fetch_all_product_prices(self, _sleep=1):
    # Reinit self.return_queue
    self.return_queue = queue.Queue(self.num_of_pages * NUM_ROWS_PER_PAGE)
    # Multithreaded solution
    results = util.run_multithreaded(self.fetch_product_prices, range(1, self.num_of_pages + 1), self.return_queue, sleep=_sleep)
    print(f"fetch_all_product_prices() results: {results}")
    return results