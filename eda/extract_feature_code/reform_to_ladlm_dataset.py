import os
import json
from datasets import load_dataset, Features, Value, Audio, Dataset
from datasets.features import Dict, Image
import matplotlib.pyplot as plt
from PIL import Image as PILImage

def define_features():
    return Features({
        "file_path": Value("string"),
        "file_name": Value("string"),
        "linear_spectrogram_with_axes": Dict({
            "image": Image(),
            "librosa_parameters": Dict({}),
            "plot_parameters": Dict({})
        }),
        "linear_spectrogram_no_axes": Dict({
            "image": Image(),
            "librosa_parameters": Dict({}),
            "plot_parameters": Dict({})
        }),
        "float_features": Dict({
            "zero_crossing_rate": Value("float"),
            "harmonic_to_noise_ratio": Value("float"),
            "spectral_flatness": Value("float"),
            "spectral_rolloff": Value("float"),
            "rms_energy": Value("float"),
            "entropy": Value("float"),
            "std": Value("float"),
            "avg": Value("float")
        }),
        "domain": Value("string"),
        "type": Value("string"),   
        "machineType": Value("string"),
        "explanation_about_spectrogram": Value("string"),
        "audio": Audio(sampling_rate=16000)
    })

def load_json_dataset(json_file, features):
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"The specified JSON file '{json_file}' does not exist.")
    
    with open(json_file, 'r') as f:
        data = json.load(f)['ladlm_dataset_view']
    
    return Dataset.from_dict(data, features=features)

def process_audio(dataset):
    def add_audio(example):
        file_path = example.get('file_path')
        if file_path and os.path.exists(file_path):
            example['audio'] = file_path
        else:
            example['audio'] = None
        return example
    
    return dataset.map(add_audio, num_proc=4)

def process_images(dataset):
    def add_images(example):
        # Update 'linear_spectrogram_with_axes'
        spect_with_axes_path = example['linear_spectrogram_with_axes'].get('path')
        if spect_with_axes_path and os.path.exists(spect_with_axes_path):
            example['linear_spectrogram_with_axes']['image'] = spect_with_axes_path
        else:
            example['linear_spectrogram_with_axes']['image'] = None

        # Update 'linear_spectrogram_no_axes'
        spect_no_axes_path = example['linear_spectrogram_no_axes'].get('path')
        if spect_no_axes_path and os.path.exists(spect_no_axes_path):
            example['linear_spectrogram_no_axes']['image'] = spect_no_axes_path
        else:
            example['linear_spectrogram_no_axes']['image'] = None

        return example
    
    dataset = dataset.map(add_images, num_proc=4)
    
    def remove_image_paths(example):
        example['linear_spectrogram_with_axes'].pop('path', None)
        example['linear_spectrogram_no_axes'].pop('path', None)
        return example
    
    return dataset.map(remove_image_paths, num_proc=4)

def visualize_sample(dataset, index=0):
    first_example = dataset[index]
    print(first_example)
    
    # Display 'linear_spectrogram_with_axes' image
    spect_with_axes_image = first_example['linear_spectrogram_with_axes']['image']
    if spect_with_axes_image:
        try:
            image = PILImage.open(spect_with_axes_image)
            plt.figure(figsize=(6, 4))
            plt.imshow(image)
            plt.title("Linear Spectrogram With Axes")
            plt.axis('off')
            plt.show()
        except Exception as e:
            print(f"Error loading 'linear_spectrogram_with_axes' image: {e}")
    else:
        print("No image found for 'linear_spectrogram_with_axes'.")
    
    # Display 'linear_spectrogram_no_axes' image
    spect_no_axes_image = first_example['linear_spectrogram_no_axes']['image']
    if spect_no_axes_image:
        try:
            image = PILImage.open(spect_no_axes_image)
            plt.figure(figsize=(6, 4))
            plt.imshow(image)
            plt.title("Linear Spectrogram No Axes")
            plt.axis('off')
            plt.show()
        except Exception as e:
            print(f"Error loading 'linear_spectrogram_no_axes' image: {e}")
    else:
        print("No image found for 'linear_spectrogram_no_axes'.")

def save_dataset(dataset, save_path='ladlm_dataset'):
    if os.path.exists(save_path):
        print(f"The directory '{save_path}' already exists. Overwriting...")
    dataset.save_to_disk(save_path)

def main():
    json_file = 'ladlm_dataset_view.json'
    features = define_features()
    dataset = load_json_dataset(json_file, features)
    dataset = process_audio(dataset)
    dataset = process_images(dataset)
    visualize_sample(dataset)
    save_dataset(dataset)

if __name__ == "__main__":
    main()
