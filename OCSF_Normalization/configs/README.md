# ⚙️ configs 디렉토리 설명

`configs/` 디렉토리는 로그 수집 및 정규화 파이프라인의 설정 정보를 포함하며,  
Kafka 브로커 설정과 OCSF 클래스 매핑을 위한 키워드 사전 등이 정의되어 있습니다.

---

## 📁 구성 요소

| 파일명              | 설명 |
|---------------------|------|
| `kafka_config.py`   | Kafka 클러스터에 대한 연결 정보를 설정합니다. <br> - 원본 로그 수신용 토픽 (ex. `raw-logs`) <br> - OCSF 포맷으로 정규화된 로그 전송용 토픽 (ex. `ocsf-logs`) |
| `keyword.json`      | OCSF 클래스(`class_uid`)와 관련된 키워드 목록을 정의합니다. <br> - `classifier.py`에서 로그 내용에 포함된 키워드와 비교하여 클래스 판단 시 사용됩니다. |
| `__init__.py`       | Python 패키지 인식용 빈 파일입니다. |

---

## 🔧 kafka_config.py 주요 내용

```python
# 원본 로그 수신용 Kafka 클러스터 설정
INPUT_KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
INPUT_KAFKA_TOPIC = "raw-logs"
INPUT_GROUP_ID = "ocsf-mapper-group"

# 정규화된 로그 전송용 Kafka 설정
OUTPUT_KAFKA_BOOTSTRAP_SERVERS = "localhost:9092"
OUTPUT_KAFKA_TOPIC = "ocsf-logs"
```

> 해당 설정은 `stream_loop.py` 및 `kafka_handler.py`에서 사용되며,  
> Kafka 브로커와 주고받을 토픽 및 그룹 ID를 정의합니다.

---

## 🧠 keyword.json 구성 방식

`keyword.json`은 각 OCSF 클래스(`class_uid`)별로 관련 키워드 리스트를 정의하여,  
`classifier.py`에서 로그 내 키워드를 기반으로 클래스를 자동 분류하는 데 활용됩니다.

### 예시:
```json
"1001": {
  "class_name": "File System Activity",
  "keywords": ["file created", "file deleted", "chmod", "mv", "cp", "unlink"]
}
```

- 예를 들어, 로그에 `file deleted` 또는 `mv` 같은 키워드가 포함되면 `1001` 클래스에 해당한다고 판단합니다.

>  이 구조는 신규 클래스 추가 시도 및 탐지 정확도 개선을 위해 쉽게 확장할 수 있도록 설계되어 있습니다.

---

## 💡 활용 팁

- 새로운 로그 유형이 도입되면 `keyword.json`에 키워드를 추가하여 분류 정확도를 높일 수 있습니다.
- Kafka 클러스터 주소나 토픽은 배포 환경에 따라 `kafka_config.py`에서 쉽게 수정 가능합니다.
