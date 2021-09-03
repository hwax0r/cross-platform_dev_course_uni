from nltk import sent_tokenize
from typing import List, Dict
import json


#def read_request_json(filename: str = "request.json") -> dict:
#   with open(filename) as file:
#        f = json.load(file)
#        return f


def get_sentences_from_file(filename: str = "./Crime and Punishment.txt", lang: str = "english") -> List[str]:
    with open(filename, "r", encoding="utf-8") as book:
        text = book.read()
        sentences = sent_tokenize(text, lang)
        return sentences


def find_words(sentences: List[str], words: List[str], examples: int = 5) -> dict:
    ret = []
    for sentence in sentences:
        #if not (min_len <= len(sentence) <= max_len):
        #    continue
        if examples <= 0:
            break
        if set(words).issubset(set(sentence.split())):
            ret.append(sentence)
            examples -= 1
    return {'words': ret}


#def save_response(obj: dict) -> None:
#    with open("response.json", "w", encoding="utf-8") as file:
#        json.dump(obj, file, ensure_ascii=True, indent=4)

def find_words_by_request(req: dict) -> dict:
    sents = get_sentences_from_file()
    return find_words(sents, req['words'], req['examples'])

