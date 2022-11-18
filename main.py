import cv2
import numpy as np
import cv2
from mss import mss

bounding_box = {'top': 30, 'left': 0, 'width': 800, 'height': 600}

sct = mss()

colors = {
    'orange': ((22, 69, 224,), (27, 227, 255)),
    'green': ((36, 95, 0,), (65, 182, 255))
}


# Функция обработки изображения
def process_img(img, name, color):
    # Конвертируем в HSV
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Создаём маску, используя показатели toolbars и Выводим изображение маски
    img_mask_lines = cv2.inRange(hsv_image, color['orange'][0], color['orange'][1])
    img_mask_car = cv2.inRange(hsv_image, color['green'][0], color['green'][1])

    # Создаём прямоугольную область маски, залитую чёрным цветом
    x, y, w, h = 0, 0, 800, 150
    img_mask_lines = cv2.rectangle(img_mask_lines, (x, y), (x + w, y + h), 0, -1)
    img_mask_car = cv2.rectangle(img_mask_car, (x, y), (x + w, y + h), 0, -1)
    add_masks = img_mask_lines + img_mask_car

    # Ищем контуры нужного цвета
    orange_contours, _ = cv2.findContours(img_mask_lines, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(img_mask_car, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Рисуем контуры нужного цвета
    drawing = img.copy()
    # if cv2.contourArea(orange_contours) < 100:

    if orange_contours:
        # cv2.putText(drawing, 'CONTOURS WAS DETECTED', (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
        cv2.drawContours(drawing, orange_contours, -1, (0, 0, 255), thickness=cv2.FILLED)
    if green_contours:
        cv2.drawContours(drawing, green_contours, -1, (255, 0, 00), 1)

    cv2.imshow('contours', drawing)


if __name__ == '__main__':
    while True:
        cap = sct.grab(bounding_box)
        img = np.array(cap)
        cv2.imshow('GTAV', img)
        process_img(img, 'GTA', colors)
        pressed_key = cv2.waitKey(1)
