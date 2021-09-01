"""
Created on Wed 1 Sep 10:12

@author: Sergeev David Evgenievich
Group: IVT-41-18
"""


import random


def main():
    left_corner: int = 0
    right_corner: int = 100
    guessing_number: int = random.randint(left_corner, right_corner + 1)
    print(f'Загаданное число находится в рамках от {left_corner} до {right_corner}\n')

    while True:
        user_input: int = int(input("Введите число: "))

        if user_input == guessing_number:
            print(f'Угадали! Действительно было загадано число {guessing_number}.')
            break

        if user_input > guessing_number:
            print(f'Загаданное число меньше, чем {user_input}.')
        else:
            print(f'Загаданное число больше, чем {user_input}.')


if __name__ == '__main__':
    main()
