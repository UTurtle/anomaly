# 오디오 특징 정리 및 저장 가이드

---

## 개요

본 문서에서는 정상(Normal)과 이상(Anomaly) 데이터에 대해 추출된 오디오 특징들을 정리하고, 이를 효과적으로 저장하기 위한 JSON 포맷을 제안합니다. 또한, 각 특징의 설명과 용도에 대해 상세히 다룹니다.

---

## 추출된 오디오 특징 목록

### 1. **Time-Domain Waveform**

![Time-Domain Waveform](https://prod-files-secure.s3.us-west-2.amazonaws.com/988a1a27-53ef-429d-9eab-b39d2d4d4536/42b82507-1e9a-4ac5-811d-d2125f83597e/section_00_source_test_anomaly_0001_pro_A_vel_4_loc_A_waveform.png)

- **설명**: 시간에 따라 변화하는 신호의 진폭을 시각화한 것입니다.
- **용도**: 신호의 전반적인 형태, 파형의 주기성 또는 비주기성을 판단하는 데 유용합니다. 예를 들어, 소음과 같은 불규칙 신호와 음성과 같은 규칙 신호를 구별하는 데 사용됩니다.

### 2. **Envelope**

![Envelope](https://prod-files-secure.s3.us-west-2.amazonaws.com/988a1a27-53ef-429d-9eab-b39d2d4d4536/1031caff-c9f0-43de-955b-1d2e1afe0ad6/section_00_source_test_anomaly_0001_pro_A_vel_4_loc_A_envelope.png)

- **설명**: 신호의 강도 변화를 시각화한 것으로, 주로 진폭의 외곽선을 따라가는 패턴을 보여줍니다.
- **용도**: 에너지나 볼륨의 변화를 확인하는 데 유용하며, 음성, 음악 등의 에너지 변화를 추적하고 유사한 음향을 그룹화하는 작업에 활용됩니다.

### 3. **Cepstrum**

![Cepstrum](https://prod-files-secure.s3.us-west-2.amazonaws.com/988a1a27-53ef-429d-9eab-b39d2d4d4536/c51d6513-41be-44e6-89c6-c9377cc2abbf/section_00_source_test_anomaly_0001_pro_A_vel_4_loc_A_cepstrum.png)

- **설명**: 로그 스펙트럼의 역푸리에 변환을 통해 얻은 주파수의 스펙트럼으로, 신호의 피치와 포만트 정보를 포함합니다.
- **용도**: 음성 분석에서 목소리의 피치와 음색을 구별하는 데 사용됩니다. 예를 들어, 발화자의 음색을 분석하는 연구에 활용됩니다.

### 4. **Mel Spectrogram**

![Mel Spectrogram](https://prod-files-secure.s3.us-west-2.amazonaws.com/988a1a27-53ef-429d-9eab-b39d2d4d4536/9d8300e6-42bb-4ad3-acae-0e969cde074c/section_00_source_test_anomaly_0001_pro_A_vel_4_loc_A_mel.png)

- **설명**: 주파수 정보를 멜 스케일로 변환하여 사람이 인지하는 주파수 대역에 맞게 시각화한 스펙트로그램입니다.
- **용도**: 음성 및 음악에서 중요한 주파수 대역을 시각화하고 분석하는 데 유용하며, 음성 인식, 음악 장르 분류 등에 자주 사용됩니다.

### 5. **MFCC (Mel-Frequency Cepstral Coefficients)**

![MFCC](https://prod-files-secure.s3.us-west-2.amazonaws.com/988a1a27-53ef-429d-9eab-b39d2d4d4536/d8bd470f-8b4e-4807-9c5c-e3309fd997de/section_00_source_test_anomaly_0001_pro_A_vel_4_loc_A_mfcc.png)

- **설명**: Mel 스케일의 주파수 대역을 기반으로 Cepstrum을 계산한 것입니다. 주로 음성의 음색을 잘 나타냅니다.
- **용도**: 음성 인식, 화자 구별, 감정 분석 등 음성의 고유 특성을 분석하는 데 사용됩니다.

### 6. **Linear Spectrogram**

![Linear Spectrogram](https://prod-files-secure.s3.us-west-2.amazonaws.com/988a1a27-53ef-429d-9eab-b39d2d4d4536/8cab76e9-d2d9-45c9-bb96-bf8fe4dfd244/section_00_source_test_anomaly_0001_pro_A_vel_4_loc_A_linear.png)

- **설명**: 시간에 따른 주파수 구성 요소를 선형 스케일로 표현한 스펙트로그램입니다.
- **용도**: 일반적인 오디오 신호의 주파수 변화를 시각화하는 데 유용하며, 주파수 대역이 넓은 환경에서 소리를 분석하는 연구에서 많이 사용됩니다.

### 7. **Chroma Features**

![Chroma Features](https://prod-files-secure.s3.us-west-2.amazonaws.com/988a1a27-53ef-429d-9eab-b39d2d4d4536/fb06e786-a79d-4f64-a292-f5d9d2a0260e/section_00_source_test_anomaly_0001_pro_A_vel_4_loc_A_chroma.png)

- **설명**: 각 옥타브의 12개 음을 기준으로 주파수 정보를 그룹화하여 표시합니다.
- **용도**: 음악 장르 분석, 코드 감지, 음원 추적 등에 사용됩니다.

### 8. **Spectral Centroid**

![Spectral Centroid](https://prod-files-secure.s3.us-west-2.amazonaws.com/988a1a27-53ef-429d-9eab-b39d2d4d4536/5724aa8e-5a7a-4b7a-8898-a5514009b24d/section_00_source_test_anomaly_0002_pro_A_vel_4_loc_A_spectral_centroid.png)

- **설명**: 신호의 주파수 스펙트럼의 무게중심을 나타냅니다.
- **용도**: 소리의 밝기나 날카로움을 평가하는 데 사용되며, 음악 장르 분류와 같은 작업에서 소리의 명도나 음색을 비교할 때 활용됩니다.

### 9. **Spectral Bandwidth**

![Spectral Bandwidth](https://prod-files-secure.s3.us-west-2.amazonaws.com/988a1a27-53ef-429d-9eab-b39d2d4d4536/90b9d275-a6f5-4d82-914b-a4785e2fee96/section_00_source_test_anomaly_0002_pro_A_vel_4_loc_A_spectral_bandwidth.png)

- **설명**: 주파수 분포의 넓이를 나타냅니다.
- **용도**: 소리의 날카로움과 부드러움을 나타내며, 소리의 복잡성을 분석하는 데 사용됩니다.

### 10. **Zero-Crossing Rate (ZCR)**

- **설명**: 신호가 시간축을 기준으로 얼마나 자주 0을 통과하는지를 측정합니다.
- **용도**: 잡음 수준이나 음성의 특성을 파악하는 데 유용합니다. 무작위 잡음과 규칙적인 신호를 구분하는 데 사용됩니다.

### 11. **Harmonic-to-Noise Ratio (HNR)**

- **설명**: 신호의 조화 성분과 잡음 성분의 비율을 측정합니다.
- **용도**: 신호의 품질을 평가하고, 신호 내 잡음의 양을 파악하는 데 사용됩니다. 높은 HNR은 신호가 깨끗함을 나타냅니다.

### 12. **Spectral Flatness**

- **설명**: 스펙트럼의 평탄도를 측정하여 신호가 노이즈에 가까운지, 톤에 가까운지를 나타냅니다.
- **용도**: 톤과 노이즈 신호를 구분하는 데 유용하며, 음악 신호에서는 화음과 같은 조화로운 패턴을 식별하는 데 사용됩니다.

### 13. **Spectral Rolloff**

- **설명**: 스펙트럼의 에너지 누적 비율이 특정 임계값(예: 85%)에 도달하는 주파수 지점을 측정합니다.
- **용도**: 신호의 고주파 성분을 파악하여 소리의 밝기나 날카로움을 평가하는 데 사용됩니다.

### 14. **Root Mean Square (RMS) Energy**

- **설명**: 신호의 에너지 수준을 측정하는 지표로, 신호의 제곱 평균의 제곱근을 계산합니다.
- **용도**: 신호의 강도 변화를 추적하고, 에너지 기반의 이벤트 감지에 사용됩니다.

### 15. **Wavelet Transform**

- **설명**: 시간-주파수 분석을 위해 웨이블릿 변환을 적용하여 다양한 주파수 대역에서 신호의 특성을 추출합니다.
- **용도**: 신호의 다중 해상도 분석에 유용하며, 비정상적인 패턴이나 급격한 변화 감지에 사용됩니다.

### 16. **Power Spectrum**

- **설명**: 신호의 주파수 성분별 에너지 분포를 나타냅니다.
- **용도**: 신호의 주파수 특성을 분석하고, 특정 주파수 대역의 에너지 변화를 추적하는 데 사용됩니다.

### 17. **Entropy Measures**

- **설명**: 신호의 불확실성이나 복잡도를 측정합니다.
- **용도**: 신호의 정보량을 평가하고, 복잡한 신호 패턴을 식별하는 데 사용됩니다.

---

## JSON 저장 포맷 및 구조

데이터 페어(정상 및 이상) 분석을 효율적으로 수행하기 위해 JSON 파일의 구조를 체계적으로 설계합니다. 각 페어의 특성을 명확히 구분하고, 각 특성을 별도로 저장할 수 있도록 구조화합니다. 또한, 수기 노트를 추가할 수 있는 필드를 포함시킵니다.

### 권장 JSON 구조

```json
{
  "data_pairs": [
    {
      "pair_id": "pair_001",
      "normal_data": {
        "file_path": "path/to/normal_file_001.wav",
        "machine_type": "fan",
        "section": "00",
        "domain": "source",
        "features": {
          "waveform": "path/to/normal_file_001_waveform.png",
          "envelope": "path/to/normal_file_001_envelope.png",
          "cepstrum": "path/to/normal_file_001_cepstrum.png",
          "mel_spectrogram": "path/to/normal_file_001_mel.png",
          "mfcc": "path/to/normal_file_001_mfcc.png",
          "linear_spectrogram": "path/to/normal_file_001_linear.png",
          "chroma_features": "path/to/normal_file_001_chroma.png",
          "spectral_centroid": "path/to/normal_file_001_spectral_centroid.png",
          "spectral_bandwidth": "path/to/normal_file_001_spectral_bandwidth.png",
          "zero_crossing_rate": 0.012,
          "harmonic_to_noise_ratio": 0.75,
          "spectral_flatness": 0.3,
          "spectral_rolloff": 2800.0,
          "rms_energy": 0.05,
          "wavelet_transform": "path/to/normal_file_001_wavelet.png",
          "power_spectrum": "path/to/normal_file_001_power_spectrum.png",
          "entropy": 1.45
        },
        "handwrite": "Initial observations: Signal appears smooth with consistent energy levels."
      },
      "anomaly_data": {
        "file_path": "path/to/anomaly_file_001.wav",
        "machine_type": "fan",
        "section": "00",
        "domain": "source",
        "features": {
          "waveform": "path/to/anomaly_file_001_waveform.png",
          "envelope": "path/to/anomaly_file_001_envelope.png",
          "cepstrum": "path/to/anomaly_file_001_cepstrum.png",
          "mel_spectrogram": "path/to/anomaly_file_001_mel.png",
          "mfcc": "path/to/anomaly_file_001_mfcc.png",
          "linear_spectrogram": "path/to/anomaly_file_001_linear.png",
          "chroma_features": "path/to/anomaly_file_001_chroma.png",
          "spectral_centroid": "path/to/anomaly_file_001_spectral_centroid.png",
          "spectral_bandwidth": "path/to/anomaly_file_001_spectral_bandwidth.png",
          "zero_crossing_rate": 0.025,
          "harmonic_to_noise_ratio": 0.60,
          "spectral_flatness": 0.45,
          "spectral_rolloff": 3100.0,
          "rms_energy": 0.08,
          "wavelet_transform": "path/to/anomaly_file_001_wavelet.png",
          "power_spectrum": "path/to/anomaly_file_001_power_spectrum.png",
          "entropy": 1.80
        },
        "handwrite": "Observed irregular spikes in the waveform and higher energy levels."
      }
    },
    // 추가 데이터 페어들...
  ]
}
