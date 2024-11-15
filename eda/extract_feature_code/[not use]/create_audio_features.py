import os
import shutil
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np

def check_wav_files(folder_path, result_folder):
    abnormal_files = []
    features_files = []
    
    total_files = 0
    normal_files = 0
    for filename in os.listdir(folder_path):
        filepath = os.path.join(folder_path, filename)
        
        if os.path.isfile(filepath) and filename.endswith('.wav'):
            total_files += 1
            try:
                y, sr = librosa.load(filepath, sr=None)
                normal_files += 1

                base_name = os.path.splitext(filename)[0]
                audio_result_folder = os.path.join(result_folder, base_name)
                os.makedirs(audio_result_folder, exist_ok=True)

                plot_waveform(y, sr, audio_result_folder, base_name)
                plot_envelope(y, sr, audio_result_folder, base_name)
                plot_cepstrum(y, sr, audio_result_folder, base_name)

                mel_spect = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=1024, hop_length=512)
                mel_spect_db = librosa.power_to_db(mel_spect, ref=np.max)
                plot_and_save(mel_spect_db, sr, 'mel', audio_result_folder, base_name)
                
                mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
                plot_and_save(mfcc, sr, 'mfcc', audio_result_folder, base_name)
                
                linear_spect = np.abs(librosa.stft(y, n_fft=1024, hop_length=512))
                linear_spect_db = librosa.amplitude_to_db(linear_spect, ref=np.max)
                plot_and_save(linear_spect_db, sr, 'linear', audio_result_folder, base_name)

                chroma = librosa.feature.chroma_stft(y=y, sr=sr, n_fft=1024, hop_length=512)
                plot_and_save(chroma, sr, 'chroma', audio_result_folder, base_name)

                spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
                plot_and_save_1d(spectral_centroid, sr, 'spectral_centroid', audio_result_folder, base_name)

                spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y, sr=sr)
                plot_and_save_1d(spectral_bandwidth, sr, 'spectral_bandwidth', audio_result_folder, base_name)

                features_files.append({
                    "file": filename,
                    "feature_folder": audio_result_folder
                })

            except Exception as e:
                print(f"Abnormal file detected: {filename} - {e}")
                abnormal_files.append(filename)
    
    return abnormal_files, total_files, normal_files, features_files

def plot_and_save_1d(data, sr, feature_name, result_folder, base_name):
    plt.figure(figsize=(10, 4))
    times = librosa.times_like(data, sr=sr)
    plt.plot(times, data[0], label=feature_name)
    plt.title(feature_name.capitalize())
    plt.xlabel("Time (s)")
    plt.ylabel("Frequency (Hz)")
    plt.tight_layout()
    output_path = os.path.join(result_folder, f"{base_name}_{feature_name}.png")
    plt.savefig(output_path)
    plt.close()


def plot_waveform(y, sr, result_folder, base_name):
    plt.figure(figsize=(10, 4))
    librosa.display.waveshow(y, sr=sr)
    plt.title("Time-domain Waveform")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    output_path = os.path.join(result_folder, f"{base_name}_waveform.png")
    plt.savefig(output_path)
    plt.close()

def plot_envelope(y, sr, result_folder, base_name):
    plt.figure(figsize=(10, 4))
    envelope = np.abs(librosa.onset.onset_strength(y=y, sr=sr))
    times = librosa.times_like(envelope, sr=sr)
    plt.plot(times, envelope)
    plt.title("Envelope")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude")
    plt.tight_layout()
    output_path = os.path.join(result_folder, f"{base_name}_envelope.png")
    plt.savefig(output_path)
    plt.close()

def plot_cepstrum(y, sr, result_folder, base_name):
    plt.figure(figsize=(10, 4))
    spectrum = np.abs(librosa.stft(y))
    log_spectrum = np.log(spectrum + 1e-6)
    cepstrum = np.fft.ifft(log_spectrum, axis=0).real
    librosa.display.specshow(cepstrum, sr=sr, x_axis='time', y_axis='linear')
    plt.title("Cepstrum")
    plt.colorbar()
    plt.tight_layout()
    output_path = os.path.join(result_folder, f"{base_name}_cepstrum.png")
    plt.savefig(output_path)
    plt.close()

def plot_and_save(data, sr, feature_type, result_folder, base_name, y_axis='linear'):
    plt.figure(figsize=(10, 4))
    if feature_type == 'mel' or feature_type == 'linear':
        librosa.display.specshow(data, sr=sr, x_axis='time', y_axis='mel' if feature_type == 'mel' else y_axis)
    elif feature_type == 'mfcc' or feature_type == 'chroma':
        librosa.display.specshow(data, x_axis='time')
    elif feature_type == 'spectral_centroid' or feature_type == 'spectral_bandwidth':
        plt.semilogy(data.T, label=feature_type)
        plt.xlabel("Time")
        plt.ylabel("Hz")
    plt.colorbar(format='%+2.0f dB' if feature_type in ['mel', 'linear'] else None)
    plt.title(f'{feature_type.capitalize()}')
    plt.tight_layout()
    
    output_path = os.path.join(result_folder, f"{base_name}_{feature_type}.png")
    plt.savefig(output_path)
    plt.close()

def save_abnormal_files(folder_path, abnormal_files):
    result_folder = os.path.join(folder_path, "Check_Result")
    os.makedirs(result_folder, exist_ok=True)
    
    for file in abnormal_files:
        src_file = os.path.join(folder_path, file)
        dst_file = os.path.join(result_folder, file)
        shutil.copy(src_file, dst_file)

def main():

    classes = ['bearing', 'fan', 'gearbox', 'slider', 'ToyTrain', 'ToyCar', 'valve']
    data_type = ['test', 'train']

    for class_name in classes:
        for data in data_type:

            # Type Folder's Path
            folder_path = f'../../datasets/dev/{class_name}/{data}'
            result_base_path = f'../unziped/dev/{class_name}/{data}'

            print(f'Current Work Directory : {folder_path}')

            result_folder = os.path.join(result_base_path, "Feature_Extraction_Results")
            os.makedirs(result_folder, exist_ok=True)

            abnormal_files, total_files, normal_files, features_files = check_wav_files(folder_path, result_folder)

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
                
            for feature in features_files:
                print(f"\nFeatures extracted for '{feature['file']}' are saved in folder: {feature['feature_folder']}")

if __name__ == "__main__":
    main()
