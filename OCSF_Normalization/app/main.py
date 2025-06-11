# main.py
from kafka_handler import get_raw_log, send_to_logstash
from classifier import classify_log
from schema_loader import load_schema_json
from mapping import map_log_to_ocsf

def main():
    print("🔄 Transform Service Started")

    # 1️⃣ Kafka에서 원본 로그 1개 가져오기
    raw_log = get_raw_log()

    # 2️⃣ classifier.py → 클래스 번호 반환
    class_number = classify_log(raw_log)

    # 3️⃣ schema_loader.py → JSON 스키마 로드
    schema_json = load_schema_json(class_number)

    # 4️⃣ mapping.py → LLM 통해 OCSF 변환
    ocsf_log = map_log_to_ocsf(raw_log, schema_json)

    # 5️⃣ Kafka에 전송
    send_to_logstash(ocsf_log)

if __name__ == "__main__":
    main()
