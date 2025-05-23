from elasticsearch import Elasticsearch

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("usser_id", "user_password"), # elasticsearch 접근 id, password를 순서대로 기입.
    ca_certs="/home/kyoung/ELK/ca.crt"
    # 현재는 인증서를 도커에서 복사해온 후, 권한 제한을 풀어 (chmod +r) 진행.
    # 인증서에 관한 세부 설정은 추가로 진행해야 할 듯.
)

log_line = es.search(
    index="filebeat-*", # 인덱스 설정
    query={"match_all": {}},
    size=1 # 출력 개수 설정
)

for hit in log_line["hits"]["hits"]: # ["hits"]["hits"] -> elastic 검색 응답 구조
    print(hit["_source"]) # 메타데이터 ("_id" 등) 제외
    
    
# 모두 출력할 거면 그냥 print하면 됨
# print(log_line)
