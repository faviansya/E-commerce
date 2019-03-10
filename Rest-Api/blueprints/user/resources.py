import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims

from . import *

bp_user = Blueprint('user', __name__)
api = Api(bp_user)

class UserResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, user_id = None):
        jwtclaim = get_jwt_claims()
        if user_id == None or user_id == 'all':
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 10)
            parser.add_argument('user_id', type = int, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = User.query

            if args['user_id'] is not None:
                qry = qry.get(args['user_id'])
                return marshal(qry, User.response_field), 200, {'Content_type' : 'application/json'} 

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, User.response_field))

            return rows, 200, {'Content_type' : 'application/json'}
        elif (user_id == 'me'):
            qry = User.query.get(jwtclaim['id'])
            return marshal(qry, User.response_field), 200, {'Content_type' : 'application/json'}            
        else:
            qry = User.query.get(user_id)

            if qry is not None:
                return marshal(qry, User.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'Incorrect ID'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('accept', type = bool, location = 'args', default = False)
        args = parser.parse_args()
        jwtclaim = get_jwt_claims()
        if(jwtclaim['level'] == 'admin'):
            return {"status":"you Are Admin,Do Delete From Admin Page"}, 402, {'Content_type' : 'application/json'}

        if args['accept'] == True:
            qry = User.query.get(jwtclaim['id'])
            
            db.session.delete(qry)
            db.session.commit()

            return {'status' : 'Success', 'message' : 'See You Again In Another Time'}, 200, {'Content_type' : 'application/json'}
        return {'status' : 'Failed', 'message' : 'Please Accept For Delete Your ID'}, 404, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self):
        jwtclaim = get_jwt_claims()
        if(jwtclaim['level'] == 'admin'):
            return {"status":"you Are Admin, You Dont Have Privileage to Change User Information"}, 401, {'Content_type' : 'application/json'}

        qry = User.query.get(jwtclaim['id'])
        parser = reqparse.RequestParser()
        parser.add_argument('password', location = 'json', required = True)
        parser.add_argument('passwordconfirm', location = 'json', required = True)
        parser.add_argument('nama', location = 'json')
        parser.add_argument('alamat', location = 'json')
        args = parser.parse_args()
        if args['nama'] is not None:
            qry.nama = args['nama']
        if args['alamat'] is not None:
            qry.alamat = args['alamat']

        if(args['password'] != args['passwordconfirm']):
            return {'status' : 'Failed', 'message' : 'Please MakeSure Your PasswordConfirm same With Password'}, 401, {'Content_type' : 'application/json'}
        
        qry.password = args['password']
        db.session.commit()
        return {'status' : 'Success Change Password', 'Your ID' : marshal(qry, User.response_field)}, 200, {'Content_type' : 'application/json'}

    def post(sef, user_id = None):
        if user_id == None:
            return {'status' : 'Failed', 'message' : 'Access /user/api/user/register'}, 404, {'Content_type' : 'application/json'}
        elif user_id == 'register':
            parser = reqparse.RequestParser()
            parser.add_argument('username', location = 'json', required = True)
            parser.add_argument('password', location = 'json', required = True)
            parser.add_argument('nama', location = 'json', required = True)
            parser.add_argument('alamat', location = 'json', default = 'You Can Change It later')
            args = parser.parse_args()

            user = User(args['username'], args['password'],args['nama'],args['alamat'], 'normal', 'user')
            db.session.add(user)
            db.session.commit()

            return {'status' : 'Success', 'Your Account' : marshal(user, User.response_field)}, 200, {'Content_type' : 'application/json'}
        else:
            return {'status' : 'Failed', 'message' : 'Wrong Register Page'}, 404, {'Content_type' : 'application/json'}


api.add_resource(UserResource, '', '/<user_id>')