import keyboard
from time import sleep

for t in range(5, 0, -1):
    print(t)

keyboard.press('w')
sleep(10)
keyboard.release('w')
