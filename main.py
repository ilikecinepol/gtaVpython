import numpy as np
import cv2
from mss import mss
import keyboard
import time
import vgamepad as vg
from pynput.mouse import Button, Controller
import pyautogui as pag

gamepad = vg.VX360Gamepad()
bounding_box = {'top': 540, 'left': 470, 'width': 50, 'height': 50}
# bounding_box = {'top': 30, 'left': 0, 'width': 800, 'height': 600}
sct = mss()

mouse = Controller()


# Функция обработки изображения
def process_img():
    color = {
        'orange': ((10, 110, 0,), (30, 167, 241)),
        'green': ((36, 95, 0,), (65, 182, 255)),
        'red': ((0, 243, 170,), (0, 255, 255)),
    }

    res = 400
    cap = sct.grab(bounding_box)
    #cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc(*"MJPG"))
    img = np.array(cap)
    # Конвертируем в HSV
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Создаём маску, используя показатели toolbars и Выводим изображение маски
    img_mask = cv2.inRange(hsv_image, color['red'][0], color['red'][1])

    # Ищем контуры нужного цвета
    red_contours, _ = cv2.findContours(img_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Рисуем контуры нужного цвета
    drawing = img.copy()
    # if cv2.contourArea(orange_contours) < 100:

    if red_contours:
        # cv2.putText(drawing, 'CONTOURS WAS DETECTED', (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
        pag.click(100, 100, 10, 0.2, 'left')
        '''mouse.press(Button.left)
        print('mouse')
        time.sleep(0.5)
        mouse.release(Button.left)
        print('mouse 1')
        time.sleep(0.5)
        print('mouse')'''
        for cnt in red_contours:

            cv2.drawContours(drawing, [cnt], -1, (0, 0, 255), thickness=cv2.FILLED)
            moments = cv2.moments(cnt)
            try:
                x = int(moments['m10'] / moments['m00'])
                y = int(moments['m01'] / moments['m00'])
                cv2.circle(drawing, (x, y), 4, (0, 255, 255), -1)
                # cv2.putText(drawing, 'CONTOURS WAS DETECTED', (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
            except ZeroDivisionError:
                pass
    cv2.imshow('fd', img)
    cv2.waitKey(33)


if __name__ == '__main__':
    # keyboard.wait('i')
    while True:
        keyboard.add_hotkey('1', process_img)
