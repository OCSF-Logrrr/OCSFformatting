from app.llm import call_llm
from app.schema_loader import load_all_schemas

def predict_class(log: str) -> str:
    """
    로그를 분석하여 가장 적절한 OCSF 클래스 이름을 예측합니다.
    
    :param log: 원본 로그 문자열
    :return: 예측된 클래스 이름 (예: "threat_detection")
    """
    schemas = load_all_schemas()
    class_names = "\n".join(schemas.keys())

    prompt = f"""Given the following log:

{log}

And the list of available OCSF class names:
{class_names}

Which class best fits the log above? Just return the class name only.
"""

    return call_llm(prompt)
