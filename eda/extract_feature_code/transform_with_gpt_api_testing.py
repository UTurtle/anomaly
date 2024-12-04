import os
from openai import OpenAI
client = OpenAI()

api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print("api found")
else:
    print("api key not found")


def translate_text(text):
    if not text.strip():
        print("text의 내용이 비어있기 때문에 skip 됬습니다.")
        return ""  # Return empty string if note is empty
    
    prompt = f"Translate the following Korean text to English and look like expert:\n\n{text}"
    
    try:
        completion = client.chat.completions.create(
            model="gpt-4o-mini",  
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        # message.content를 사용하여 번역된 텍스트 추출
        translated_text = completion.choices[0].message.content
        return translated_text
    except Exception as e:
        print(f"실패했습니다. 에러: {e}")
        return ""

# 빈 텍스트 테스트
text = ""
output = translate_text(text)
print(output)

# 실제 텍스트 번역
text = "고주파수에서 앞뒤 1초의 강도가 매우 약함.\n저중주파수(2kHz, 3kHz)에서 0.5kHz 폭만큼 강도가 약해지는 구간 관측됨.\n스파이크 패턴이 비주기적으로 저주파수에서 고주파수까지 존재하나 높은 주파수일수록 강도가 점점 작아짐.\n고중주파수(6kHz-7kHz)에서 1kHz 폭만큼 강도가 약해지는 구간 관측됨."
output = translate_text(text)
print(output)
