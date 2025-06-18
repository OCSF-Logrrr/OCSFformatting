# app/classifier.py

import json
import os
import math

KEYWORDS_JSON_PATH = os.path.join("configs", "keyword.json")

with open(KEYWORDS_JSON_PATH, "r", encoding="utf-8") as f:
    ALL_KEYWORDS = json.load(f)


def predict_class(log: dict | str) -> int | None:
    if isinstance(log, dict):
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
                position_ratio = idx / len(log_text)               # 0(앞쪽)~1(뒤쪽)
                position_weight = math.exp(-2 * position_ratio)    # λ=2 감쇠 계수
                rank_weight = 1 / rank

                total_score += position_weight * rank_weight

        if total_score > 0:
            match_scores[class_uid] = total_score

    if match_scores:
        # 점수가 같은 경우는 UID 작은 것 선택
        max_score = max(match_scores.values())
        candidates = [uid for uid, score in match_scores.items() if score == max_score]
        chosen = min(int(uid) for uid in candidates)
        return chosen

    return None
