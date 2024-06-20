from flask import Blueprint, redirect, url_for, render_template, jsonify, request, session
from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField

from .database import Users
from .user import Profile

blueprint = Blueprint('quiz', __name__)


class Entry:
    username: str
    score: int

    def __init__(self, username, score):
        self.username = username
        self.score = score

    def __repr__(self):
        return f'<Entry {self.username}: {self.score}>'


class Quiz(FlaskForm):
    # Leider ist es nicht möglich das dynamischer zu schreiben

    # Question 1, Ans: 1
    q1_1 = BooleanField('q1_1', default=False)
    q1_2 = BooleanField('q1_2', default=False)
    q1_3 = BooleanField('q1_3', default=False)

    # Question 2, Ans: 3
    q2_1 = BooleanField('q2_1', default=False)
    q2_2 = BooleanField('q2_2', default=False)
    q2_3 = BooleanField('q2_3', default=False)

    # Question 3, Ans: 2
    q3_1 = BooleanField('q3_1', default=False)
    q3_2 = BooleanField('q3_2', default=False)
    q3_3 = BooleanField('q3_3', default=False)

    # Question 4, Ans: 2
    q4_1 = BooleanField('q4_1', default=False)
    q4_2 = BooleanField('q4_2', default=False)
    q4_3 = BooleanField('q4_3', default=False)

    # Question 5, Ans: 1, 2, 3
    q5_1 = BooleanField('q5_1', default=False)
    q5_2 = BooleanField('q5_2', default=False)
    q5_3 = BooleanField('q5_3', default=False)

    submit = SubmitField('Absenden')


@blueprint.route('/quiz/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    users = Users.query.all()
    board = [Entry(user.name, user.score) for user in users]
    board = sorted(board, key=lambda entry: entry.score, reverse=True)

    if request.method == 'POST':
        json_board = [{'name': entry.username, 'score': entry.score} for entry in board]
        return jsonify({
            'board': json_board,
            'entry_count': len(board),
            'max_score': board[0].score,
            'min_score': board[-1].score
        })
        # Weil APIs cool sind. Wird safe irgendwer in naher Zukunft brauchen...
    else:
        return render_template('quiz/leaderboard.html', route="leaderboard", board=board, profile=Profile.getProfile())


@blueprint.route('/quiz/', methods=['GET', 'POST'])
@blueprint.route('/quiz/quiz', methods=['GET', 'POST'])
def quiz():
    if not session.get('logged_in'):
        return redirect(url_for('account.login'))

    if request.method != 'POST':
        return render_template('quiz/quiz.html', route="quiz", form=Quiz(), profile=Profile.getProfile())

    score = calculateScore(Quiz(request.form))
    res = Profile.updateScore(score)

    if res == 1:
        return redirect(url_for('account.login'))
    if res == 2:
        return redirect(url_for('account.register'))

    return redirect(url_for('quiz.leaderboard'))


def calculateScore(form: Quiz):
    score: int = 0

    if form.q1_1.data and not form.q1_2.data and not form.q1_3.data:
        score += 1
    if not form.q2_1.data and not form.q2_2.data and form.q2_3.data:
        score += 1
    if not form.q3_1.data and form.q3_2.data and not form.q3_3.data:
        score += 1
    if not form.q4_1.data and form.q4_2.data and not form.q4_3.data:
        score += 1
    if form.q5_1.data:
        score += 1
    if form.q5_2.data:
        score += 1
    if form.q5_3.data:
        score += 1

    return score
