from flask import Flask, redirect, render_template, session, url_for, request
from decouple import config

from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
boggle_game = Boggle()


@app.route('/', methods=['GET', 'POST'])
def home():
    board = boggle_game.make_board()
    classes = ['one', 'two', 'three', 'four', 'five']
    session['board'] = board
    if request.method == 'GET':
        return render_template('home.html', board=board,
        classes=classes)
