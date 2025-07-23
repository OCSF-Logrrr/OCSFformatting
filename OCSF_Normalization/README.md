# 📘 OCSF 기반 보안 로그 정규화 프로젝트

본 프로젝트는 다양한 시스템 환경에서 발생하는 로그를 **OCSF(Open Cybersecurity Schema Framework)** 표준 포맷으로 정규화하여,  
Elasticsearch에 저장하고 Kibana에서 시각화 및 탐지가 가능하도록 구성된 **보안 로그 분석 자동화 시스템**입니다.

---

## 🎯 프로젝트 개요

- **목표**: 이기종 시스템에서 수집된 원본 로그를 OCSF 스키마 기반으로 변환하고, 분석 가능한 형태로 전송
- **활용 스택**: Kafka, Python, Elasticsearch, Kibana, OCSF, LLM(GPT) 등
- **주요 기능**
  - 원본 로그 수신 및 분류
  - 원본 로그의 class_uid 판단
  - LLM을 이용하여 OCSF 스키마 기반 매핑
  - Kafka 연동 처리

---

## 🧩 디렉토리 구조

```
project_root/
│
├── app/
│   ├── __init__.py
│   ├── classifier.py       # 로그가 어떤 클래스인지 판단
│   ├── kafka_handler.py    # kafka handling
│   ├── llm.py              # llm 사용 정보 관리
│   ├── mapping.py          # 실질적인 필드 매핑 진행
│   ├── schema_loader.py    # class_schemas/ 에서 해당 클래스의 JSON 가져옴
│   └── stream_loop.py      # kafka에서 raw logs를 지속적으로 읽어와 main에 전달
│
├── class_schemas/          # OCSF 클래스마다의 JSON 파일 저장되어 있음
│   ├── __init__.py
│   └── ...
│
├── configs/
│   ├── __init__.py
│   ├── kafka_config.py
│   └── keyword.json
│
├── __init__.py
├── main.py
└── requirements.txt
```

---

## 🚀 실행 방법

```bash
# 가상환경 설정 (선택)
python3 -m venv venv
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt

# 실행
python main.py
```

Kafka 브로커가 사전에 실행되어 있어야 하며,  
`configs/kafka_config.py`에 브로커 및 토픽 설정이 정의되어 있습니다.

---

## 🔄 로그 처리 흐름 요약

1. Kafka에서 원본 로그 수신 (`stream_loop.py`)
2. 로그가 몇 번 OCSF 클래스인지 판단 (`classifier.py`)
3. 관련 JSON 스키마 로딩 (`schema_loader.py`)
4. 필드 정규화 및 매핑 (`mapping.py`)
5. LLM 모델 설정 (`llm.py`)
6. Kafka로 재전송 (`kafka_handler.py`)

---

## 💡 수정 / 확장 방법

- 새로운 OCSF 클래스 스키마는 `class_schemas/`에 JSON 형식으로 추가
- `keyword.json` 업데이트 시 클래스 번호와 관련 키워드 함께 등록
- PR 요청 시 설명과 예시 로그를 함께 남겨주세요

---

## 🛡️ 라이선스

MIT License
