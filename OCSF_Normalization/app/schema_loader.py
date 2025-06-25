# app/schema_loader.py

import os
import json

def load_class_json(class_uid) -> dict:
    filename = f"{class_uid}.json"
    filepath = os.path.join("class_schemas", filename)

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {filepath}")

    except json.JSONDecodeError as e:
        raise ValueError(f"JSON decode error in {filepath}: {e}")

    except Exception as e:
        raise RuntimeError(f"Unexpected error loading {filepath}: {e}")

    return data
