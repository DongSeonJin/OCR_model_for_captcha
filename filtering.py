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
