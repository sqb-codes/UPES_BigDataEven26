from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v : json.dumps(v).encode()
)

event_types = ["login", "transaction", "order"]

while True:
    event = {
        "user_id": random.randint(100,999),
        "event_type": random.choice(event_types),
        "amount": random.randint(100,50000),
        "location": random.choice(['Delhi', 'Mumbai', 'Pune']),
        "timestamp": time.time()
    }

    producer.send(
        topic='events_topic',
        value=event
    )
    print("Sent Event :", event)
    time.sleep(5)