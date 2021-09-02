"""
Created on Thu 2 Sep 23:16

@author: Sergeev David Evgenievich
Group: IVT-41-18
"""


from flask import Flask, render_template, Response, \
    Request, redirect, url_for

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def index():
    return render_template('main.html')


def anime():
    print("anime")


if __name__ == '__main__':
    app.run()
