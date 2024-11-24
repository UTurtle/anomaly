##### Challenge:

---

This is a record of the challenges that I'm personally doing.

---

# DCASE 2024 Task 2: First-Shot Unsupervised Anomalous Sound Detection

## Overview

The **DCASE 2024 Task 2** focuses on developing an **Anomalous sound detection (ASD)** is the task of identifying whether the sound emitted from a target machine is normal or anomalous. Automatic detection of mechanical failure is an essential technology in the fourth industrial revolution, which involves artificial-intelligence-based factory automation. Prompt detection of machine anomalies by observing sounds is useful for monitoring the condition of machines. Figure 1 shows an overview of the detection system.

![task2_unsupervised_detection_of_anomalous_sounds_01](https://github.com/user-attachments/assets/f4715132-290a-4fc8-bc6c-3fe18d23a4d3)
*Figure 1: Overview of ASD system.*

- [Description](https://dcase.community/challenge2024/task-first-shot-unsupervised-anomalous-sound-detection-for-machine-condition-monitoring)
- [DCASE2025](https://ossified-ox-0b0.notion.site/DCASE2025-117958188bc680f5a63cf112d4e5be99)

---

##### TODO
- EDA (Exploratory Data Analysis)
  - using `eda/notebook/playground/eda_playground complete.ipynb`
    - [ ] make `audio_pair_notes.json`. has attribute `same note` and `difference note`
    - [ ] add write `difference note` and `same note` in `eda_playground complete pair.ipynb` 

##### directory structure

- anomaly
  - datasets
    - dev
    - eval_2024
  - eda
    - extract_feature_code
    - notebook
      - playground (*)
    - unziped (same datasets but has feature extracted files)
      - dev
      - eval_2024s
  - model


---

### EDA setup

1. setup new python(or conda) enviroment and `pip install -r requirements.txt`. 
2. setup datasets folder `datasets` and `unziped`
3. dataset attributes_00.csv is broken. please use `eda/notebook/dataset_attributes_00_rebuild.ipynb`.
4. execute `eda/extract_feature_code/extract_feature.ipynb`. will make extract features
5. Finally, we can use `eda/notebook/playground/eda_playground complete.ipynb`.