"""
Created on Wed 1 Sep 20:55

@author: Sergeev David Evgenievich
Group: IVT-41-18
"""

import os
import re

VOWEL = {'a': 0, 'e': 0, 'i': 0, 'o': 0, 'u': 0}
CONSONANT = {'t': 0, 'r': 0, 'd': 0, 'y': 0, 'f': 0, 'q': 0, 'w': 0, 'z': 0, 'h': 0,
             'g': 0, 'k': 0, 'j': 0, 'n': 0, 'c': 0, 'l': 0, 'm': 0, 'x': 0, 'b': 0,
             'p': 0, 's': 0, 'v': 0}


def solution(book_path: str) -> str:
    book = open(book_path, mode='r')
    word_max_vowels: str = ''
    for line in book:
        # удаление символов и преобразование к строчным буквам
        processed: list = re.sub(r'[^\w]', ' ', line).split()
        processed: list = [word.lower() for word in processed]

        for word in processed:
            # подсчёт кол-ва гласных в слове
            vowels: dict = {}
            for char in word:
                if char in VOWEL and len(vowels) <= 2:
                    if char not in vowels.keys():
                        vowels.update({char: 0})
                    vowels[char] += 1
            # сравнение в соответствии с условиями задачи
            if len(vowels) == 1:
                if len(word) > len(word_max_vowels):
                    word_max_vowels = word
            else:
                continue

    return word_max_vowels


def main():
    book_path: str = f'{os.getcwd()}{os.sep}the_possessed.txt'
    result: str = solution(book_path=book_path)
    if result == '':
        print('В тексте нет слов с одним гласным')
    else:
        print(f'Самое длинное слово с одним гласным: {result}')


if __name__ == '__main__':
    main()
