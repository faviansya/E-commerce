from blueprints import db
from flask_restful import fields


class User(db.Model):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    name = db.Column(db.String(25))
    alamat = db.Column(db.String(100))
    status = db.Column(db.String(25))
    level = db.Column(db.String(25))

    response_field = {
        'id': fields.Integer,
        'username': fields.String,
        'name': fields.String,
        'alamat': fields.String,
        'status': fields.String,
        'level' : fields.String
    }

    def __init__(self, username, password, name, alamat, status, level):
        self.username = username
        self.password = password
        self.name = name
        self.alamat = alamat
        self.status = status
        self.level = level

    def __repr__(self):
        return '<User %r>' % self.id
