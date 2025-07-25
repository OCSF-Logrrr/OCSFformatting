# app/kafka_handler.py

from confluent_kafka import Consumer, Producer, KafkaError
from configs.kafka_config import INPUT_KAFKA_BOOTSTRAP_SERVERS, INPUT_KAFKA_TOPIC, INPUT_GROUP_ID, OUTPUT_KAFKA_BOOTSTRAP_SERVERS, OUTPUT_KAFKA_TOPIC
import json
import logging

logging.basicConfig(level=logging.INFO)

# 입력용 Kafka 설정
consumer_conf = {
    'bootstrap.servers': INPUT_KAFKA_BOOTSTRAP_SERVERS,
    'group.id': INPUT_GROUP_ID,
    'auto.offset.reset': 'earliest',
    'enable.auto.commit': True,
    'max.poll.interval.ms': 60000000
}
consumer = Consumer(consumer_conf)
consumer.subscribe(INPUT_KAFKA_TOPIC)

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


async def send_to_kafka(mapped_log):

    def fix_message_field(mapped_log: dict) -> dict:
        if "message" in mapped_log and isinstance(mapped_log["message"], str):
            try:
                mapped_log["message"] = json.loads(mapped_log["message"])
            except json.JSONDecodeError:
                pass
        return mapped_log

    try:
        mapped_log = fix_message_field(mapped_log)
        producer.produce(OUTPUT_KAFKA_TOPIC, value=json.dumps(mapped_log))
        producer.flush()
        logging.info("Sent to Kafka (ocsf-logs)")
    except Exception as e:
        logging.error(f"Kafka send error: {e}")
        
