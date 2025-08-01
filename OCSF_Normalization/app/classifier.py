# app/classifier.py

import json
import os
import math
import re


KEYWORDS_JSON_PATH = os.path.join("configs", "keyword_table.json")


with open(KEYWORDS_JSON_PATH, "r", encoding="utf-8") as f:
    ALL_KEYWORDS = json.load(f)


def predict_class(log: dict | str) -> int | None:
    if isinstance(log, dict):
        winlog = log.get("winlog")
        cloudtrail = log.get("tags")
        guardduty = log.get("detail-type")

        if winlog:
            event_id = int(winlog.get("event_id"))
            for class_uid, info in ALL_KEYWORDS.items():
                if event_id in info.get("event_id"):
                    return int(class_uid)


        elif cloudtrail != None and "cloudtrail" in cloudtrail:
            
            try:
                log_message = json.loads(log.get("message"))
                if log_message.get("sourceIPAddress"):
                    return 6003
                    
#                eventsource = log_message.get("eventSource")
#                eventname = log_message.get("eventName")

#                for class_uid, info in ALL_KEYWORDS.items():
#                    if eventsource + eventname in info.get("aws_keywords", []):
#                        return int(class_uid)
            except Exception as e:
                return 6005


        elif "GuardDuty" == guardduty:
            if str(log.get("detail").get("type"))[:6] == "Policy":
                return 2003
            else:
                return 2004


        else:
            pattern = r'^(\d+)\s+(\d+)\s+(eni-[a-f0-9]+|-)\s+([0-9.]+|-)\s+([0-9.]+|-)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)\s+(\d+|-)\s+(ACCEPT|REJECT|-)\s+(OK|NODATA|SKIPDATA|-)$'
            message = log.get('message')
            if message:
                matched = re.match(pattern, message.strip())
                if matched:
                    return 4001
                else:
                    return None

        log_text = json.dumps(log, ensure_ascii=False).lower()
    else:
        log_text = str(log).lower()


    if not log_text:
        return None

    match_scores = {}

    for class_uid, info in ALL_KEYWORDS.items():
        keywords = info.get("keywords", [])
        total_score = 0

        for rank, keyword in enumerate(keywords, start=1):
            idx = log_text.find(keyword.lower())
            if idx >= 0:
                position_ratio = idx / len(log_text)
                position_weight = math.exp(-2 * position_ratio)
                rank_weight = 1 / rank
                total_score += position_weight * rank_weight

        if total_score > 0:
            match_scores[class_uid] = total_score

    if match_scores:
        max_score = max(match_scores.values())
        candidates = [uid for uid, score in match_scores.items() if score == max_score]
        chosen = min(int(uid) for uid in candidates)
        return chosen

    return None
