from .application import db

class Distribution(db.Model):
    __tablename__ = 'distributions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    home_page = db.Column(db.String(50))
    author = db.Column(db.String(50))
    summary = db.Column(db.String(50))

    
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    openid = db.Column(db.String(200), unique=True)
    username = db.Column(db.String(16), unique=True)
    email = db.Column(db.String(120))
    fullname = db.Column(db.String(50))

    def __init__(self, username, email, openid, fullname=''):
        self.username = username
        self.email = email
        self.openid = openid
        self.fullname = fullname

    def __repr__(self):
        return '<User %r>' % (self.username)


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    distribution_id = db.Column("distribution_id", db.Integer, db.ForeignKey('distributions.id'))
    user_id = db.Column("user_id", db.Integer, db.ForeignKey('users.id'))
    comment = db.Column(db.String(5000))
    status = db.Column(db.Boolean()) #True=Working,False=FAILING
