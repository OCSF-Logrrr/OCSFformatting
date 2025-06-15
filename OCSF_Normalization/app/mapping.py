# app/mapping.py

from app.llm import call_llm
from app.schema_loader import load_class_json
import re
import json

def normalize_log(raw_log, class_uid) -> dict:
    schema = load_class_json(class_uid)

    prompt = f"""Given this raw log:

{raw_log}

And the following OCSF JSON schema:
{schema}

Convert the log into a JSON object that follows the schema.
Do NOT include code blocks, comments, or markdown.
Return only minified JSON (no pretty-print, no markdown, no escaping, no code block).

"""

    try:
        response = call_llm(prompt)
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "error": "JSON parsing failed",
            "response": response
        }
