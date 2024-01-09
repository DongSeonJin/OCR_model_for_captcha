from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tensorflow as tf
from tensorflow import keras
import numpy as np
import requests
import io



model_path = 'model_path'

# 모델 불러오기
model = keras.models.load_model(model_path)

def start_selenium():
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-blink-features=AutomationControlled') # 봇 접속 방지 회피
    options.add_experimental_option("detach", True) # 화면 꺼지지않고 유지

    # 페이지 로드 전략 설정 (로드를 기다리지 않음)
    options.page_load_strategy = 'none'

    # 크롬드라이버 자동 설치
    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service, options=options)

    print('크롬 드라이버 실행')
    driver.get('https://2captcha.com/demo/normal')


    captchaPng = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CLASS_NAME, "_2hXzbgz7SSP0DXCyvKWcha")))
    captcha_image_url = captchaPng.get_attribute('src')
    response = requests.get(captcha_image_url)
    image_bytes = io.BytesIO(response.content)

    answer = captcha_solve(image_bytes)
        
    print('정답은? :', answer)
    
    answer_field = driver.find_element(By.XPATH, '//*[@id="simple-captcha-field"]')
    answer_field.send_keys(answer)

    time.sleep(10)

    



def captcha_solve(image_bytes):
    global model

    max_length = 6
    img_width = 200
    img_height = 50
    image_path = image_bytes
    characters = ['5', '9', '2', '4', '0', '7', '3', '1', '6', '8']

    # 이미지 읽기 및 전처리 단계
    def preprocess_image_for_prediction(image_path):

        img = tf.io.decode_png(image_path.getvalue(), channels=1)
        img = tf.image.convert_image_dtype(img, tf.float32)
        img = tf.image.resize(img, [img_height, img_width])
        img = tf.transpose(img, perm=[1, 0, 2])
        img = tf.expand_dims(img, axis=0)  # 배치 차원 추가
        return img


    start_time = time.time()

    char_to_num = tf.keras.layers.StringLookup(
        vocabulary=list(characters), num_oov_indices=0, mask_token=None
    )

    num_to_char = tf.keras.layers.StringLookup(
        vocabulary=char_to_num.get_vocabulary(), num_oov_indices=0, mask_token=None, invert=True
    )

    prediction_model = keras.models.Model(
    model.get_layer(name='image').input, model.get_layer(name='dense2').output
    )


    def decode_predictions(pred):
        input_len = np.ones(pred.shape[0]) * pred.shape[1]
        results = keras.backend.ctc_decode(pred, input_length=input_len, greedy=True)[0][0][:, :max_length]
        output_text = []
        for res in results:
            res = tf.strings.reduce_join(num_to_char(res)).numpy().decode('utf-8')
            output_text.append(res)
        return output_text


    # 이미지 전처리 및 예측
    preprocessed_image = preprocess_image_for_prediction(image_path)
    preds = prediction_model.predict(preprocessed_image)
    pred_text = decode_predictions(preds)


    print("보안문자 푸는데 걸린시간 :", time.time() - start_time)

    return pred_text


start_selenium()