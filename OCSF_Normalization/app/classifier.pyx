# app/classifier.pyx

from libc.math cimport exp
from libc.string cimport strstr
from cpython.dict cimport PyDict_New, PyDict_SetItem
from cpython.unicode cimport PyUnicode_AsUTF8

import json
import os
cimport cython


KEYWORDS_JSON_PATH = os.path.join("configs", "keyword.json")

with open(KEYWORDS_JSON_PATH, "r", encoding="utf-8") as f:
    ALL_KEYWORDS = json.load(f)


@cython.boundscheck(False)
@cython.wraparound(False)
cpdef int predict_class(object log):
    cdef bytes log_bytes
    cdef dict match_scores = {}
    cdef str class_uid, keyword, uid
    cdef list keywords, candidates
    cdef double total_score, position_ratio, position_weight, rank_weight, max_score
    cdef int log_len, idx, rank, chosen, int_uid

    if isinstance(log, dict):
        log_values = ' '.join([str(v) for v in log.values()])
        log_bytes = log_values.lower().encode('utf-8')
    else:
        log_bytes = str(log).lower().encode('utf-8')

    if not log_bytes:
        return -1

    log_len = len(log_bytes)

    for class_uid, info in ALL_KEYWORDS.items():
        keywords = info.get("keywords", [])
        total_score = 0.0

        for rank, keyword in enumerate(keywords, start=1):
            keyword_b = keyword.lower().encode('utf-8')

            if strstr(log_bytes, keyword_b) != NULL:
                idx = log_bytes.find(keyword_b)
                position_ratio = idx / (log_len ** 0.5)
                position_weight = exp(-2.0 * position_ratio)
                rank_weight = 1.0 / rank
                total_score += position_weight * rank_weight

        if total_score > 0.0:
            match_scores[class_uid] = total_score

    if match_scores:
        max_score = max(match_scores.values())
        candidates = []

        for uid, score in match_scores.items():
            if score == max_score:
                candidates.append(uid)

        chosen = int(candidates[0])
        for uid in candidates:
            int_uid = int(uid)
            if int_uid < chosen:
                chosen = int_uid

        return chosen

    return -1
