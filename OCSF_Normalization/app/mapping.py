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
2. Map them to the appropriate fields in the schema, but ignore any existing 'metadata' field defined in the schema.
3. Construct a top-level 'metadata' object with the following fields, extracting from the raw log when possible or generating defaults:
    - 'product': An object with:
        - 'name': the name of the product or tool that generated the log. Try to extract from raw_log. If the log is from AWS CloudTrail, use the value from userAgent. Otherwise, extract relevant name-like information, e.g., "aws-cli".
        - 'uid': the infrastructure identifier (host ID, agent ID, etc.) if present in raw_log. If not present, generate a UUID.
    - 'log_provider': the source of the log (e.g., "AWS CloudTrail", "Sysmon"). Extract from raw_log.
    - 'version': the version of the log format or system. Use '1.0.0' if missing.
    - 'original_time': the original event timestamp. Extract from raw_log and format in ISO 8601 (e.g., "2025-07-29T04:20:00Z").
    - 'logged_time': the current UTC time in ISO 8601 format. Generate at runtime.
    - 'log_name': a short descriptive name for the type of log, inferred from raw_log (e.g., "firewall_denied", "iam_access", "dns_request").
    - 'uid': a unique identifier for the log event. Extract from raw_log if present, else generate a UUID.

⚠️ Ignore any existing metadata fields in the schema. Use only raw_log to extract or derive values.
4. If the raw log contains a current working directory (e.g., 'cwd=...'), map it to 'actor.process.working_directory'.

⚠️ Output requirements:
- You **MUST** include the "class_uid" field exactly as defined in the schema.
- Output a valid, minified JSON string.
- Use double quotes for all keys and string values.
- Do not wrap or escape the entire JSON output.
- Output only a single line of valid JSON. No markdown, comments, or code blocks.
- Use ISO 8601 format for timestamps.
- Omit metadata fields if they cannot be extracted or generated.

Raw log:
{raw_log}

OCSF JSON schema (ignore the 'metadata' field in this schema):
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
