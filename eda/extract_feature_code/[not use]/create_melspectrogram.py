import os
import shutil
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def check_wav_files(folder_path, result_folder):
    abnormal_files = []
    Mel_Spectrograms = []
    
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
                
                # Mel Spectrogram 만들기
                mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=512)
                mel_spect = librosa.power_to_db(mel_spect, ref=np.max)
                plt.figure(figsize=(10, 4)) # Mel Spectrogram 크기 설정
                librosa.display.specshow(mel_spect, y_axis='mel', x_axis='time')
                plt.title('Mel Spectrogram')
                plt.colorbar(format='%+2.0f dB')
                plt.tight_layout()

                # 이미지 파일로 저장
                count = len(Mel_Spectrograms)
                mel_spectrogram_file = os.path.join(result_folder, f'mel_spectrogram_{count}.png')
                plt.savefig(mel_spectrogram_file)
                Mel_Spectrograms.append(mel_spectrogram_file)

                plt.close()
                
            except Exception as e:
                # 예외 발생 시 이상한 파일로 간주하고 파일 목록에 추가
                print(f"Abnormal file detected: {filename} - {e}")
                abnormal_files.append(filename)
    
    return abnormal_files, total_files, normal_files, Mel_Spectrograms

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

    # 검사할 폴더 경로 설정
    folder_path = r'Mel Spectrogram을 만들고자 하는 .wav파일들이 존재하는 디렉토리의 경로를 입력해주시면 됩니다.'

    # Mel Spectrogram 결과저장 폴더 생성 (changed)
    result_folder = os.path.join(folder_path, "Mel_Spectrogram_Result")
    os.makedirs(result_folder, exist_ok=True)

    # 이상한 파일 검출 및 결과 출력
    abnormal_files, total_files, normal_files, Mel_Spectrograms = check_wav_files(folder_path, result_folder)

    print("Total number of files:", total_files)
    print("Number of normal files:", normal_files)
    print("Number of abnormal files:", len(abnormal_files))

    # 이상 파일이 존재한다면 새로운 디렉터리를 만들어서 별도 저장 (changed)
    if abnormal_files:
        print("\nAbnormal files detected:")
        for file in abnormal_files:
            print(file)
        save_abnormal_files(folder_path, abnormal_files)
        print("\nAbnormal files have been saved in 'Check_Result' folder.")
    else:
        print("\nNo abnormal files detected.")
        

    # Mel spectrogram 파일들을 Mel_Spectrogram_Result 폴더에 저장
    for idx, file in enumerate(Mel_Spectrograms):
        src_file = file  
        dst_file = os.path.join(result_folder, f'mel_spectrogram_{idx}.png')  # 중복을 피하기 위해 idx를 사용하여 파일 이름 생성
        if src_file != dst_file:  # 동일한 파일이 아니라면 복사 수행
            shutil.copyfile(src_file, dst_file)


if __name__ == "__main__":
    main()