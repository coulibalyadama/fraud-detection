import time
import json
import tracemalloc

import joblib
from kafka import KafkaConsumer
from kafka.errors import KafkaError
from prometheus_client import start_http_server, Counter, Gauge


PREDICTION_COUNTER = Counter('fraud_predictions_total', 'Total number of fraud predictions made')
PREDICTION_LATENCY = Gauge('fraud_prediction_latency_seconds', 'Latency of fraud prediction in seconds')
PREDICTION_MEMORY_CURRENT = Gauge(
    'fraud_prediction_memory_current_bytes',
    'Python memory still allocated after the prediction'
)
PREDICTION_MEMORY_PEAK = Gauge(
    'fraud_prediction_memory_peak_bytes',
    'Peak Python memory allocated during the prediction'
)

# Start Prometheus metrics server on port 8001 early
print("Starting Prometheus metrics server on port 8001...")
start_http_server(8001)
print("Prometheus metrics server started.")
tracemalloc.start()

model = joblib.load("models/model.pkl")

def create_consumer():
    """
    Create a Kafka consumer instance.

    Returns:
        KafkaConsumer: An instance of KafkaConsumer.
    """
    while True:
        try:
            consumer = KafkaConsumer(
                'transactions',
                bootstrap_servers='kafka:9092',
                auto_offset_reset='earliest',
                group_id='transaction-consumer-group',
                value_deserializer=lambda v: json.loads(v.decode('utf-8'))
            )
            return consumer
        except KafkaError:
            print("Waiting for kafka...")
            time.sleep(5)

consumer = create_consumer()

for message in consumer:
    trx_start_time = time.time()
    transaction = message.value
    tracemalloc.reset_peak()

    input_data = [[
        transaction['amount'],
        transaction['transaction_time'],
        transaction['user_age'],
        transaction['is_international']
    ]]
    
    prediction = model.predict(input_data)[0]
    trx_end_time = time.time()
    latency = trx_end_time - trx_start_time
    memory_current, memory_peak = tracemalloc.get_traced_memory()
    PREDICTION_COUNTER.inc()
    PREDICTION_LATENCY.set(latency)
    PREDICTION_MEMORY_CURRENT.set(memory_current)
    PREDICTION_MEMORY_PEAK.set(memory_peak)
    
    if prediction == 1:
        print(f"Fraudulent transaction detected: {transaction}")
    else:
        print(f"Legitimate transaction: {transaction}")