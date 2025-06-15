# app/llm.py

import os
from openai import OpenAI

client = OpenAI(api_key="your key")

def call_llm(log_data: str, temperature: float = 0.2) -> str:
    prompt = f"""
    다음 로그를 OCSF 스키마에 따라 정규화된 JSON 형식으로 변환해줘.
    로그:
    {log_data}
    """

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a cybersecurity log normalization assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] LLM 호출 실패: {e}")
        return ""
