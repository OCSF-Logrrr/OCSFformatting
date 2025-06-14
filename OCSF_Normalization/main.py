# main.py

import json
from app.stream_loop import stream_logs
from app.classifier import predict_class
from app.schema_loader import load_class_json
from app.mapping import normalize_log
from app.kafka_handler import send_to_kafka

def main():
    for raw_log in stream_logs():
        try:
            log_data = json.loads(raw_log)
        except json.JSONDecodeError:
            continue

        class_uid = predict_class(log_data)
        
        ocsf_log = normalize_log(log_data, class_uid)
        
        if ocsf_log:
            send_to_kafka(ocsf_log)


if __name__ == "__main__":
    main()
