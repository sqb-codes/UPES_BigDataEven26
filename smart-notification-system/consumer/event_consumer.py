from kafka import KafkaConsumer
import json
from rule_engine import evaluate_event
from notification_service import send_notification

consumer = KafkaConsumer(
    # topic to subscribe to
    'events_topic',
    # kafka broker address
    bootstrap_servers='localhost:9092',
    # convert bytes -> JSON -> Python dictionary
    value_deserializer=lambda x : json.loads(x.decode()),
    # Consumer group ID (multiple consumers can share load)
    group_id='event-consumer-group',
    # if no offset exists -> start from beginning of topic
    auto_offset_reset='earliest',
    # Automatically commit offsets after consuming messages
    enable_auto_commit=True
)

for message in consumer:
    event = message.value
    print("Received Event:",event)

    result = evaluate_event(event)
    priority = result['priority']
    reason = result['reason']

    print("Processed Event")
    print("Priority :",priority)
    print("Reason :",reason)

    if priority == "HIGH":
        send_notification(event, priority, reason)

