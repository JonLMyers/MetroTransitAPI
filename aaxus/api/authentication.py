""" Authentication Managment API """
import json
from flask import jsonify, request
from flask_restful import Resource, reqparse
from aaxus import rest_api
from aaxus.models.user import User
from aaxus.models.token import RevokedToken
from aaxus.services.confirm_email import generate_confirmation_token, confirm_token
from itsdangerous import URLSafeTimedSerializer
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity, get_raw_jwt)

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)

class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}, 500
        if data['password'] == '':
            return {'message': 'A password is required'}, 500
        
        new_user = User(
            username = data['username'],
            display_name = data['username'],
            password_hash = User.hash_password(data['password'])
        )

        email_token = generate_confirmation_token(new_user.username)

        try:
            new_user.save()
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return{
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token,
                'email_token': email_token
            }
        except:
            return{'message': 'Something went wrong'}, 500

class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()

        current_user = User.find_by_username(data['username'])
        if not current_user:
            return {'message': 'User {} Does Not Exist'.format(data['username'])}

        if not current_user.confirmed:
            return {'message': 'User Not Confirmed'}

        if current_user.check_password(data['password']):
            access_token = create_access_token(identity = data['username'])
            refresh_token = create_refresh_token(identity = data['username'])
            return {
                'message': 'Logged in as {}'.format(data['username']),
                'access_token': access_token,
                'refresh_token': refresh_token     
            }
        else:
            return {'message': 'Invalid Credentials'}, 500
        
class ConfirmEmail(Resource):
    def get(self):
        arg = request.args
        print (arg)
        token = arg['token']

        try:
            username = confirm_token(token)
        except:
            return {'message': 'Invalid Token'}, 500

        current_user = User.find_by_username(username)
        if not current_user:
            return {'message': 'User {} Does Not Exist'.format(username)}

        if current_user.confirmed:
            return {'message': 'User already confirmed'}, 500
        else:
            current_user.confirmed = True
            #current_user.confirmed_on = datetime.datetime.now()
            current_user.save()

        return {'message': 'User Confirmed'}

class UserLogoutAccess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.save()
            return {'message': 'Access token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
    
class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti = jti)
            revoked_token.save()
            return {'message': 'Refresh token has been revoked'}
        except:
            return {'message': 'Something went wrong'}, 500
            
class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}
       
class SecretResource(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 42
        }