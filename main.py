import cv2
import numpy as np
import cv2
from mss import mss

bounding_box = {'top': 30, 'left': 0, 'width': 800, 'height': 600}

sct = mss()
color_lines = (
    # H   S   V
    (22, 69, 224,),  # Минимальная граница значений
    (27, 227, 255),  # Максимальные значения
)
color_car = (
    # H   S   V
    (36, 95, 0,),  # Минимальная граница значений
    (65, 182, 255),  # Максимальные значения
)


# Функция обработки изображения
def process_img(img, name, color):
    # Конвертируем в HSV
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # Обрезаем изображение на 150 px сверху
    crop_img = hsv_image[150:600, 0:800]

    # Создаём маску, используя показатели toolbars и Выводим изображение маски
    img_mask_lines = cv2.inRange(crop_img, color_lines[0], color_lines[1])
    img_mask_car = cv2.inRange(crop_img, color_car[0], color_car[1])
    cv2.imshow('crop_mask' + name, (img_mask_lines + img_mask_car))


if __name__ == '__main__':
    while True:
        cap = sct.grab(bounding_box)
        img = np.array(cap)
        cv2.imshow('GTAV', img)
        process_img(img, 'GTA', color_lines)
        pressed_key = cv2.waitKey(1)
