# app/llm.py

import os
from openai import OpenAI

client = OpenAI(api_key="your-api-key)

def call_llm(log_data: str, temperature: float = 0.2) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a cybersecurity log normalization assistant."},
                {"role": "user", "content": log_data}
            ],
            temperature=temperature,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"[ERROR] LLM 호출 실패: {e}")
        return ""
