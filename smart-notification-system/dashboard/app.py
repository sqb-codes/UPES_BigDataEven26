import streamlit as st
from kafka import KafkaConsumer
import json
import pandas as pd
import time
import sys
import os
import threading
import queue

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from consumer.rule_engine import evaluate_event

st.set_page_config(page_title="Smart Notification Dashboard",
                   layout="wide")

st.title("Smart Notification Dashboard")

def consume_data(event_queue):
    consumer = KafkaConsumer(
        'events_topic',
        bootstrap_servers='localhost:9092',
        value_deserializer=lambda x: json.loads(x.decode()),
        group_id='event-consumer-group',
        auto_offset_reset='earliest',
        enable_auto_commit=True
    )

    for message in consumer:
        event = message.value
        print("Received Event:", event)

        result = evaluate_event(event)
        event['priority'] = result['priority']
        event['reason'] = result['reason']

        print("Processed Event")
        print("Priority :", event['priority'])
        print("Reason :", event['reason'])

        event_queue.put(event)

# Initialize session state
if "event_queue" not in st.session_state:
    st.session_state.event_queue = queue.Queue()

if "data_store" not in st.session_state:
    st.session_state.data_store = []

if "notification_count" not in st.session_state:
    st.session_state.notification_count = 0

if "thread_started" not in st.session_state:
    threading.Thread(target=consume_data, args=(st.session_state.event_queue,), daemon=True).start()
    st.session_state.thread_started = True

# Drain queue into session_state on each rerun
while not st.session_state.event_queue.empty():
    event = st.session_state.event_queue.get()
    st.session_state.data_store.append(event)
    if len(st.session_state.data_store) > 50:
        st.session_state.data_store.pop(0)
    if event.get('priority') == 'HIGH':
        st.session_state.notification_count += 1

data_store = st.session_state.data_store
notification_count = st.session_state.notification_count

# Create dynamic UI
placeholder = st.empty()

with placeholder.container():
    print("Data Store:", len(data_store))

    if data_store:
        df = pd.DataFrame(data_store)

        col_1, col_2, col_3 = st.columns(3)

        with col_1:
            st.metric("Total Events:", len(df))

        with col_2:
            st.metric("High Priority Alerts:", notification_count)

        with col_3:
            st.metric("Max Amount:", int(df['amount'].max()))

        st.subheader("Transaction Trend")
        st.line_chart(df["amount"])

        st.subheader("High Priority Events")
        high_df = df[df['priority'] == "HIGH"]
        if not high_df.empty:
            st.dataframe(high_df)
        else:
            st.write("No high priority events...")

        st.subheader("All Events")
        st.dataframe(df)
    else:
        st.write("Waiting for events...")

time.sleep(2)
st.rerun()
