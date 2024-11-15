import os
import shutil
import librosa

def check_wav_files(folder_path):
    abnormal_files = []

    # 폴더 내의 모든 파일에 대해 반복
    total_files = 0
    normal_files = 0
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        
        # 파일인지 확인
        if os.path.isfile(filepath) and filename.endswith('.wav'):
            total_files += 1
            try:
                # 파일을 로드하여 음악 데이터를 가져오기 시도
                y, sr = librosa.load(filepath, sr=None)
                normal_files += 1
            except Exception as e:
                # 예외 발생 시 이상한 파일로 간주하고 파일 목록에 추가
                print(f"Abnormal file detected: {filename} - {e}")
                abnormal_files.append(filename)
    
    return abnormal_files, total_files, normal_files


def save_abnormal_files(folder_path, abnormal_files):
    # Check_Result 폴더 생성
    result_folder = os.path.join(folder_path, "Check_Result")
    os.makedirs(result_folder, exist_ok=True)
    
    # 이상한 파일들을 Check_Result 폴더에 저장
    for file in abnormal_files:
        src_file = os.path.join(folder_path, file)
        dst_file = os.path.join(result_folder, file)
        shutil.copy(src_file, dst_file)



def main():

    classes = ['bearing', 'fan', 'gearbox', 'slider', 'ToyCar', 'ToyTrain', 'valve']
    data_type = ['test', 'train']

    for class_name in classes:
        for data in data_type:

            # 검사할 폴더 경로 설정
            folder_path = f'../../datasets/dev/{class_name}/{data}'

            # 이상한 파일 검출 및 결과 출력
            abnormal_files, total_files, normal_files = check_wav_files(folder_path)

            print(f"Checked Point : {folder_path}")
            print("Total number of files:", total_files)
            print("Number of normal files:", normal_files)
            print("Number of abnormal files:", len(abnormal_files))

            if abnormal_files:
                print("\nAbnormal files detected:")
                for file in abnormal_files:
                    print(file)
                save_abnormal_files(folder_path, abnormal_files)
                print("\nAbnormal files have been saved in 'Check_Result' folder.")
            else:
                print("\nNo abnormal files detected.")


if __name__ == "__main__":
    main()