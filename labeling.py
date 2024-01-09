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


    