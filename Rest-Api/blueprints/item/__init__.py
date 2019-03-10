from blueprints import db
from flask_restful import fields


class Item(db.Model):

    __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    harga = db.Column(db.Integer)
    kategori = db.Column(db.String(100))
    kondisi = db.Column(db.String(100))
    deskripsi = db.Column(db.String(100))
    status_publish = db.Column(db.String(25))
    berat = db.Column(db.Integer)
    post_by = db.Column(db.Integer)
    tanggal_upload = db.Column(db.String(25))

    response_field = {
        'id': fields.Integer,
        'name': fields.String,
        'harga': fields.Integer,
        'kategori': fields.String,
        'kondisi': fields.String,
        'deskripsi': fields.String,
        'status_publish': fields.String,
        'berat': fields.Integer,
        'post_by': fields.Integer,
        'tanggal_upload': fields.String,
    }

    def __init__(self, name, harga, kategori, kondisi, deskripsi, status_publish, berat, post_by, tanggal_upload):
        self.name = name
        self.harga = harga
        self.kategori = kategori
        self.kondisi = kondisi
        self.deskripsi = deskripsi
        self.status_publish = status_publish
        self.berat = berat
        self.post_by = post_by
        self.tanggal_upload = tanggal_upload

    def __repr__(self):
        return '<Item %r>' % self.id
