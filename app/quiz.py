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
    q1_1 = BooleanField('q1_1')
    q1_2 = BooleanField('q1_2')
    q1_3 = BooleanField('q1_3')

    q2_1 = BooleanField('q2_1')
    q2_2 = BooleanField('q2_2')
    q2_3 = BooleanField('q2_3')

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
        # Weil APIs cool sind. Wird safe irgendwer in naher Zukunft brauchen.
    else:
        return render_template('quiz/leaderboard.html', route="leaderboard", board=board, profile=Profile.getProfile())


@blueprint.route('/quiz/', methods=['GET', 'POST'])
@blueprint.route('/quiz/quiz', methods=['GET', 'POST'])
def quiz():
    if not session.get('logged_in'):
        return redirect(url_for('account.login'))

    if request.method != 'POST':
        return render_template('quiz/quiz.html', route="quiz", form=Quiz(), profile=Profile.getProfile())

    score = calculateScore(request.form)
    res = Profile.updateScore(score)

    if res == 1:
        return redirect(url_for('account.login'))
    if res == 2:
        return redirect(url_for('account.register'))

    return redirect(url_for('quiz.leaderboard'))


def calculateScore(form: dict):
    results: dict[str, [int]] = {}
    for (questionId, _) in dict(form).items():
        if not questionId.startswith("q"):
            continue

        idParts = questionId.split("_")
        name = idParts[0]
        answer = idParts[1]

        if not results.get(name):
            results[name] = []

        results[name].append(answer)

    score = 0
    right_answers = {'q1': ['1'], 'q2': ['2']}
    for (name, answers) in right_answers.items():
        if name in results:
            score += set(answers) == set(results[name]) if len(answers) else 0

    return score
