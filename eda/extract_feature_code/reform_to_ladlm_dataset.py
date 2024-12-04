import os
import json
from datasets import Dataset, Features, Value, Audio, Image, Sequence
import matplotlib.pyplot as plt
from PIL import Image as PILImage

def define_features():
    return Features({
        "file_path": Value("string"),
        "file_name": Value("string"),
        "linear_spectrogram_with_axes": {
            "path": Value("string"),
            "librosa_parameters": Features({
                "n_fft": Value("int32"),
                "hop_length": Value("int32"),
                "window": Value("string")
            }),
            "plot_parameters": Features({
                "figsize": Sequence(Value("string")),
                "dpi": Value("int32"),
                "file_format": Value("string")
            }),
            "image": Image()
        },
        "linear_spectrogram_no_axes": {
            "path": Value("string"),
             "librosa_parameters": Features({
                "n_fft": Value("int32"),
                "hop_length": Value("int32"),
                "window": Value("string")
            }),
            "plot_parameters": Features({
                "figsize": Sequence(Value("string")),
                "dpi": Value("int32"),
                "file_format": Value("string")
            }),
            "image": Image()
        },
        "float_features": {
            "zero_crossing_rate": Value("float32"),
            "harmonic_to_noise_ratio": Value("float32"),
            "spectral_flatness": Value("float32"),
            "spectral_rolloff": Value("float32"),
            "rms_energy": Value("float32"),
            "entropy": Value("float32"),
            "std": Value("float32"),
            "avg": Value("float32")
        },
        "domain": Value("string"),
        "type": Value("string"),
        "machineType": Value("string"),
        "explanation_about_spectrogram": Value("string"),
        "audio": Audio(sampling_rate=16000)  # Ensure this is included
    })

def load_json_dataset(json_file, features):
    if not os.path.exists(json_file):
        raise FileNotFoundError(f"The specified JSON file '{json_file}' does not exist.")
    
    with open(json_file, 'r') as f:
        data = json.load(f)['ladlm_dataset_view']
    
    # Ensure each example has the 'audio' field set to None initially
    for example in data:
        example['audio'] = None  # Initialize 'audio' field
    
    return Dataset.from_list(data, features=features)

def process_audio(example):
    file_path = example.get('file_path')
    if file_path and os.path.exists(file_path):
        example['audio'] = file_path  # Set to file path; Audio feature will handle decoding
    else:
        example['audio'] = None  # Ensure it's set to None if path doesn't exist
    return example

def process_images(example):
    # Update 'linear_spectrogram_with_axes'
    spect_with_axes = example.get('linear_spectrogram_with_axes', {})
    print(spect_with_axes)
    spect_with_axes_path = spect_with_axes.get('path')
    if spect_with_axes_path and os.path.exists(spect_with_axes_path):
        spect_with_axes['image'] = spect_with_axes_path  # Set to image path
    else:
        spect_with_axes['image'] = None  # Set to None if path doesn't exist
    spect_with_axes.pop('path', None)  # Remove the 'path' field
    print(spect_with_axes)
    example['linear_spectrogram_with_axes'] = spect_with_axes
    
    # Update 'linear_spectrogram_no_axes'
    spect_no_axes = example.get('linear_spectrogram_no_axes', {})
    spect_no_axes_path = spect_no_axes.get('path')
    if spect_no_axes_path and os.path.exists(spect_no_axes_path):
        spect_no_axes['image'] = spect_no_axes_path  # Set to image path
    else:
        spect_no_axes['image'] = None  # Set to None if path doesn't exist
    spect_no_axes.pop('path', None)  # Remove the 'path' field
    example['linear_spectrogram_no_axes'] = spect_no_axes
    
    return example

def visualize_sample(dataset, index=0):
    first_example = dataset[index]
    print(first_example)
    
    # Display 'linear_spectrogram_with_axes' image
    spect_with_axes_image = first_example['linear_spectrogram_with_axes']['image']
    if spect_with_axes_image:
        try:
            plt.figure(figsize=(6, 4))
            plt.imshow(spect_with_axes_image)  # Image feature should decode to PIL Image
            plt.title("Linear Spectrogram With Axes")
            plt.axis('off')
            plt.show()
        except Exception as e:
            print(f"Error displaying 'linear_spectrogram_with_axes' image: {e}")
    else:
        print("No image found for 'linear_spectrogram_with_axes'.")
    
    # Display 'linear_spectrogram_no_axes' image
    spect_no_axes_image = first_example['linear_spectrogram_no_axes']['image']
    if spect_no_axes_image:
        try:
            plt.figure(figsize=(6, 4))
            plt.imshow(spect_no_axes_image)  # Image feature should decode to PIL Image
            plt.title("Linear Spectrogram No Axes")
            plt.axis('off')
            plt.show()
        except Exception as e:
            print(f"Error displaying 'linear_spectrogram_no_axes' image: {e}")
    else:
        print("No image found for 'linear_spectrogram_no_axes'.")

def save_dataset(dataset, save_path='ladlm_dataset'):
    if os.path.exists(save_path):
        print(f"The directory '{save_path}' already exists. Overwriting...")
    dataset.save_to_disk(save_path)



# Call this function after processing images and audio
def main():
    json_file = 'ladlm_dataset_view.json'  # Ensure this is the updated JSON
    features = define_features()
    dataset = load_json_dataset(json_file, features)

    # Process audio and images
    dataset = dataset.map(process_audio, num_proc=4)
    dataset = dataset.map(process_images, num_proc=4)
    
    # Visualize a sample
    # visualize_sample(dataset)
    
    # Save the processed dataset
    save_dataset(dataset)



if __name__ == "__main__":
    main()
