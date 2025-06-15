# 📦 app/ 디렉토리 설명

app 디렉토리 내부에 있는 파이썬 파일들을 각각 설명합니다.
해당 파일 내부에 있는 파일들은 일련된 과정을 거쳐 원본 로그를 OCSF 형태로 변환하여 다시 ELK 서버로 보냅니다.

`app/` 디렉토리는 로그 수집 → 분류(classify) → 정규화(mapping) → 전달까지의 전처리 핵심 로직을 포함합니다.  
Kafka를 통해 전달된 원본 로그를 OCSF 포맷으로 정규화하고, Elasticsearch로 전송하기 위한 준비 단계를 담당합니다.

---

## ⚙️ 구성 요소

- `classifier.py`   
  원본 로그를 분석하여 몇 번 클래스의 OCSF format인지 결정하는 기능

- `kafka_handler.py`  
  kafka에서 원본로그를 받아 오고, OCSF format으로 매핑된 로그를 kafka로 전달하는 기능

- `llm.py`   
  사용할 LLM 세팅

- `mapping.py`   
  LLM을 통해 OCSF 매핑 수행

- `schema_loader.py`   
  사용할 class json 파일을 class_schemas/ 에서 가져오는 기능

- `stream_loop.py`   
  kafka에 있는 로그를 지속적으로 읽어오는 기능

---

### 처리 흐름 순서 (예시)
1. `stream_loop.py`: Kafka에서 로그 스트리밍
2. `classifier.py`: 로그의 OCSF 클래스 판별
3. `schema_loader.py`: 클래스별 스키마 로딩
4. `mapping.py`: OCSF 포맷으로 정규화
5. `llm.py`: LLM 사용 시 후처리 또는 판단 보완
6. `kafka_handler.py`: Kafka로 최종 전송


##🔄 로그 처리 흐름과 구성 요소 설명
Kafka로부터 수신한 원본 로그는 아래의 순서로 처리되어 OCSF 포맷으로 정규화된 후 다시 Kafka로 전송됩니다. 각 단계별 역할을 담당하는 파이썬 파일은 다음과 같습니다:

① 수신	stream_loop.py	Kafka에서 원본 로그를 지속적으로 읽어오는 역할을 수행합니다.
② 분류	classifier.py	로그 내용을 분석하여 어떤 OCSF 클래스(class_uid)에 해당하는지 판단합니다.
③ 스키마 로딩	schema_loader.py	판별된 클래스에 해당하는 JSON 스키마를 class_schemas/ 디렉토리에서 로딩합니다.
④ 정규화	mapping.py	불러온 스키마를 기준으로 원본 로그를 OCSF 포맷으로 정규화합니다. 필요 시 LLM 결과를 반영합니다.
⑤ LLM 판단 (옵션)	llm.py	로그 의미가 불분명할 경우 LLM(GPT 등)을 사용하여 보조 판단을 수행합니다.
⑥ 전송	kafka_handler.py	최종적으로 OCSF 포맷으로 정규화된 로그를 Kafka에 재전송합니다.


3. 예시 로그 플로우 (입력 → 출력)

#### 예시 로그 흐름

#### 🟡 원본 로그 (입력)

Jun 14 18:22:00 ubuntu sshd[1483]: Accepted password for user1 from 192.168.0.1 port 51234 ssh2

#### 🟢 OCSF 정규화 결과 (출력)
```
json
{
  "class_uid": 3001,
  "class_name": "Authentication",
  "user": { "name": "user1" },
  "src_endpoint": { "ip": "192.168.0.1", "port": 51234 },
  "status": "Success"
}
```
