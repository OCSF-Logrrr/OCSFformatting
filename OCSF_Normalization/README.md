# OCSF 정규화 컨테이너의 내부 디렉토리 구조

2025-05-31 초안
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
│   ├── enum_mapper.py      # 혹시 enum 타입 매핑이 잘 안 될 수도 있기에 예비로 넣어둠
│   ├── kafka_handler.py    # 카프카에서 원본 로그를 가져오고, 정규화 진행 후 다시 넣기
│   ├── llm.py              # llm 사용 정보 관리
│   ├── mapping.py          # 실질적인 필드 매핑 진행
│   └── schema_loader.py    # class_schemas/ 내부에서 해당 클래스의 JSON 가져옴
│
├── class_schemas/          # OCSF 클래스마다의 JSON 파일 저장되어 있음
│   └── ...
│
└── configs/
    └── ...

```
