import time
import cv2
import keyboard
import mss
import numpy
import pyautogui as pag
from random import choice


def screen_record_efficiency():
    #game_window
    mon = {'top':30, 'left': 0, 'width':1600, 'height':900}
    title  = '[MSS] FPS benchmark'
    fps = 0
    sct = mss.mss()
    last_time = time.time()
    color = {
        'orange': ((10, 110, 0,), (30, 167, 241)),
        'green': ((36, 95, 0,), (65, 182, 255)),
        'red': ((0, 243, 170,), (0, 255, 255)),
    }
    x = [1300, 1400, 1500]
    while True:
        img = numpy.asarray(sct.grab(mon))
        fps += 1
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_mask = cv2.inRange(hsv_image, color['red'][0], color['red'][1])
        red_contours, _ = cv2.findContours(img_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if red_contours:
            for cnt in red_contours:
                # print(cv2.contourArea(cnt))
                if cv2.contourArea(cnt) > 140:
                    # print('кликай!')11
                    current_x = choice(x)
                    current_y = 700

                    pag.click(current_x, current_y, 2, 0.01, 'left')
        else:
            # print('не кликай')
            pass
        # cv2.imshow('fd', img_mask)
        if cv2.waitKey(25) and 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    return fps
number_of_warms = 25
if __name__ == '__main__':
    print('start')
    for i in range(number_of_warms +1):
        print(f'Попытка номер {i+1}')
        keyboard.add_hotkey('1', screen_record_efficiency)
        print('Рыба поймана')
        time.sleep(37)
        keyboard.send('1')