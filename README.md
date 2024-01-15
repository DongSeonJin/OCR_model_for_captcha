# OCR model for bypass Captcha

Captcha 데이터를 학습한 OCR 모델을 파이썬 Selenium에 실 적용시킨 프로젝트 입니다.

이 프로젝트는 Keras를 사용하여 구현된 Optical Character Recognition (OCR) 모델입니다.
캡챠 이미지 데이터를 학습하여 자동으로 텍스트를 인식하고 입력하는데 사용됩니다. 모델은 CNNs, RNNs 및 CTC 손실을 결합하여 구현되었습니다.



## OCR model link
OCR 모델은 하단의 colab 링크에 있습니다.

https://colab.research.google.com/drive/1cciryDMO2ptrcU2TP1mDsJb3MCc9Kx2m?usp=drive_link
* 구글 드라이브에 Captcha 데이터 약 1000개를 저장 후 위 colab 코드와 연동하여 훈련을 시킵니다.
* 데이터의 파일명에 정답을 기입하는 라벨링 작업 필요

## Test Result

![스크린샷 2024-01-10 061702](https://github.com/DongSeonJin/OCR_model_for_captcha/assets/129161266/ee873cea-e11c-4bb1-afd7-d0afdacef9cd)




### 약 1000개의 데이터를 수집하고서 일일이 손으로 힘들게 라벨링을 하면 많이 힘들겠죠?
```python
import os
from twocaptcha import TwoCaptcha

                                       # 이부분만 수정
api_key = os.getenv('APIKEY_2CAPTCHA', '2CAPTCHA_API_KEY')

solver = TwoCaptcha(api_key)

count = 0
for i in range(1000):
    count += 1

    file_name = f'captcha_image/{count}.png'

    result = solver.normal(f'captcha_image/{count}.png')

    try:
        captcha_solution = result['code']
    except:
        count -= 1
        continue

    new_file_name = f'captcha_image/{captcha_solution}.png'

    try:
        os.rename(file_name, new_file_name)
    except:
        os.remove(file_name)
        continue

    print(count, '번째 이미지 labeling 완료')
```
* 2captcha 라는 사이트의 api를 이용해 라벨링을 자동으로 수행해주는 파이썬 코드입니다. (labeling.py)
* 이 사이트의 api를 활용하여 captcha를 우회해도 괜찮지만, 한개 푸는데 10초 내외로 걸리고, 유료입니다. 
* 계정을 생성 후 API KEY를 위 코드에 기입해줍니다.
* 가격은 1000개당 1달러로 아주 저렴합니다.

```python
import os
import re


# 이미지가 저장된 디렉토리 경로
directory_path = 'captcha_image'

# 조건에 맞지 않는 파일명을 저장할 리스트
invalid_files = []


# 디렉토리 내의 모든 파일 탐색
for filename in os.listdir(directory_path):

    # 파일 확장자를 제외한 순수 파일명 추출
    pure_filename = os.path.splitext(filename)[0]

    # 파일명이 숫자로만 구성되어 있고, 길이가 6자리인지 확인
    if not re.fullmatch(r'\d{6}', pure_filename):
        invalid_files.append(filename)


count = 0
# 조건에 맞지 않는 파일명 출력
print("조건에 맞지 않는 파일들:")
for file in invalid_files:
    count += 1
    os.rename(f'{directory_path}/{file}', f'{directory_path}/{count}.png')
    print(file,'->', count, '.png', '로 변경 완료')

```
* 2captcha의 적중률은 높은편이지만 가끔씩 자릿수가 부족하다거나 오답이 나올때가 있습니다.
* filtering.py 는 파일명이 6자리 미만이거나 숫자가 아닌 문자열이 있을경우 파일명을 다시 1부터 설정하여 저장해줍니다.
* 그리고 다시 2captcha api로 라벨링 반복
