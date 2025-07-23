# main.py

import json
import asyncio
from app.stream_loop import stream_logs
from app.classifier import predict_class
from app.mapping import normalize_log
from app.kafka_handler import send_to_kafka


CONCURRENT_TASKS = 10
SKIP_CLASSES = {None, -1, 1003, 1008, 1006, 5001, 5003, 5020, 5023}


async def process_log(raw_log, kafka_lock):
    try:
        log_data = json.loads(raw_log)
    except json.JSONDecodeError:
        print("Invalid JSON:", raw_log)
        return

    class_uid = predict_class(log_data)
    if class_uid in SKIP_CLASSES:
        return

    try:
        ocsf_log = await normalize_log(log_data, class_uid)
    except Exception as e:
        print("Error during normalization:", raw_log)
        return

    if ocsf_log:
        async with kafka_lock:
            try:
                await send_to_kafka(ocsf_log)
            except Exception as e:
                print("Error sending to Kafka:", raw_log)


async def main():
    semaphore = asyncio.Semaphore(CONCURRENT_TASKS)
    kafka_lock = asyncio.Lock()
    tasks = set()

    async for raw_log in stream_logs():
        await semaphore.acquire()

        async def worker(log_data=raw_log):
            try:
                await process_log(log_data, kafka_lock)
            finally:
                semaphore.release()

        task = asyncio.create_task(worker())
        tasks.add(task)
        task.add_done_callback(lambda t: tasks.discard(t))

    await asyncio.gather(*tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
