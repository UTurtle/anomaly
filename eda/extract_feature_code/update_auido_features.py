import json
import os
import shutil

# -----------------------------
# 설정 파라미터
# -----------------------------

# 원본 JSON 파일 경로
AUDIO_FEATURES_JSON = "audio_features.json"

# 노트 정보가 담긴 JSON 파일 경로
AUDIO_FEATURES_NOTE_JSON = "audio_features_note_transform.json"

# 백업을 위한 원본 파일 복사 경로
BACKUP_JSON = "audio_features_backup.json"

# -----------------------------
# 함수 정의
# -----------------------------

def backup_file(original_file, backup_file):
    """
    원본 파일을 백업합니다.
    """
    try:
        shutil.copyfile(original_file, backup_file)
        print(f"백업 성공: {backup_file}")
    except Exception as e:
        print(f"백업 실패: {e}")
        raise

def load_json(file_path):
    """
    JSON 파일을 로드합니다.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"JSON 파일을 찾을 수 없습니다: {file_path}")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    return data

def update_notes(original_data, notes_data):
    """
    original_data의 각 항목에 notes_data의 note를 업데이트합니다.
    단, notes_data의 note가 빈 문자열("")인 경우 업데이트하지 않습니다.
    """
    # file_path를 키로 하는 딕셔너리 생성 (빠른 검색을 위해)
    notes_dict = { 
        os.path.normpath(entry['file_path']): entry['note'] 
        for entry in notes_data.get("audio_features", [])
    }
    
    updated_count = 0
    skipped_count = 0
    not_found = []
    
    for feature in original_data.get("audio_features", []):
        # 파일 경로 정규화 (운영체제에 따라 경로 구분자가 다를 수 있음)
        feature_path = os.path.normpath(feature.get("file_path", ""))
        
        if feature_path in notes_dict:
            new_note = notes_dict[feature_path]
            if new_note.strip():  # 새로운 노트가 빈 문자열이 아닌 경우에만 업데이트
                feature['note'] = new_note  # 노트 업데이트
                updated_count += 1
                # print(f"업데이트됨: {feature_path}")
            else:
                skipped_count += 1
                # print(f"건너뜀 (빈 노트): {feature_path}")
        else:
            not_found.append(feature_path)
    
    return updated_count, skipped_count, not_found

def save_json(data, file_path):
    """
    데이터를 JSON 파일로 저장합니다.
    """
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"업데이트된 JSON 파일이 저장되었습니다: {file_path}")

# -----------------------------
# 메인 실행 흐름
# -----------------------------

def main():
    # 1. 원본 파일 백업
    backup_file(AUDIO_FEATURES_JSON, BACKUP_JSON)
    
    # 2. JSON 파일 로드
    original_data = load_json(AUDIO_FEATURES_JSON)
    notes_data = load_json(AUDIO_FEATURES_NOTE_JSON)
    
    # 3. 노트 업데이트
    updated_count, skipped_count, not_found = update_notes(original_data, notes_data)
    
    # 4. 업데이트된 데이터 저장
    save_json(original_data, AUDIO_FEATURES_JSON)
    
    # 5. 결과 요약
    print(f"총 {updated_count}개의 항목이 업데이트되었습니다.")
    print(f"총 {skipped_count}개의 항목이 빈 노트로 인해 건너뛰어졌습니다.")
    if not_found:
        print(f"노트를 찾을 수 없는 파일 경로 ({len(not_found)}개):")
        for path in not_found:
            print(f" - {path}")

if __name__ == "__main__":
    main()
