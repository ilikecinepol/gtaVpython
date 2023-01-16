import time
import cv2
import keyboard
import mss
import numpy
import pyautogui as pag
from random import choice


def screen_record_efficiency():
    #game_window
    mon = {'top':30, 'left': 0, 'width':1902, 'height':1033}
    title  = '[MSS] FPS benchmark'
    fps = 0
    sct = mss.mss()
    last_time = time.time()
    color = {
        'orange': ((10, 110, 0,), (30, 167, 241)),
        'green': ((55, 112, 92,), (76, 255, 163)),
        'red': ((0, 243, 170,), (0, 255, 255)),
    }
    x = [300, 400, 500]
    while True:
        img = numpy.asarray(sct.grab(mon))
        fps += 1
        hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img_mask = cv2.inRange(hsv_image, color['green'][0], color['green'][1])
        red_contours, _ = cv2.findContours(img_mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        if red_contours:
            for cnt in red_contours:
                # print(cv2.contourArea(cnt))

                if cv2.contourArea(cnt) > 890:
                    # print(cv2.contourArea(cnt))
                    last_green_area = cv2.contourArea(cnt)
                    time.sleep(0.01)
                    current_green_area = cv2.contourArea(cnt)
                    if current_green_area < last_green_area:
                       print('rkb')
                        # keyboard.send('space')




                    # pag.click(current_x, current_y, 2, 0.01, 'left')
        else:
            print('не кликай')
            pass
        cv2.imshow('fd', img_mask)
        if cv2.waitKey(25) and 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

    return fps
number_of_warms = 24
if __name__ == '__main__':
    while True:
        screen_record_efficiency()
