## OCSF Log Formatter

---

### Overview
이 레포지토리는 Elasticsearch에서 로그를 수집하고, 이를 OCSF(Open Cybersecurity Schema Framework) 스키마에 맞춰 변환하기 위한 Python 스크립트를 포함하고 있습니다.

#### 구성 요소
```python
.
├── getlog.py        # Elasticsearch에서 로그 수집 및 출력
├── mapping.yaml     # (예정) OCSF 클래스 및 필드 매핑 정의 파일
├── format.py        # (예정) OCSF 스키마에 맞춘 로그 포맷터
├── requirements.txt # 필요한 Python 라이브러리 명세
└── changelog.md     # getlog.py 변경 이력 문서
```

---

#### 설치 방법
Python 3.x 환경에서 아래 의존성 설치:
  
  ```bash
  pip3 install elasticsearch
  ```

---

#### 사용 방법
1. getlog.py는 HTTPS로 Elasticsearch에 접속합니다. 다음 항목을 확인하세요:
  ca.crt: 인증서 파일 경로
  basic_auth: ID와 비밀번호
  host: https://your-es-endpoint:9200

2. 실행:
  ```bash
  python3 getlog.py
  ```

---

#### 개발 예정
- 인증서 처리 방식 개선 (도커 컨테이너의 인증서 접근에 관한 사항 수정)
- format.py: 로그를 OCSF 클래스에 맞춰 변환
- mapping.yaml: Windows/Linux 이벤트 ID → OCSF 클래스 매핑 정의
- 로그를 파일로 저장하거나, 외부 시스템으로 재전송

