from kafka import KafkaProducer
import json
import time
import random

# Create Kafka Producer
producer = KafkaProducer(
    # address of the Kafka broker
    bootstrap_servers='localhost:9092',
    # serialize the value as JSON and encode it to bytes
    value_serializer=lambda v: json.dumps(v).encode('utf-8'),
    # serialize the key as UTF-8 encoded bytes
    key_serializer=lambda k: k.encode('utf-8')
)

users = [101,102,103,104,105]

def generate_transactions():
    return {
        'user_id': random.choice(users),
        'amount': random.randint(0,50000),
        'location': random.choice(['New York', 'Los Angeles', 'Houston', 'Phoenix']),
        'timestamp': int(time.time())
    }

while True:
    txn = generate_transactions()
    print(f"Producing transaction: {txn}")
    key = str(txn['user_id'])
    producer.send(
        'transactions',  # topic name
        key=key,         # message key (user_id)
        value=txn        # message value (transaction data)
    )
    print(f"Sent transaction for user_id: {key}")
    time.sleep(5)  # Sleep for a while before sending the next transaction
    producer.flush()  # Ensure all messages are sent before exiting