import json, logging
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import jwt_required, get_jwt_claims
from blueprints.user import *
from . import *

bp_admin = Blueprint('admin', __name__)
api = Api(bp_admin)

class AdminResource(Resource):

    def __init__(self):
        pass

    @jwt_required
    def get(self, admin_id = None):
        jwtclaim = get_jwt_claims()
        if jwtclaim['level'] == 'user':
            return {'status' : 'Failed', 'message' : 'YOU NOT ADMIN'}, 401, {'Content_type' : 'application/json'}
        if admin_id == None or admin_id == 'all':
            parser = reqparse.RequestParser()
            parser.add_argument('p', type = int, location = 'args', default = 1)
            parser.add_argument('rp', type = int, location = 'args', default = 10)
            parser.add_argument('admin_id', type = int, location = 'args')
            parser.add_argument('user_id', type = int, location = 'args')
            args = parser.parse_args()

            offside = (args['p'] * args['rp']) - args['rp']
            qry = Admin.query
            user_qry = User.query

            if args['admin_id'] is not None:
                qry = qry.get(args['admin_id'])
                return marshal(qry, Admin.response_field), 200, {'Content_type' : 'application/json'} 

            if args['user_id'] is not None:
                user_qry = user_qry.get(args['user_id'])
                return marshal(user_qry, User.response_field), 200, {'Content_type' : 'application/json'} 

            rows = []
            for row in qry.limit(args['rp']).offset(offside).all():
                rows.append(marshal(row, Admin.response_field))
            
            user_row = []
            for row in user_qry.limit(args['rp']).offset(offside).all():
                user_row.append(marshal(row, User.response_field))

            return {'status' : 'Success', 'Admin': rows, 'User' : user_row}, 200, {'Content_type' : 'application/json'}

        elif (admin_id == 'me'):
            qry = Admin.query.get(jwtclaim['id'])
            return marshal(qry, Admin.response_field), 200, {'Content_type' : 'application/json'}            
        else:
            qry = Admin.query.get(admin_id)
            if qry is not None:
                return marshal(qry, Admin.response_field), 200, {'Content_type' : 'application/json'}
            else:
                return {'status' : 'NOT_FOUND', 'message' : 'Incorrect ID'}, 404, {'Content_type' : 'application/json'}
    
    @jwt_required
    def delete(self):
        jwtclaim = get_jwt_claims()
        if jwtclaim['level'] == 'user':
            return {'status' : 'Failed', 'message' : 'YOU NOT ADMIN'}, 401, {'Content_type' : 'application/json'}

        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type = int, location = 'args')
        parser.add_argument('confirm', type = int, location = 'args', default = 0)
        args = parser.parse_args()

        if args['confirm'] == 1 and args['user_id'] is not None:
            qry = User.query.get(args['user_id'])
            
            db.session.delete(qry)
            db.session.commit()

            return {'status' : 'Success', 'message' : 'Admin Deleted Selected User'}, 200, {'Content_type' : 'application/json'}
        return {'status' : 'Failed', 'message' : 'Please do Delete Properly'}, 401, {'Content_type' : 'application/json'}

    @jwt_required
    def put(self):
        jwtclaim = get_jwt_claims()
        if jwtclaim['level'] == 'user':
            return {'status' : 'Failed', 'message' : 'YOU NOT ADMIN'}, 401, {'Content_type' : 'application/json'}

        qry = Admin.query.get(jwtclaim['id'])

        parser = reqparse.RequestParser()
        parser.add_argument('password', location = 'args', required = True)
        parser.add_argument('passwordconfirm', location = 'args', required = True)
        parser.add_argument('nama', location = 'args')
        parser.add_argument('alamat', location = 'args')
        args = parser.parse_args()
        if args['nama'] is not None:
            qry.nama = args['nama']
        if args['alamat'] is not None:
            qry.alamat = args['alamat']

        if(args['password'] != args['passwordconfirm']):
            return {'status' : 'Failed', 'message' : 'Please MakeSure Your PasswordConfirm same With Password'}, 401, {'Content_type' : 'application/json'}
        
        qry.password = args['password']
        db.session.commit()
        return {'status' : 'Success Change Password', 'Your ID' : marshal(qry, Admin.response_field)}, 200, {'Content_type' : 'application/json'}

    # def post(self, admin_id = None):
    #     if admin_id == None:
    #         return {'status' : 'Failed', 'message' : 'Access /admin/api/admin/register'}, 404, {'Content_type' : 'application/json'}
    #     elif admin_id == 'register':
    #         parser = reqparse.RequestParser()
    #         parser.add_argument('username', location = 'json', required = True)
    #         parser.add_argument('password', location = 'json', required = True)
    #         parser.add_argument('nama', location = 'json', required = True)
    #         parser.add_argument('alamat', location = 'json', default = 'You Can Change It later')
    #         args = parser.parse_args()

    #         admin = Admin(args['username'], args['password'],args['nama'],args['alamat'],'admin','admin')
    #         db.session.add(admin)
    #         db.session.commit()

    #         return {'status' : 'Success', 'Your Account' : marshal(admin, Admin.response_field)}, 200, {'Content_type' : 'application/json'}
    #     else:
    #         return {'status' : 'Failed', 'message' : 'Wrong Register Page'}, 404, {'Content_type' : 'application/json'}


api.add_resource(AdminResource, '', '/<admin_id>')