import scrapers.util as util
import queue

# Default parent scraper class
# All scrapers should derive from this class
class Scraper:
  def __init__(self, num_of_pages=10):
    self.num_of_pages = num_of_pages
    # Return queue for multithreaded fetching
    self.return_queue = queue.Queue()

  # Scrapes a single product's price(s) from website for a given product_id
  def scrape_product_price(self, product_id, save_output):
    pass

  # Fetches and prints a product's price(s) for a given yaml product_dict object
  # Puts result into return_queue if fetch was successful
  def fetch_product_prices(self, product_dict, return_queue):
    pass

  # Fetches, prints, and returns all products' price(s) with a given _sleep in between
  def fetch_all_product_prices(self, _sleep):
    pass