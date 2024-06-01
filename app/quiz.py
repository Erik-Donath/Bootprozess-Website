from flask import Blueprint, redirect, url_for, render_template, jsonify, request, session
from flask_sqlalchemy import SQLAlchemy

routes = Blueprint('quiz', __name__)
db = SQLAlchemy()


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    email = db.Column(db.String(50), unique=True)
    score = db.Column(db.Integer)

    def __init__(self, name, email, score=0):
        self.name = name
        self.email = email
        self.score = score

    def __repr__(self):
        return '<User %r>' % self.name


class LeaderboardEntry:
    name: str
    score: int

    def __init__(self, name, score):
        self.name = name
        self.score = score


@routes.route('/quiz/leaderboard', methods=['GET', 'POST'])
def leaderboard():
    users = Users.query.all()
    board = [LeaderboardEntry(user.name, user.score) for user in users]
    board = sorted(board, key=lambda entry: entry.score, reverse=True)

    if request.method == 'POST':
        json_board = [{'name': entry.name, 'score': entry.score} for entry in board]
        return jsonify({
                'board': json_board,
                'entry_count': len(board),
                'max_score': board[0].score,
                'min_score': board[-1].score
            }
        )
    else:
        return render_template('quiz/leaderboard.html', route="leaderboard", board=board)


@routes.route('/quiz/register', methods=['GET', 'POST'])
def register():
    # Dont register if already logged in
    if session.get('username'):
        return redirect(url_for('quiz.quiz'))

    if not request.method == 'POST':
        return render_template('quiz/register.html', route="quiz", failed=None)

    # Analyse form data and register if not exist
    username: str = request.form['username']
    email: str = request.form['email']

    if not username or not email:
        return render_template('quiz/register.html', route="quiz", failed="empty")

    if len(username) > 30 or len(email) > 50:
        return render_template('quiz/register.html', route="quiz", failed="too_long")

    if Users.query.filter_by(name=username).first() or Users.query.filter_by(email=email).first():
        return render_template('quiz/register.html', route="quiz", failed="exist")

    usr = Users(username, email)
    db.session.add(usr)
    db.session.commit()
    session["username"] = usr.name
    session["email"] = usr.email

    return redirect(url_for('quiz.quiz'))


@routes.route('/quiz/', methods=['GET', 'POST'])
@routes.route('/quiz/quiz', methods=['GET', 'POST'])
def quiz():
    if not session.get('username'):
        return redirect(url_for('quiz.register'))
    if request.method == 'POST':
        score = calculateScore(request.form)

        Users.query.filter_by(name=session['username']).update({'score': score})
        db.session.commit()

        return redirect(url_for('quiz.leaderboard'))
    else:
        return render_template('quiz/quiz.html', route="quiz")


def calculateScore(form: dict):
    results: dict[str, [int]] = {}
    for (questionId, _) in dict(form).items():
        idParts = questionId.split("-")
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
