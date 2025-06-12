# configs/kafka_config.py

# 원본 로그를 수신할 Kafka 클러스터 설정
INPUT_KAFKA_BOOTSTRAP_SERVERS = "kafka1:9092,kafka2:9092,kafka3:9092"
INPUT_KAFKA_TOPIC = "raw-logs"
INPUT_GROUP_ID = "ocsf-mapper-group"

# 매핑된 로그를 전송할 Kafka 클러스터 설정
OUTPUT_KAFKA_BOOTSTRAP_SERVERS = "kafka1:9092,kafka2:9092,kafka3:9092"  # 또는 별도 클러스터
OUTPUT_KAFKA_TOPIC = "ocsf-logs"
