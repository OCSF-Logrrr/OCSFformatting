# app/mapping.py

from app.llm import call_llm
from app.schema_loader import load_class_json
import re
import json
import asyncio

async def normalize_log(raw_log, class_uid):
    schema = load_class_json(class_uid)

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
        return json.loads(response)

    except json.JSONDecodeError:
        return {
            "error": "JSON parsing failed",
            "response": response
        }
