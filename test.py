import json

from unittest import TestCase
from app import app
from flask import session

from boggle import Boggle


class FlaskTests(TestCase):

    def test_main_game_route(self):
        """Test to ensure the main game content is loading."""
        with app.test_client() as client:
            resp = client.get('/')
            self.assertEqual(len(session['board']), 5)
            self.assertEqual(resp.status_code, 200)
            post_resp = client.post('/')
            self.assertEqual(post_resp.status_code, 302)
            self.assertIn('<h1 class="header">Boggle</h1>', resp.get_data(as_text=True))
    

    def test_check_word_route(self):
        """Tests to ensure that correct responses are given depending on the 
           word submitted."""
        responses = ['not-word', 'not-on-board', 'ok', 'not-word', 'not-word']
        words = ['zyx', 'build', 'war', '-15', '']

        with app.test_client() as client:
            with client.session_transaction() as sesh:
                sesh['board'] = [
                    ['X', 'W', 'T', 'U', 'B'],
                    ['Q', 'A', 'R', 'N', 'L'],
                    ['E', 'E', 'S', 'N', 'V'],
                    ['I', 'K', 'W', 'H', 'O'],
                    ['T', 'D', 'B', 'O', 'R']
                ]
            
            for i in range(len(words)):
                resp = client.get('/temp', query_string={'word': words[i]})
                self.assertEqual(resp.json, responses[i])
                self.assertEqual(resp.status_code, 200)
    

    def test_games_played_route(self):
        """Testing to ensure that the session['games_played']
           is being updated after each game."""
        with app.test_client() as client:
            with client.session_transaction() as sesh:
                sesh['games_played'] = 2
            
            data = {"games": 1}
            resp = client.get('/games', data=json.dumps(data), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, 3)

            with client.session_transaction() as sesh:
                sesh['games_played'] = 11
            
            data = {"games": 1}
            resp = client.get('/games', data=json.dumps(data), content_type='application/json')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.json, 12)


