from flask import Flask, redirect, url_for, request
from flask import render_template
from flask import Response
from words_api import find_words_by_request
import os

app = Flask("My app", template_folder="./templates", static_folder='./static')


@app.route('/')
def index():
    return redirect(url_for('search'))


@app.route('/search')
def search():
    words = "in; a; Nastasya"
    if request.cookies.get("words"):
        words = request.cookies.get("words")
    examples = 5
    if request.cookies.get("examples"):
        examples = request.cookies.get("examples")
    return render_template('search.html', words=words, examples=examples)


@app.route('/result')
def result():
    words = request.args.get('words', type=str, default="in; a; Nastasya").replace(' ', '').split(';')
    examples = request.args.get('examples', type=int, default=5)
    sentences = find_words_by_request({"words": words, "examples": examples})
    resp = Response(render_template('result.html', sentences=sentences['words'], words=words), status=200)
    resp.set_cookie("words", ';'.join(words))
    resp.set_cookie("examples", str(examples))
    return resp


@app.route('/request', methods=['POST'])
def req():
    obj = request.get_json(force=True)
    sentences = find_words_by_request(obj)
    return sentences, 200

