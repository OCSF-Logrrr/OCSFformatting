import os
import json
import time
import sys
from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

# 환경 변수
brokers    = os.getenv("BROKERS", "localhost:9092").split(",")
raw_topic  = os.getenv("RAW_TOPIC", "raw-logs")

print(f"🔄 Single log fetcher starting: {raw_topic}", flush=True)

# 브로커 연결 대기
while True:
    try:
        consumer = KafkaConsumer(
            raw_topic,
            bootstrap_servers=brokers,
            group_id=None,  # 단일 fetcher라서 group_id 지정 안 함
            auto_offset_reset='earliest',
            enable_auto_commit=False,  # 커밋하지 않음 (한 번만 가져오기)
            value_deserializer=lambda b: json.loads(b)
        )
        print("✅ Connected to Kafka brokers:", brokers, flush=True)
        break
    except NoBrokersAvailable:
        print("⚠️  Kafka brokers not available, retrying in 5s...", file=sys.stderr, flush=True)
        time.sleep(5)

# 메시지 한 개 가져오기
try:
    msg = next(consumer)
    raw_log = msg.value
    print("▶ [INFO] Fetched raw log:", raw_log, flush=True)
except StopIteration:
    print("⚠️  No messages available.", flush=True)
finally:
    consumer.close()
