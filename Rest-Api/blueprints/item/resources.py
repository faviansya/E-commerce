import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from . import *

bp_item = Blueprint('item', __name__)
api = Api(bp_item)

class ItemResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, item_id = None):
        jwtclaim = get_jwt_claims()
        if item_id == None or item_id == 'all':
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 10)
            parser.add_argument('item_id', type = int, location = 'args')
            parser.add_argument('nama', location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Item.query

            if args['nama'] is not None:
                qry = qry.filter(Item.name.like("%"+args['nama']+"%")).all()
                data = []
                for row in qry:
                    data.append(marshal(qry, Item.response_field))
                return data, 200, {'Content_type' : 'application/json'} 

            if args['item_id'] is not None:
                qry = qry.get(args['item_id'])
                return marshal(qry, Item.response_field), 200, {'Content_type' : 'application/json'} 

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Item.response_field))

            return rows, 200, {'Content_type' : 'application/json'}

        elif (item_id == 'myitems'):
            if(jwtclaim['level'] is not 'admin'):
                qry = Item.query.filter(Item.post_by.like(jwtclaim['id'])).all()
                return marshal(qry, Item.response_field), 200, {'Content_type' : 'application/json'}
            return {'status' :"you Are Admin, You Dont Have Privileage to SELL something"}, 402, {'Content_type' : 'application/json'}

        else:
            qry = Item.query.get(item_id)
            if qry is not None:
                return marshal(qry, Item.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'Incorrect ID'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def delete(self):
        jwtclaim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('accept', type = bool, location = 'args', default = False)
        parser.add_argument('nama', location = 'json',required = True)
        parser.add_argument('small_deskripsi', location = 'json',required = True)
        args = parser.parse_args()

        qry = Item.query.filter(Item.name.like("%"+args['nama']+"%")).filter(Item.deskripsi.like("%"+args['small_deskripsi']+"%")).first()
        
        if(jwtclaim['level'] == 'user'):
            if args['accept'] == True and jwtclaim['id'] == marshal(qry, Item.response_field)['post_by']:
                db.session.delete(qry)
                db.session.commit()
                return {'status' : 'Success', 'message' : 'Your Own Data has Been Deleted'}, 200, {'Content_type' : 'application/json'}
        
        elif(jwtclaim['level'] == 'admin'):
            if args['accept'] == True:
                db.session.delete(qry)
                db.session.commit()

                return {'status' : 'Success', 'message' : 'Admin Delete Choosen Data'}, 200, {'Content_type' : 'application/json'}
        return {'status' : 'Failed', 'message' : 'Not Your Items, You Only Can Choose Your Item'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self):
        jwtclaim = get_jwt_claims()
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=int, location = 'args', required = True)
        args = parser.parse_args()
        qry_item = Item.query.get(args['id'])

        if jwtclaim['level'] == 'user':
            if jwtclaim['id'] != marshal(qry_item, Item.response_field)['post_by']:
                return {'status' : 'Failed', 'Your ID' : 'Not Your Item'}, 200, {'Content_type' : 'application/json'}

        item_marshal = marshal(qry_item, Item.response_field)
        parser = reqparse.RequestParser()
        parser.add_argument('id',type=int, location = 'args', required = True)
        parser.add_argument('nama', location = 'json', default = item_marshal['name'])
        parser.add_argument('harga', location = 'json', default = item_marshal['harga'])
        parser.add_argument('kategori', location = 'json',default = item_marshal['kategori'])
        parser.add_argument('kondisi', location = 'json',default = item_marshal['kondisi'])
        parser.add_argument('deskripsi', location = 'json',default = item_marshal['deskripsi'])
        parser.add_argument('berat', location = 'json',default = item_marshal['berat'])
        args = parser.parse_args()
        
        qry_item.name = args['nama']
        qry_item.harga = args['harga']
        qry_item.kategori = args['kategori']
        qry_item.kondisi = args['kondisi']
        qry_item.deskripsi = args['deskripsi']
        qry_item.berat = args['berat']
        
        db.session.commit()
        return {'status' : marshal(qry_item, Item.response_field)['post_by'], 'Your Item' : marshal(qry_item, Item.response_field)}, 200, {'Content_type' : 'application/json'}
    
    @jwt_required
    def post(self):
        jwtclaim = get_jwt_claims()
        if jwtclaim['level'] == 'user':
            parser = reqparse.RequestParser()
            parser.add_argument('nama', location = 'json', required = True)
            parser.add_argument('harga', location = 'json', required = True)
            parser.add_argument('kategori', location = 'json', required = True)
            parser.add_argument('kondisi', location = 'json', default = 'baru',required = True)
            parser.add_argument('deskripsi', location = 'json', required = True )
            parser.add_argument('status_publish', location = 'json', default = 'unpublish')
            parser.add_argument('berat', location = 'json', default = 100)
            args = parser.parse_args()

            item = Item(args['nama'], args['harga'],args['kategori'],args['kondisi'],
                        args['deskripsi'],args['status_publish'],args['berat'], jwtclaim['id'], '24-02-2019')
            db.session.add(item)
            db.session.commit()

            return {'status' : 'Success', 'Your Account' : marshal(item, Item.response_field)}, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'Failed', 'message' : 'You Are Admin Not Allowed To Sell'}, 401, {'Content_type' : 'application/json'}


api.add_resource(ItemResource, '', '/<item_id>')