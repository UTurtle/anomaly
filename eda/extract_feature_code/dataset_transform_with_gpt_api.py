import json
import os
import time
import shutil
from openai import OpenAI
client = OpenAI()



# 원본 JSON 파일 경로
AUDIO_FEATURES_JSON = "../../extract_feature_code/audio_features.json"

# 노트 정보가 담긴 JSON 파일 경로
AUDIO_FEATURES_NOTE_JSON = "../../extract_feature_code/audio_features_note_transform.json"

# 백업을 위한 원본 파일 복사 경로
BACKUP_JSON = "../../extract_feature_code/audio_features_backup.json"



api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    print("api found")
else:
    print("api key not found")

# Set your OpenAI API key

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
        print(translated_text)
        return translated_text
    except Exception as e:
        print(f"실패했습니다. 에러: {e}")
        return ""


def translate_notes_in_json(input_file, output_file, max_entries=None):
    with open(input_file, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    
    audio_features = data.get("audio_features", [])
    
    # Filter out entries with empty 'note' fields
    non_empty_features = [feature for feature in audio_features if feature.get('note', '').strip()] # 빈 노트는 건너뜀
    
    translated_data = []

    count = 0
    for idx, feature in enumerate(non_empty_features):
        if max_entries and idx >= max_entries:
            break
        
        note = feature.get('note', '').strip()
        translated_note = translate_text(note)
        feature['note'] = translated_note  # Update the note with the translated text
        translated_data.append(feature)
        print(f"Translated note for file {feature.get('file_path', '')}")

        count+=1
        print(f"count: {count}")
    
    # Save the translated data into the output_file
    with open(output_file, 'w', encoding='utf-8') as outfile:
        json.dump({"audio_features": translated_data}, outfile, ensure_ascii=False, indent=4)
    
    print(f"Translated data has been saved to {output_file}")




if __name__ == "__main__":
    try:
        # 번역 수행
        input_json = "audio_features_note.json"
        output_json = "audio_features_note_transform.json"
        translate_notes_in_json(input_json, output_json, max_entries=None)

    except Exception as e:
        print(f"프로그램 실행 중 오류 발생: {e}")
