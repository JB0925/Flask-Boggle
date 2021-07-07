from flask import Flask, redirect, render_template, session, url_for, request, jsonify
from decouple import config

from boggle import Boggle


app = Flask(__name__)
app.config['SECRET_KEY'] = config('SECRET_KEY')
boggle_game = Boggle()
board = boggle_game.make_board()


@app.route('/', methods=['GET', 'POST'])
def home():
    """The main route for the game. Displays the board
        and all major aspects of the game."""
    session['board'] = board
    games = session['games_played']
    if request.method == 'GET':
        return render_template('home.html', board=board, games=games)
    return redirect(url_for('home', board=board, games=games))
    


@app.route('/temp', methods=['GET','POST'])
def temp():
    """We send a GET request here from Axios to 
       validate the word that is coming from the 
       front end."""
    board = session['board']
    word = request.args.get('word')
    result = boggle_game.check_valid_word(board, word)
    result = jsonify(result)
    return result

@app.route('/games', methods=['GET', 'POST'])
def games_played():
    """Another GET request is sent here at the end
       of the game to update on the server the 
       number of games that have been played."""
    games = request.json['games']
    session['games_played'] += 1
    return jsonify(games)