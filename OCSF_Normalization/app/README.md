# 📦 app/ 디렉토리 설명

app 디렉토리 내부에 있는 파이썬 파일들을 각각 설명합니다.
해당 파일 내부에 있는 파일들은 일련된 과정을 거쳐 원본 로그를 OCSF 형태로 변환하여 다시 ELK 서버로 보냅니다.

`app/` 디렉토리는 로그 수집 → 분류(classify) → 정규화(mapping) → 전송까지의 전처리 핵심 로직을 포함합니다.  
Kafka를 통해 전달된 원본 로그를 OCSF 포맷으로 정규화하고, Elasticsearch로 전송하기 위한 준비 단계를 담당합니다.



---

## 🔄 로그 처리 흐름과 구성 요소 설명

Kafka로부터 수신한 원본 로그는 아래의 순서로 처리되어 OCSF 포맷으로 정규화된 후 다시 Kafka로 전송됩니다.  
각 단계별 역할을 담당하는 파이썬 파일은 다음과 같습니다:

| 순서 | 파일명             | 설명 |
|------|--------------------|------|
| ① 수신 | `stream_loop.py`     | Kafka에서 원본 로그를 지속적으로 읽어옵니다. |
| ② 분류 | `classifier.pyx`      | 로그를 분석해 어떤 OCSF 클래스(`class_uid`)인지 판단합니다. |
| ③ 스키마 로딩 | `schema_loader.py`   | 해당 클래스의 JSON 스키마를 `class_schemas/`에서 로딩합니다. |
| ④ 정규화 | `mapping.py`         | 불러온 스키마 기준으로 LLM을 이용하여 로그를 OCSF 포맷으로 정규화합니다. |
| ⑤ 전송 | `kafka_handler.py`   | 최종 정규화된 로그를 Kafka로 재전송합니다. |

> 🚨`class_schemas/` 폴더에는 OCSF 클래스별 스키마(JSON)가 정의되어 있으며,    
> 🚨`configs/keyword.json`은 `classifier.py`에서 키워드 기반 분류 기준으로 사용됩니다.

---


### 예시 로그 흐름

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
