# app/schema_loader.py

import os
import json

def load_class_json(class_number) -> dict:

    filename = f"{class_number}.json"
    filepath = os.path.join("../class_schemas", filename)

    if not os.path.exists(filepath):
        raise FileNotFoundError(f"JSON 파일이 존재하지 않습니다: {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)

    return data


# json_data = load_class_json(class_number)
# main.py에선 위 코드만 수행하면 json 파일 불러오기 가능
