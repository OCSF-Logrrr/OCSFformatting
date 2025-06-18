# main.py

import json
import asyncio
from app.stream_loop import stream_logs
from app.classifier import predict_class
from app.mapping import normalize_log
from app.kafka_handler import send_to_kafka

CONCURRENT_TASKS = 10

async def process_log(raw_log, semaphore, kafka_lock):
    try:
        log_data = json.loads(raw_log)
    except json.JSONDecodeError:
        return

    class_uid = predict_class(log_data)
    if not class_uid:
        return

    async with semaphore:
        ocsf_log = await normalize_log(log_data, class_uid)
        if ocsf_log:
            async with kafka_lock:
                send_to_kafka(ocsf_log)


async def main():
    semaphore = asyncio.Semaphore(CONCURRENT_TASKS)
    kafka_lock = asyncio.Lock()
    tasks = set()

    for raw_log in stream_logs():
        task = asyncio.create_task(process_log(raw_log, semaphore, kafka_lock))
        tasks.add(task)
        task.add_done_callback(tasks.discard)

        if semaphore._value == 0:
            await asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED)

    if tasks:
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
