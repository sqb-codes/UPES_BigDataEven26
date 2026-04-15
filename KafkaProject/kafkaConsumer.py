from kafka import KafkaConsumer
import json

# Create Kafka Consumer
consumer = KafkaConsumer(
    'transactions',  # topic name
    bootstrap_servers='localhost:9092', # address of the Kafka broker
    auto_offset_reset='earliest',  # start reading from the earliest message
    group_id='transaction-consumers',  # consumer group id
    value_deserializer=lambda v: json.loads(v.decode('utf-8')),  # deserialize the value from bytes to JSON
    key_deserializer=lambda k: k.decode('utf-8')  # deserialize the key from bytes to string
)

def detect_fraud(transaction):
    # Simple fraud detection logic based on transaction amount
    if transaction['amount'] > 40000:
        return True
    return False

for message in consumer:
    txn = message.value
    print(f"Consumed transaction: {txn}")
    if detect_fraud(txn):
        print(f"Fraud detected for transaction: {txn}")
    else:
        print(f"Transaction is normal: {txn}")