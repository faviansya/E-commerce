import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from . import *
from blueprints.item import *

bp_cart = Blueprint('cart', __name__)
api = Api(bp_cart)

class CartResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self):
        jwtclaim = get_jwt_claims()
        if(jwtclaim['level'] == 'admin'):
            return {"status":"you Are Admin, You Dont Have Privileage to SELL something"}, 401, {'Content_type' : 'application/json'}
        parser = reqparse.RequestParser()
        parser.add_argument('p', type = int, location = 'args', default = 1)
        parser.add_argument('rp', type = int, location = 'args', default = 10)
        args = parser.parse_args()

        offside = (args['p'] * args['rp']) - args['rp']
        qry = Cart.query

        rows = []
        for row in qry.filter(Cart.user_id.like(jwtclaim['id'])).limit(args['rp']).offset(offside).all():
            rows.append(marshal(row, Cart.response_field))

        return rows, 200, {'Content_type' : 'application/json'}
    
    @jwt_required
    def delete(self):
        jwtclaim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('id', location = 'args', required = True)
        parser.add_argument('accept', type = int, location = 'args', default = 0)
        args = parser.parse_args()

        qry = Cart.query.get(args['id'])
        
        if(jwtclaim['level'] == 'user'):
            if args['accept'] == 1 and jwtclaim['id'] == marshal(qry, Cart.response_field)['user_id']:
                db.session.delete(qry)
                db.session.commit()
                return {'status' : 'Success', 'message' : 'Your Own Cart has Been Deleted'}, 200, {'Content_type' : 'application/json'}

        elif(jwtclaim['level'] == 'admin'):
            if args['accept'] == 1:
                db.session.delete(qry)
                db.session.commit()
                return {'status' : 'Success', 'message' : 'Admin Delete Choosen Data'}, 200, {'Content_type' : 'application/json'}
        return {'status' : 'Failed', 'message' : 'Not Your Cart Items, You Only Can Choose Your Cart Item'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        jwtclaim = get_jwt_claims()
        if jwtclaim['level'] == 'user':
            parser = reqparse.RequestParser()
            parser.add_argument('id', location = 'args', required = True)
            args = parser.parse_args()

            qry_item = Item.query.get(args['id'])
            if (qry_item == None):
                return {'status' : 'Failed', 'message' : 'Data ID Item GAG Ada'}, 404, {'Content_type' : 'application/json'}
            # qry_cart = Cart.query.get(args['id'])
            # if (qry_cart is not None):
            #     return {'status' : 'Failed', 'message' : 'Barang Sudah Ada di Cart Anda'}, 402, {'Content_type' : 'application/json'}

            item_now = marshal(qry_item, Item.response_field)

            cart = Cart(item_now['name'], item_now['harga'], jwtclaim['id'],item_now['id'], '24-02-2019')
            db.session.add(cart)
            db.session.commit()

            return {'status' : 'Success', 'Your Cart Item Added' : item_now['name'], 'Harga':item_now['harga'] }, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'Failed', 'message' : 'You Are Admin Not Allowed To Add Cart'}, 401, {'Content_type' : 'application/json'}


api.add_resource(CartResource, '')