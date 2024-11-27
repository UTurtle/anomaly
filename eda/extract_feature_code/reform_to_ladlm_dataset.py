import json
import os
from datasets import load_dataset, Features, Value, Dict, Audio, Image
import matplotlib.pyplot as plt
from PIL import Image as PILImage

features = Features({
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
    "explanation_about_spectrogram": Value("string"),  # Renamed 'note'
    "audio": Audio(sampling_rate=22050)
})


# Step 2: Load Dataset
dataset = load_dataset(
    'json',
    data_files='ladlm_dataset_view.json',
    field='ladlm_dataset_view',
    split='train',
    features=features
)

# Step 3: Add 'audio' field pointing to 'file_path'
def add_audio(example):
    example['audio'] = example['file_path']
    return example

dataset = dataset.map(add_audio)

# Step 4: Cast 'audio' column to Audio feature
dataset = dataset.cast_column("audio", Audio(sampling_rate=22050))

# Step 5: Add image data for spectrograms
def add_images(example):
    # Update 'linear_spectrogram_with_axes'
    spect_with_axes_path = example['linear_spectrogram_with_axes']['path']
    if os.path.exists(spect_with_axes_path):
        example['linear_spectrogram_with_axes']['image'] = spect_with_axes_path
    else:
        example['linear_spectrogram_with_axes']['image'] = None  # Handle missing images

    # Update 'linear_spectrogram_no_axes'
    spect_no_axes_path = example['linear_spectrogram_no_axes']['path']
    if os.path.exists(spect_no_axes_path):
        example['linear_spectrogram_no_axes']['image'] = spect_no_axes_path
    else:
        example['linear_spectrogram_no_axes']['image'] = None  # Handle missing images

    return example

dataset = dataset.map(add_images)

# Optional: Remove 'path' fields if no longer needed
def remove_image_paths(example):
    if 'path' in example['linear_spectrogram_with_axes']:
        del example['linear_spectrogram_with_axes']['path']
    if 'path' in example['linear_spectrogram_no_axes']:
        del example['linear_spectrogram_no_axes']['path']
    return example

dataset = dataset.map(remove_image_paths)

# Step 6: Inspect the first example
first_example = dataset[0]
print(first_example)

# Display 'linear_spectrogram_with_axes' image
spect_with_axes_image = first_example['linear_spectrogram_with_axes']['image']
if spect_with_axes_image:
    image = PILImage.open(spect_with_axes_image)
    plt.figure(figsize=(6, 4))
    plt.imshow(image)
    plt.title("Linear Spectrogram With Axes")
    plt.axis('off')
    plt.show()
else:
    print("No image found for 'linear_spectrogram_with_axes'.")

# Display 'linear_spectrogram_no_axes' image
spect_no_axes_image = first_example['linear_spectrogram_no_axes']['image']
if spect_no_axes_image:
    image = PILImage.open(spect_no_axes_image)
    plt.figure(figsize=(6, 4))
    plt.imshow(image)
    plt.title("Linear Spectrogram No Axes")
    plt.axis('off')
    plt.show()
else:
    print("No image found for 'linear_spectrogram_no_axes'.")

# Step 7: Save the dataset locally
dataset.save_to_disk('ladlm_dataset')

# Optional Steps: Push to Hugging Face Hub
# from huggingface_hub import login
# login(token='YOUR_TOKEN_HERE')  # Or use huggingface-cli login

# dataset.push_to_hub("your-username/ladlm-dataset-view")
