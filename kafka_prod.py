from kafka import KafkaProducer
import json

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

data = {"user_id": 101, "action": "login", "timestamp": "2024-06-01T12:00:00Z"}
producer.send('user_actions', value=data)
producer.flush()
print("Message sent to Kafka topic 'user_actions'")

