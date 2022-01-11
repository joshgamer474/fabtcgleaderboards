import scrapers.util as util

# Read all productdata from fabtcgleaderboardsbackup backup
data = util.read_data_from_localdb('~/localbackup/fabtcgleaderboardsbackup.json')
print(f"Read data len: {len(data)}")

# Push localdb data to Kafka
print(f"Pushing {len(data)} items from localdb to Kafka")
util.push_data_to_kafka(data, 'kafka.yaml', 'Kafka')