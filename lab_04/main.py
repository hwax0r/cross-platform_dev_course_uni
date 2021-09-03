"""
Created on Thu 2 Sep 13:20

@author: Sergeev David Evgenievich
Group: IVT-41-18
"""

import re
import json
import string
import pprint
from pathlib import Path


class Request:
    def __init__(self):
        self.file_name: str = ''

        self.words: list = []  # массив искомых в абзаце слов

        self.ex_min_len: int = 0  # минимальное количестов слов в абзаце
        self.ex_max_len: int = 0  # максимальное количестов слов в абзаце

        self.ex_amount: int = 0  # количестов абзацев для удачного поиска

    def process_input(self, file_name: str):
        self.file_name = file_name
        file = open(self.file_name, mode='r')
        request_ = json.load(file)
        file.close()

        self.words = set(request_['words'])
        self.ex_min_len = request_['example minimum length']
        self.ex_max_len = request_['example maximum length']
        self.ex_amount = request_['number of examples']


class Response:
    def __init__(self, file_name: str, paragraph_number: int, paragraph_content: list):
        self.file_name: str = file_name
        self.paragraph_number: int = paragraph_number
        self.paragraph_content: list = paragraph_content

        self.json_object_keys: list = ['file name', 'paragraph number', 'paragraph content']
        self.json_object_values = [self.file_name, self.paragraph_number, list(self.paragraph_content)]

        self.response_json: dict = dict(zip(self.json_object_keys, list(self.json_object_values)))


class Book:
    def __init__(self):
        self.file_name: str = ''
        self.book_txt: str = ''
        self.book_paragraphs: list = []

    def process_input(self, file_name: str) -> None:
        self.file_name = file_name
        self.book_txt = Path(self.file_name).read_text()
        self.book_paragraphs = self.book_txt.split("\n\n")

    def process_paragraphs(self):
        """
        Функция преобразовывает абзацы к списку из слов
        для последующего поиска
        """
        allowed_symbols = string.ascii_letters

        for paragraph_idx in range(len(self.book_paragraphs)):
            paragraph: str = self.book_paragraphs[paragraph_idx]

            # преобразование текста
            paragraph = paragraph.replace('\n', ' ').lower()
            paragraph = re.sub('[^%s]' % allowed_symbols, ' ', paragraph)

            self.book_paragraphs[paragraph_idx] = set(paragraph.split())

    def get_data(self, request: Request):
        responses: list = []

        for paragraph_idx in range(len(self.book_paragraphs)):
            paragraph: list = self.book_paragraphs[paragraph_idx]

            if set(request.words).issubset(set(paragraph)):
                if request.ex_min_len < len(paragraph) < request.ex_max_len+1:
                    responses.append(Response(self.file_name, paragraph_idx, paragraph))
            if len(responses) == request.ex_amount:
                break

        if len(responses) == request.ex_amount:
            # вывод результата в файл
            with open('response.json', mode='w') as resp_json:
                resp_json.write('[\n')
                pp = pprint.PrettyPrinter(indent=4, width=80, compact=True, stream=resp_json)

                for resp_idx in range(len(responses)):
                    str_ = json.dumps(responses[resp_idx].response_json, separators=(',', ': '))
                    pp.pprint(json.loads(str_))
                    if resp_idx != len(responses)-1:
                        resp_json.write(',')
                    resp_json.write('\n')
                resp_json.write(']')

            with open('response.json', mode='r+') as f:
                text = f.read()
                text = re.sub('\'', '\"', text)
                f.seek(0)
                f.write(text)
                f.truncate()
        else:
            print("No")


def main():
    request = Request()
    request.process_input('request.json')

    book = Book()
    book.process_input('Crime and Punishment.txt')
    book.process_paragraphs()

    book.get_data(request=request)


if __name__ == '__main__':
    main()
