# app/schema_loader.py

import os
import json

def load_class_json(class_number) -> dict:

    filename = f"{class_number}.json"
    filepath = os.path.join("class_schemas", filename)

    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data
