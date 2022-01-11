import time

# 24 hours sleep time
SLEEPTIMESECONDS = 24 * 60 * 60

def run():
  exec(open("scrape_data.py").read())
  print(f"Sleeping for {SLEEPTIMESECONDS / 3600} hours")
  time.sleep(SLEEPTIMESECONDS)

while(1):
  run()