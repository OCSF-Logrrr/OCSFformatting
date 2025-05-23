## 📝 OCSF formatting 변경 이력 (OCSFformatting Changelog)
이 문서는 OCSF 매핑 과정과 진행 상황에 대한 변경 내역을 관리합니다.
변경된 날짜, 주요 내용, 이유를 타임라인 형식으로 정리합니다.

### 📅 2025-05-22
#### 1) [getlog.py 업로드]
- **내용:**
  - Elasticsearch에서 python 코드를 이용해 로그를 가져오는 py 파일을 업로드.

- **사용 방법:**
  ```bash
  pip3 install elasticsearch

  python3 getlog.py
  ```

- **작동 방식:**
  주석 참고
  elasticsearch에 접속하여 index에 따라 어떤 로그를 가져올지, size에 따라 몇 개의 로그를 가져올지 정할 수 있다.

- **수정 & 추가해야 할 사항:**
  - 인증서 관련 설정
    현재는 단순히 도커 컨테이너의 인증서를 복사해서 접근권한을 준 것이기 때문에, 실제 서버에서는 다른 방식을 적용해야 함

  - OCSF 매핑 코드 작성
    로그를 가져오는 것은 인증서 설정이 완료되면 정상 작동.
    가져온 로그를 OCSF 스키마에 맞게 매핑해주는 코드 필요.
