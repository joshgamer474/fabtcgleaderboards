from kafka import KafkaConsumer
from scrapers import util
from datetime import datetime

# Get Kafka Server info
kafka_yaml = util.read_yaml('kafka.yaml', 'Kafka')
kafka_server = kafka_yaml['Server']
print(f"Using Kafka server: {kafka_server}")

topics = [
  'data',
]

# Create filename for db backup file
backupfilename = datetime.today().strftime('%Y%m%d') + ".json"

# Create Kafka consumer to verify test
consumer = KafkaConsumer(
  bootstrap_servers=kafka_server,
  auto_offset_reset='earliest',
  group_id=None,
  consumer_timeout_ms=1000)

# Subscribe to consume testset topic
consumer.subscribe(topics)
print(f"Kafka consumer subscribed to topics: {consumer.topics()}")

# Consume all messages on all topics and write out to a backup .json file
print("Will now attempt to consume messages")
msg_count = 0
with open(backupfilename, 'w') as f:
  # Verify testset was successfully pushed to Kafka
  for msg in consumer:
    data = msg.value.decode("utf-8")
    f.writelines("%s\n" % data)
    #print(f"Consumed data from topic testset: {msg}")
    msg_count += 1
    #print(f"Consumed %d msgs" % msg_count)

print(f"Backed up %d msgs to %s" % (msg_count, backupfilename))