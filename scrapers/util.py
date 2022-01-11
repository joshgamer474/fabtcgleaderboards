import yaml
import json
from os.path import expanduser
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import threading
import time
from datetime import datetime
from kafka import KafkaProducer
import kafka
from scrapers.leaderboard_data import LeaderboardData

HEADERS = {
          #'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.71 Safari/537.36',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:92.0) Gecko/20100101 Firefox/92.0',
          'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
          'Accept-Language': 'en-US, en;q=0.5',
          'Accept-Encoding': 'identity',
          #'Accept Encoding': 'gzip, deflate, br',
          'Accept': '*/*',
          'Cache-Control': 'max-age=0',
          'Connection': 'keep-alive',
          }

def read_yaml(filename, category):
  with open(filename, "r") as f:
    doc = yaml.load(f, Loader=yaml.BaseLoader)
    return doc[category]

def get_soup(url, cookies=None):
  useHeaders = HEADERS
  if (cookies != None):
    useHeaders['Cookie'] = '; '.join(cookies)
    #print(f"get_soup() using headers: {useHeaders}")
  req = Request(url, headers=useHeaders)
  page = urlopen(req)
  html = page.read().decode("utf-8")
  cookies = page.info().get_all('Set-Cookie')
  soup = BeautifulSoup(html, "html.parser")
  return soup, cookies

# Write out prettify soup to file
def save_soup(soup, outfile):
  with open(outfile, "w", encoding='utf-8') as f:
    f.writelines(soup.prettify())

# Parse html soup for prices by class
def parse_soup_leaderboard(soup, type, class_):
  ret = []
  today = datetime.today().strftime('%Y-%m-%d')
  found = soup.find_all(type, {'class': class_})
  for tag in found:
    #print(f"found tag: {tag}")
    rows = tag.find_all('tr')
    #print(f"found {len(rows)} rows")
    headers = {}
    reverse_headers = {}
    for rindex in range(0, len(rows)):
      # Initialize reverse headers dict
      if rindex > 0 and len(reverse_headers) == 0:
        reverse_headers = {v: k for k, v in headers.items()}
        #print(f"rev headers: {reverse_headers}")
      r = rows[rindex]
      index = 0
      r_data = {}
      for i in r:
        if i.string is not None and i.string.strip():
          #print(f"{i.string.strip()}")
          if rindex == 0:
            # Save header value from table
            headers[i.string.strip()] = (index)
          else:
            # Save data value from table
            r_data[reverse_headers[index]] = i.string.strip()
        else:
          # Try to parse country value from table
          try:
            country = i.find('i')['title']
            #print(f"{country}")
            r_data[reverse_headers[index]] = country
          except:
            index += 1
            pass
        index += 1
      #print(f"rdata: {r_data}")
      #print("********************")
      values = list(r_data.values())
      #print(f"values len: {len(values)}, data: {values}")
      try:
        ret.append(LeaderboardData(values[0], values[1], values[2], values[3], today))
      except:
        continue
  #print(f"headers: {headers}")
  #print(f"ret len: {len(ret)}")
  return ret

def run_multithreaded(method, args, return_queue, sleep=0):
  threads = []
  print(f"Starting run_multithreaded() for method: {method}")
  # Create threads
  for arg in args:
    t = threading.Thread(target=method, args=(arg, return_queue))
    t.start()
    threads.append(t)
    time.sleep(sleep)
  time.sleep(sleep)
  print("Done creating threads, will now start join()ing them")
  # Ensure threads end
  for thread in threads:
    thread.join()
  print("Done join()ing threads, will now get results from return queue")
  # Get results from queue
  results = []
  while not return_queue.empty():
    result = return_queue.get_nowait()
    results.append(result)
    return_queue.task_done()
  print(f"Done run_multithreaded() for method: {method}")
  return results

def get_date():
  return str(datetime.utcnow())

def push_data_to_kafka(data_list, kafka_yaml_filename, kafka_yaml_category):
  # Get Kafka Server info
  kafka_yaml = read_yaml(kafka_yaml_filename, kafka_yaml_category)
  kafka_server = kafka_yaml['Server']
  print(f"Producing to Kafka server: {kafka_server}")

  # Create Kafka producer
  producer = KafkaProducer(bootstrap_servers=kafka_server)

  for result in data_list:
    # Recast data to LeaderboardData
    lead_data = LeaderboardData(result.rank,
      result.country,
      result.name,
      result.xp,
      result.date)
    # Push data to Kafka
    print(f"Pushing set {lead_data.set} to Kafka, rank: {result.rank}, country: {result.country}, name: {result.name}, xp: {result.xp}, date: {result.date}")
    # Asynchronous send
    future = producer.send('data',
                  lead_data.to_json())
  producer.flush()

def push_data_to_localdb(data_list, filename):
  print(f"Saving {len(data_list)} data entries to {filename}")
  path = expanduser(filename)
  with open(path, 'a+', encoding='utf-8') as f:
    for result in data_list:
      f.writelines("%s\n" % result.to_json().decode("utf-8"))

def read_data_from_localdb(filename):
  ret = []
  # Manually read db with utf-8 encoding as JsonDatabase does not
  path = expanduser(filename)
  with open(path, 'r', encoding='utf-8') as f:
    while True:
      line = f.readline()
      if not line:
        break
      item = json.loads(line)
      #print(f"item: %s" % item)
      # Recast data to LeaderboardData
      lead_data = LeaderboardData(item['rank'],
        item['country'],
        item['name'],
        item['xp'],
        item['date'])
      #print(f"Read leaderboard data: {lead_data}")
      ret.append(lead_data)
    print(f"Read {len(ret)} items from {filename}")
    return ret
