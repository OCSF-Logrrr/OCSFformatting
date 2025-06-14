# app/llm.py

import openai

# API 키 설정 (환경변수로 처리 권장)
openai.api_key = "your-api-key"

def call_llm(prompt: str, temperature: float = 0.2) -> str:
    """
    GPT 모델에 프롬프트를 전송하고 응답을 문자열로 반환합니다.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a cybersecurity log classification assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
    )
    return response['choices'][0]['message']['content'].strip()
