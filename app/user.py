from flask import session

from .database import db, Users


class Profile:
    id: int
    name: str
    email: str
    icon: int
    score: int

    def __init__(self, id, name, email, icon, score):
        self.id = id
        self.name = name
        self.email = email
        self.icon = icon
        self.score = score

    def __repr__(self):
        return self.name

    @staticmethod
    def getProfile() -> None | object:
        if not session.get('logged_in'):
            return None
        profile = session.get('profile')
        return Profile(profile['id'], profile['name'], profile['email'], profile['icon'], profile['score'])

    @staticmethod
    def getUser() -> Users | None:
        if not session.get('logged_in'):
            return None
        pid = session.get('profile')['id']
        return Users.query.filter_by(id=pid).first()

    @staticmethod
    def checkPassword(password: str) -> bool:
        user = Profile.getUser()
        if not user:
            return False
        return user.check_password(password)

    # 0 => Logged in
    # 1 => Not exist
    # 2 => Wrong pw
    @staticmethod
    def login(name: str, password: str) -> int:
        if session.get('logged_in'):
            return 0

        user = Users.query.filter_by(name=name).first()
        if not user:
            return 1

        if not user.check_password(password):
            return 2

        session['logged_in'] = True
        session['profile'] = {'id': user.id, 'name': user.name, 'email': user.email, 'icon': user.icon, 'score': user.score}

    @staticmethod
    def logout() -> None:
        session['logged_in'] = False
        session.pop('logged_in', None)
        session.pop('profile', None)

    # 0 => Registered and Logged in
    # 1 => already Logged in
    # 2 => already exist
    @staticmethod
    def register(name: str, email: str, password: str) -> int:
        if session.get('logged_in'):
            return 1

        if (Users.query.filter_by(name=name).first()
                or Users.query.filter_by(email=email).first()):
            return 2

        user = Users(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()

        session['logged_in'] = True
        session['profile'] = {'id': user.id, 'name': user.name, 'email': user.email, 'icon': user.icon, 'score': user.score}
        return 0

    # 0 => Deleted User
    # 1 => User not logged in
    @staticmethod
    def delete() -> int:
        if not session.get('logged_in'):
            return 1

        Users.query.filter_by(id=session.get('profile')['id']).delete()
        db.session.commit()

        session['logged_in'] = False #Just in Case
        Profile.logout()
        return 0

    # 0 => Yes
    # 1 => Not Logged in
    # 2 => User not exist
    @staticmethod
    def IsLoggedInAndExists() -> (int, Users | None):
        if not session.get('logged_in'):
            return 1, None

        user = Profile.getUser()
        if not user:
            Profile.logout()
            return 2, None

        return 0, user

    # 0 => Score Set
    # 1 => Not Logged in
    # 2 => User not exist
    @staticmethod
    def updateScore(score: int) -> int:
        res, user = Profile.IsLoggedInAndExists()
        if res != 0:
            return res

        user.score = score
        db.session.commit()

        profile = session['profile']
        profile['score'] = score
        session['profile'] = profile

        return 0

    # 0 => Icon set
    # 1 => Not Logged in
    # 2 => User not exist
    @staticmethod
    def updateIcon(icon: int) -> int:
        res, user = Profile.IsLoggedInAndExists()
        if res != 0:
            return res

        user.icon = icon
        db.session.commit()

        profile = session['profile']
        profile['icon'] = icon
        session['profile'] = profile

        return 0

    # 0 => Data Set
    # 1 => Not Logged in
    # 2 => User not exist
    # 3 => Already used by other user
    @staticmethod
    def updateData(name: str, email: str) -> int:
        res, user = Profile.IsLoggedInAndExists()
        if res != 0:
            return res

        pid = session.get('profile')['id']
        nameUser = Users.query.filter_by(name=name).first()
        emailUser = Users.query.filter_by(email=email).first()
        if (nameUser and nameUser.id != pid) or (emailUser and emailUser.id != pid):
            return 3

        user.name = name
        user.email = email
        db.session.commit()

        profile = session['profile']
        profile['name'] = name
        profile['email'] = email
        session['profile'] = profile

        return 0
