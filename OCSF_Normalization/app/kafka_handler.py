# app/kafka_handler.py

import json
import logging
from confluent_kafka import Consumer, Producer, KafkaError
from configs.kafka_config import (
    INPUT_KAFKA_BOOTSTRAP_SERVERS,
    INPUT_KAFKA_TOPIC,
    INPUT_GROUP_ID,
    OUTPUT_KAFKA_BOOTSTRAP_SERVERS,
    OUTPUT_KAFKA_TOPIC
)

logging.basicConfig(level=logging.INFO)

# 입력용 Kafka 설정
consumer_conf = {
    'bootstrap.servers': INPUT_KAFKA_BOOTSTRAP_SERVERS,
    'group.id': INPUT_GROUP_ID,
    'auto.offset.reset': 'latest',
    'enable.auto.commit': True
}
consumer = Consumer(consumer_conf)
consumer.subscribe([INPUT_KAFKA_TOPIC])

# 출력용 Kafka 설정
producer = Producer({'bootstrap.servers': OUTPUT_KAFKA_BOOTSTRAP_SERVERS})

def receive_log(timeout=1.0) -> str | None:
    msg = consumer.poll(timeout)
    if msg is None or msg.error():
        return None
    try:
        return msg.value().decode("utf-8")
    except Exception as e:
        logging.warning(f"Kafka decode error: {e}")
        return None

def send_to_kafka(mapped_log: dict):
    try:
        producer.produce(OUTPUT_KAFKA_TOPIC, value=json.dumps(mapped_log))
        producer.flush()
        logging.info("Sent to Kafka (ocsf-logs)")
    except Exception as e:
        logging.error(f"Kafka send error: {e}")
