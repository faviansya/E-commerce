import logging, json
from flask import Blueprint
from flask_restful import Api, Resource, reqparse, marshal
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, get_jwt_claims
from blueprints.user import *
from blueprints.admin import *

bp_auth = Blueprint('auth', __name__)
api = Api(bp_auth)

class CreateTokenResources(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', location='args', required=True)
        parser.add_argument('password', location = 'args', required = True)
        parser.add_argument('admin', location = 'args')
        args = parser.parse_args()

        qry = User.query.filter_by(username = args['username']).filter_by(password = args['password']).first()
        qry_admin = Admin.query.filter_by(username = args['username']).filter_by(password = args['password']).first()
        if qry_admin is not None and args['admin'] == 'admin':
            token = create_access_token(marshal(qry_admin, Admin.response_field))
        elif qry is not None:
            token = create_access_token(marshal(qry, User.response_field))
        else:
            return {'status' : 'UNAUTHORIZED', 'message' : 'Invalid key'}, 401, {'Content_type' : 'application/json'}
        return {'token' : token}, 200, {'Content_type' : 'application/json'}

api.add_resource(CreateTokenResources, '')