from elasticsearch import Elasticsearch
import json

es = Elasticsearch(
    "https://localhost:9200",
    basic_auth=("user_id", "user_pwd"), # elasticsearch 접근 id, password를 순서대로 기입.
    ca_certs="/home/bishop/basic-elk/getlog/ca.crt" # 인증서 경로
    # 현재는 인증서를 도커에서 복사해온 후, 권한 제한을 풀어 (chmod +r) 진행.
    # 인증서에 관한 세부 설정은 추가로 진행해야 할 듯.
)

log_line = es.search(
    index="winlogbeat-*", # 인덱스 설정
    query={"match_all": {}},
    size=1, # 출력 개수 설정
    sort=[{"@timestamp": {"order": "desc"}}] # 로그를 최신 우선으로 가져옴.
)

for hit in log_line["hits"]["hits"]: # [][] -> elastic 검색 응답 구조
    print(json.dumps(hit["_source"], indent=2, ensure_ascii=False)) # 메타데이터 ("_id" 등) 제외

#for hit in log_line["hits"]["hits"]: # ["hits"]["hits"] -> elastic 검색 응답 구조
#    print(hit["_source"]) # 메타데이터 ("_id" 등) 제외


# 모두 출력할 거면 그냥 print하면 됨
# print(log_line)
