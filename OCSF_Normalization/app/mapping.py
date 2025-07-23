# app/mapping.py

from app.llm import call_llm
from app.schema_loader import load_class_json
import re
import json
import time
import asyncio

async def normalize_log(raw_log, class_uid):
    schema = load_class_json(class_uid)

    pattern = r'^(\d+)\s+(\d+)\s+(eni-[a-f0-9]+|-)\s+([0-9.]+|-)\s+([0-9.]+|-)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)\s+(ACCEPT|REJECT|-)\s+(OK|NODATA|SKIPDATA|-)$'
    fields = ['version', 'account_id', 'interface_id', 'srcaddr', 'dstaddr', 'srcport', 'dstport', 'protocol', 'packets', 'bytes', 'start', 'end', 'action', 'log_status']

    for log_entry in raw_log:
        if log_entry == "message":
            match = re.match(pattern, log_entry.strip())
            if match:
                log_entry['message'] = dict(zip(fields, match.groups()))


    prompt = f"""
You are given a raw security log and a JSON schema that follows the OCSF (Open Cybersecurity Schema Framework).

Your task is to:
1. Extract relevant fields from the raw log.
2. Map them to the appropriate fields in the schema.
3. Output a valid, minified JSON string.

⚠️ Ensure all keys and all string values are enclosed in double quotes (").
⚠️ Do not escape the overall JSON string or wrap it in additional quotes.
⚠️ Output only a single line of valid JSON. No markdown, no comments, no code block.

Raw log:
{raw_log}

OCSF JSON schema:
{schema}
"""
    try:
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(None, call_llm, prompt)
        time.sleep(0.8) # consider
        return json.loads(response)

    except json.JSONDecodeError:
        return {
            "error": "JSON parsing failed",
            "response": response
        }
