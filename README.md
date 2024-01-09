# OCR model for bypass Captcha

이 프로젝트는 TensorFlow를 사용하여 구현된 Optical Character Recognition (OCR) 모델입니다.
주로 캡챠 이미지 데이터를 학습하여 자동으로 텍스트를 인식하고 입력하는데 사용됩니다. 모델은 CNNs, RNNs 및 CTC 손실을 결합하여 구현되었습니다.

Captcha 데이터를 학습한 OCR 모델을 파이썬 Selenium에 실 적용시킨 프로젝트 입니다.


### OCR model link
https://colab.research.google.com/drive/1cciryDMO2ptrcU2TP1mDsJb3MCc9Kx2m?usp=drive_link
* 구글 드라이브에 Captcha 데이터 약 1000개를 저장 후 위 colab 코드와 연동하여 훈련을 시킵니다.
* 데이터의 파일명에 정답을 기입하는 라벨링 작업도 필요합니다.
