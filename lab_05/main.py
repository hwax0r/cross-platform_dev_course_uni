"""
Created on Thu 2 Sep 20:28

@author: Sergeev David Evgenievich
Group: IVT-41-18
"""

import re
import json
import nltk
from pathlib import Path


class Request:
    def __init__(self):
        self.file_name: str = ''

        self.words: list = []  # массив искомых в абзаце слов

        self.ex_min_len: int = 0  # минимальное количестов слов в предложении
        self.ex_max_len: int = 0  # максимальное количестов слов в предложении

        self.ex_amount: int = 0  # количестов предложений для удачного поиска

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
    def __init__(self, file_name: str, sentence_number: int, sentence_content: str):
        self.file_name: str = file_name
        self.sentence_number: int = sentence_number
        self.sentence_content: str = sentence_content.replace("\n", " ").encode('ascii', 'ignore').decode()

        self.json_object_keys: list = ['file name', 'sentence number', 'sentence content']
        self.json_object_values = [self.file_name, self.sentence_number, self.sentence_content]

        self.response_json: dict = dict(zip(self.json_object_keys, self.json_object_values))


class Book:
    def __init__(self):
        self.file_name: str = ''
        self.book_txt: str = ''
        self.book_sentences: list = []

    def process_input(self, file_name: str) -> None:
        self.file_name = file_name
        self.book_txt = Path(self.file_name).read_text()
        self.book_sentences = nltk.tokenize.sent_tokenize(self.book_txt)

    def get_data(self, request: Request):
        responses: list = []

        for sentence_idx in range(len(self.book_sentences)):
            sentence: str = self.book_sentences[sentence_idx]

            if set(request.words).issubset(set(sentence.split())):
                if request.ex_min_len < len(sentence) < request.ex_max_len+1:
                    responses.append(Response(self.file_name, sentence_idx, sentence))
            if len(responses) == request.ex_amount:
                break

        if len(responses) == request.ex_amount:
            # вывод результата в файл
            with open('response.json', mode='w') as resp_json:
                resp_json.write('[\n')

                for resp_idx in range(len(responses)):
                    json.dump(responses[resp_idx].response_json, separators=(',', ': '), indent=3, fp=resp_json)
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

    book.get_data(request=request)


if __name__ == '__main__':
    main()
