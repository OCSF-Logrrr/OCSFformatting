# app/stream_loop.py

import logging
from app.kafka_handler import receive_log

logging.basicConfig(level=logging.INFO)

async def stream_logs():
    logging.info("Started raw log streaming from Kafka...")

    while True:
        raw_log = receive_log()
        if raw_log:
            yield raw_log
