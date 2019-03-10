from blueprints import db
from flask_restful import fields


class Cart(db.Model):

    __tablename__ = 'cart'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    itemname = db.Column(db.String(100))
    harga = db.Column(db.Integer)
    user_id = db.Column(db.Integer)
    item_id = db.Column(db.Integer)
    tanggal_upload = db.Column(db.String(25))

    response_field = {
        # 'id': fields.Integer,
        'itemname': fields.String,
        'harga': fields.Integer,
        'user_id': fields.Integer,
        # 'item_id': fields.Integer,
        'tanggal_upload': fields.String,
    }

    def __init__(self, itemname, harga, user_id, item_id, tanggal_upload):
        self.itemname = itemname
        self.harga = harga
        self.user_id = user_id
        self.item_id = item_id
        self.tanggal_upload = tanggal_upload

    def __repr__(self):
        return '<Cart %r>' % self.id
