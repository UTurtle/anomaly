# How to Extract feature?

- 현재 지금 Data를 직접 두 눈으로 보고 스펙토그램과 소리를 들으면서 거기에 데이터에 대한 코멘트를 달고 있다.
- 해당 하는 데이터를 각 클래스 마다 10개씩 만들어서 이를 Llama 같은 모델에 fine tuning을 시킬 수 있지 않을까?



### Llama Fine Tuning - Multi Modal

1. Linear Spectrogram pair data
2. handwrite note
3. audio pair data

multi modal을 사용해서 실제로 Feature extraction이 가능한지 확인해보자.
처음에는 text + image
두 번째에는 audio + text + image 를 사용해서 데이터 pair끼리의 차이점을 분석할 수 있는지 확인해보자.

- spectrogram만으로는 보기 어려울 수 있으니 여러가지 feature를 더 알아보도록 하자.


---


