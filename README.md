# 📦 OCSFformatting

OCSFformatting은 보안 로그를 [OCSF(Open Cybersecurity Schema Framework)](https://github.com/ocsf/ocsf-schema)에 기반한 통합 포맷으로 변환하는 Python 기반 자동화 도구입니다.  
로그를 받아와 적절한 클래스와 필드에 매핑하고, OCSF 스키마에 맞는 JSON 형식으로 출력합니다.

---

## ⚙️ 구성 요소

- `getlog`  
  Elasticsearch에 저장된 로그를 가져올 수 있는 파이썬 코드.  
  보통 디버깅이나 Elasticsearch에 어떻게 저장되어 있는지 확인하기 위헤 사용될 예정.  
  실제 프로젝트에선 사용하지 않을 예정.  

- `OCSF_Normalization/`  
  공식 OCSF 스키마 JSON 파일 디렉토리.  
  OCSF의 클래스마다 JSON 파일로 변환하여 저장.  
  공식 OCSF github엔, Object와 base_event 등이 따로 정리되어 있어, 우선 모두 한 파일에 작성 후에 프로젝트 진행에 따라 모듈화를 진행해볼 예정.  

---

## 📄 라이선스

이 프로젝트는 [Apache 2.0 License](LICENSE)를 따릅니다.
