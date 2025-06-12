from app.llm import call_llm
from app.schema_loader import load_schema
import json

def normalize_log(log: str, class_name: str) -> dict:
    """
    로그를 지정된 OCSF 클래스 스키마에 따라 정규화된 JSON으로 변환합니다.
    
    :param log: 원본 로그 문자열
    :param class_name: 예측된 클래스 이름 (예: "threat_detection")
    :return: 정규화된 JSON 객체
    """
    schema = load_schema(class_name)

    prompt = f"""Given this raw log:

{log}

And the following OCSF JSON schema:
{json.dumps(schema, indent=2)}

Convert the log into a JSON object that follows the schema.
Return only the JSON output.
"""

    try:
        response = call_llm(prompt)
        return json.loads(response)
    except json.JSONDecodeError:
        return {
            "error": "JSON parsing failed",
            "response": response
        }
