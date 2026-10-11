import time
import json
import random

from kafka import KafkaProducer
from kafka.errors import KafkaError

def create_producer():
    """
    Create a Kafka producer instance.

    Returns:
        KafkaProducer: An instance of KafkaProducer.
    """
    while True:
        try:
            producer = KafkaProducer(
                bootstrap_servers='kafka:9092',
                value_serializer=lambda v: json.dumps(v).encode('utf-8')
            )
            return producer
        except KafkaError:
            print("Waiting for kafka...")
            time.sleep(5)


def generate_transaction():
    """
    Generate a random transaction.

    Returns:
        dict: A dictionary representing a transaction.
    """

    transaction = {
        'amount': random.randint(10, 1000),
        'transaction_time': random.uniform(0, 24),
        'user_age': random.randint(18, 70),
        'is_international': random.randint(0, 1),
    }
    return transaction


producer = create_producer()
while True:
    transaction = generate_transaction()
    producer.send('transactions', value=transaction)
    print(f"Sent transaction: {transaction}")
    time.sleep(1)  # Simulate a delay between transactions