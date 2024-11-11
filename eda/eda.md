
## Exploratory Data Analysis (EDA)

A comprehensive **Exploratory Data Analysis (EDA)** is essential to understand the dataset's characteristics, identify potential issues, and inform the modeling strategy. The EDA for DCASE 2024 Task 2 involves the following steps:

### 1. Data Loading and Structure

- **Objective**: Load training data exclusively from the **train** directory, ensuring no test data is included.
- **Approach**:
  - Read the `attributes_00.csv` file to extract `file_name` entries.
  - Construct complete file paths for each audio file based on the filenames.
  - Assign labels as 'normal' since only normal data is used for training.

### 2. Data Quality and Consistency

- **Objective**: Assess the consistency of audio files regarding sampling rates and durations.
- **Approach**:
  - Load each audio file using `librosa` and record its sampling rate and length.
  - Identify unique sampling rates and audio lengths.
  - Highlight inconsistencies to determine if resampling or padding/trimming is required.

### 3. Audio Waveform Visualization

- **Objective**: Visualize a subset of audio waveforms to understand the temporal characteristics of normal machine sounds.
- **Approach**:
  - Select a random sample of audio files from each machine type.
  - Plot the waveforms using `librosa.display.waveshow`.
  - Observe patterns, noise levels, and notable temporal features.

### 4. Spectrogram Analysis

- **Objective**: Examine the frequency-time representation of audio signals to understand their spectral properties.
- **Approach**:
  - Convert audio waveforms to spectrograms (e.g., Mel-spectrograms) using Short-Time Fourier Transform (STFT).
  - Compute the magnitude of the spectrograms.
  - Visualize average and standard deviation spectrograms to identify dominant frequency components and variability.
  - Assess key frequency bands relevant for anomaly detection.

### 5. Feature Extraction and Statistical Analysis

- **Objective**: Extract meaningful audio features to aid in distinguishing normal and anomalous sounds.
- **Approach**:
  - **MFCC (Mel-Frequency Cepstral Coefficients)**: Capture timbral aspects of audio.
  - **Spectral Centroid**: Indicates the "center of mass" of the spectrum.
  - **Zero-Crossing Rate**: Measures the rate at which the signal changes sign, reflecting noisiness.
  - **Additional Features**: Such as spectral bandwidth and roll-off.
  - Perform **Principal Component Analysis (PCA)** to reduce dimensionality and visualize feature distributions.
  - Analyze correlations between features and identify patterns or clusters.

### 6. Summary of EDA Findings

- **Sampling Rate Consistency**: Ensure all audio files share the same sampling rate or apply resampling as needed.
- **Audio Length Uniformity**: Apply padding or trimming to standardize audio durations across the dataset.
- **Spectral Characteristics**: Identify key frequency bands that consistently represent normal operation across different machine types.
- **Feature Distribution**: Understand the spread and clustering of features in reduced dimensional space to anticipate modeling challenges.

### 7. Data Preprocessing Recommendations

Based on EDA findings, implement the following preprocessing steps to prepare the data for modeling:

- **Resampling**: Convert all audio files to a uniform sampling rate (e.g., 22050 Hz).
- **Padding/Trimming**: Standardize audio lengths by padding shorter clips with zeros or trimming longer clips.
- **Normalization**: Normalize audio amplitudes to ensure consistent input for feature extraction.
- **Noise Reduction**: Apply noise reduction techniques if necessary to enhance signal quality.

### 8. Visualization Tools and Libraries

Utilize the following tools and libraries to perform EDA:

- **Librosa**: For audio loading, processing, and visualization.
- **Matplotlib** & **Seaborn**: For plotting waveforms, spectrograms, and feature distributions.
- **Pandas**: For handling CSV files and data manipulation.
- **Scikit-learn**: For performing PCA and other statistical analyses.

