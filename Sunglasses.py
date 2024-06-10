# 필요한 패키지를 설치합니다.
!pip install opencv-python
!pip install opencv-python-headless
!pip install numpy
!pip install tensorflow

import numpy as np
import cv2
import tensorflow as tf
from matplotlib import pyplot as plt

# 이미지를 불러옵니다.
image_path = "WSU"  # 이미지 파일 경로를 지정해주세요.
image = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 모델을 로드합니다. (SSD 모델 사용)
model = tf.keras.applications.SSDMobileNetV2()
model.summary()  # 모델 구조를 출력합니다.

# 이미지 전처리
image_resized = cv2.resize(image_rgb, (300, 300))  # 모델 입력 크기에 맞게 이미지를 조정합니다.
image_expanded = np.expand_dims(image_resized, axis=0)  # 배치 차원을 추가합니다.
image_preprocessed = tf.keras.applications.mobilenet_v2.preprocess_input(image_expanded)  # 이미지를 전처리합니다.

# 객체 인식 수행
predictions = model.predict(image_preprocessed)

# 결과를 시각화합니다.
def draw_predictions(image, predictions):
    for result in predictions[0]:
        score = result[2]
        if score > 0.5:  # 신뢰도가 0.5 이상인 결과만 출력합니다.
            label = int(result[1])
            class_name = "Unknown"
            if label == 15:
                class_name = "Person"
            elif label == 3:
                class_name = "Car"
            # 결과를 이미지에 표시합니다.
            box = result[3:7] * np.array([image.shape[1], image.shape[0], image.shape[1], image.shape[0]])
            (startX, startY, endX, endY) = box.astype("int")
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, f"{class_name}: {score:.2f}", (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    plt.figure(figsize=(10, 10))
    plt.imshow(image)
    plt.axis('off')
    plt.show()

draw_predictions(image_rgb.copy(), predictions)
