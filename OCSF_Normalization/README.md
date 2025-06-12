# OCSF 정규화 컨테이너의 내부 디렉토리 구조

2025.06.12
```
project_root/
│
├── requirements.txt
│
├── main.py
│
├── app/
│   ├── __init__.py         # init
│   ├── classifier.py       # 로그가 어떤 클래스인지 판단
│   ├── enum_mapper.py      # enum 타입 매핑 지원
│   ├── kafka_handler.py    # kafka handling
│   ├── llm.py              # llm 사용 정보 관리
│   ├── mapping.py          # 실질적인 필드 매핑 진행
│   ├── schema_loader.py    # class_schemas/ 에서 해당 클래스의 JSON 가져옴
│   └── stream_loop.py      # kafka에서 raw logs를 지속적으로 읽어와 main에 전달 
│
├── class_schemas/          # OCSF 클래스마다의 JSON 파일 저장되어 있음
│   └── ...
│
└── configs/
    └── ...

```
