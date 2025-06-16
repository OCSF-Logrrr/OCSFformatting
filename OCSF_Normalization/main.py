# main.py

import json
import asyncio
from app.stream_loop import stream_logs
from app.classifier import predict_class
from app.mapping import normalize_log
from app.kafka_handler import send_to_kafka

CONCURRENT_TASKS = 10  # LLM requests to process at the same time

async def process_log(raw_log, semaphore):
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
            send_to_kafka(json.dumps(ocsf_log))


async def main():
    semaphore = asyncio.Semaphore(CONCURRENT_TASKS)
    tasks = []

    for raw_log in stream_logs():
        tasks.append(asyncio.create_task(process_log(raw_log, semaphore)))

        if len(tasks) >= CONCURRENT_TASKS:
            await asyncio.gather(*tasks)
            tasks = []

    if tasks:
        await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
