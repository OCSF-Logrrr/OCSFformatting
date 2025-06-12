# 📦 app/ 디렉토리 설명

app 디렉토리 내부에 있는 파이썬 파일들을 각각 설명합니다.
해당 파일 내부에 있는 파일들은 일련된 과정을 거쳐 원본 로그를 OCSF 형태로 변환하여 다시 ELK 서버로 보냅니다.

---

## ⚙️ 구성 요소

- `classifier.py`   
  원본 로그를 분석하여 몇 번 클래스의 OCSF format인지 결정하는 기능

- `kafka_handler.py`  
  kafka에서 원본로그를 받아 오고, ocsf format으로 매핑된 로그를 kafka로 전달하는 기능

- `llm.py`   
  사용할 LLM 세팅

- `mapping.py`   
  LLM을 통해 실질적으로 OCSF 매핑을 수행

- `schema_loader.py`   
  사용할 class json 파일을 class_schemas/ 에서 가져오는 기능

- `stream_loop.py`
  kafka에 있는 raw logs를 지속적으로 읽어오는 기능

---
