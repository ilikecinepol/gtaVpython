import numpy as np
import cv2
from mss import mss
import keyboard
import time
import vgamepad as vg

gamepad = vg.VX360Gamepad()
bounding_box = {'top': 30, 'left': 0, 'width': 800, 'height': 600}
sct = mss()
colors = {
    'orange': ((10, 110, 0,), (30, 167, 241)),
    'green': ((36, 95, 0,), (65, 182, 255)),
}


# Функция обработки изображения
def process_img(img, name, color):
    x_list = []
    res = 400
    # Конвертируем в HSV
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Создаём маску, используя показатели toolbars и Выводим изображение маски
    img_mask_lines = cv2.inRange(hsv_image, color['orange'][0], color['orange'][1])
    img_mask_car = cv2.inRange(hsv_image, color['green'][0], color['green'][1])

    # Создаём прямоугольную область маски, залитую чёрным цветом
    x, y, w, h = 0, 0, 800, 150
    img_mask_lines = cv2.rectangle(img_mask_lines, (x, y), (x + w, y + h), 0, -1)
    img_mask_car = cv2.rectangle(img_mask_car, (x, y), (x + w, y + h), 0, -1)

    x, y, w, h = 0, 0, 200, 600
    img_mask_lines = cv2.rectangle(img_mask_lines, (x, y), (x + w, y + h), 0, -1)
    img_mask_car = cv2.rectangle(img_mask_car, (x, y), (x + w, y + h), 0, -1)

    x, y, w, h = 600, 0, 800, 600
    img_mask_lines = cv2.rectangle(img_mask_lines, (x, y), (x + w, y + h), 0, -1)
    img_mask_car = cv2.rectangle(img_mask_car, (x, y), (x + w, y + h), 0, -1)
    add_masks = img_mask_lines + img_mask_car

    # Ищем контуры нужного цвета
    orange_contours, _ = cv2.findContours(img_mask_lines, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, _ = cv2.findContours(img_mask_car, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Рисуем контуры нужного цвета
    drawing = img.copy()
    # if cv2.contourArea(orange_contours) < 100:

    if green_contours:
        cv2.drawContours(drawing, green_contours, -1, (255, 0, 00), 1)
    if orange_contours:
        # cv2.putText(drawing, 'CONTOURS WAS DETECTED', (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)

        for cnt in orange_contours:
            if cv2.contourArea(cnt) < 300:
                continue
            cv2.drawContours(drawing, [cnt], -1, (0, 0, 255), thickness=cv2.FILLED)
            moments = cv2.moments(cnt)
            try:
                x = int(moments['m10'] / moments['m00'])
                x_list.append(x)
                y = int(moments['m01'] / moments['m00'])
                cv2.circle(drawing, (x, y), 4, (0, 255, 255), -1)
                # cv2.putText(drawing, 'CONTOURS WAS DETECTED', (100, 300), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 4)
            except ZeroDivisionError:
                pass

    # cv2.line(drawing, (400, 0), (400, 600), (0, 0, 255), 2)
    # cv2.imshow('mask', add_masks)
    try:
        res = (sum(x_list)/len(x_list))

    except ZeroDivisionError:
        pass
    print(f'res: {res}')
    return drawing, res


# Рассчитываем значения линейной и угловой скоростей
def get_vel(line_coords, kp, kl):
    angular_vel = (400 - line_coords) * kp
    linear_vel = 50
    ang = 'налево' if angular_vel < 0 else 'направо'
    print(f'Линейная: {linear_vel}, Угловая: {angular_vel}, {ang}')
    return linear_vel, angular_vel



# Движение автомобиля
def car_moving(vel):
    linear_vel, angular_vel = vel[0], vel[1]
    if linear_vel >= 0:
        gamepad.right_trigger(value=int(linear_vel))
    else:
        gamepad.left_trigger(value=int(linear_vel))
    # Левый стик х - влево(минус)/вправо(плюс)
    gamepad.left_joystick_float(x_value_float=angular_vel, y_value_float=-1.0)  # values between -1.0 and 1.0
    gamepad.update()
    time.sleep(0.01)


if __name__ == '__main__':
    # keyboard.wait('i')
    while True:
        kp = - 10
        kl = 0.2
        cap = sct.grab(bounding_box)
        img = np.array(cap)
        cv2.imshow('GTAV', process_img(img, 'GTA', colors)[0])
        vel = get_vel(process_img(img, 'GTA', colors)[1], kp=kp, kl=kl)
        car_moving(vel)

        if cv2.waitKey(33) == ord('a'):
            break
