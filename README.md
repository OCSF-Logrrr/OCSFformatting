## 📝 OCSF formatting 변경 이력 (OCSFformatting Changelog)
이 문서는 OCSF 매핑 과정과 진행 상황에 대한 변경 내역을 관리합니다.
변경된 날짜, 주요 내용, 이유를 타임라인 형식으로 정리합니다.

### 📅 2025-05-22
#### 1) [getlog.py 업로드]
- **내용:**
  - Elasticsearch에서 python 코드를 이용해 로그를 가져오는 py 파일을 업로드.

- **사용 방법:**
  python이 설치되어 있다는 전제하에 진행
  ```bash
  pip3 install elasticsearch

  python3 getlog.py
  ```

- **작동 방식:**
  주석 참고
  elasticsearch에 접속하여 index에 따라 어떤 로그를 가져올지, size에 따라 몇 개의 로그를 가져올지 정할 수 있다.
