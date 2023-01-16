# Игра "Угадай число"
import random

random_number = random.randint(1,100)
while True:
    num = int(input('Введите число от 1 до 100: '))
    if random_number == num:
        print(f'Вы победили! Было загадано число {num}')
        break
    elif random_number > num:
        print("Загаданное число больше")
    else:
        print("Загаданное число меньше")
