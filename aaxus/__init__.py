""" Initializes and configures the flask app / DOM """
import sys
from flask import Flask
from flask_restful import Api
from mongoengine import *
from flask_jwt_extended import JWTManager
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config.from_pyfile('config.py')
#We can change this as new apps are deployed :D<3
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
jwt = JWTManager(app)
rest_api = Api(app)

#db = connect(app.config['MONGODB_DB'])
db = connect('mongoenginetest', host='mongomock://localhost')

import aaxus.api.authentication
rest_api.add_resource(aaxus.api.authentication.UserRegistration, '/registration')
rest_api.add_resource(aaxus.api.authentication.UserLogin, '/login')
rest_api.add_resource(aaxus.api.authentication.UserLogoutAccess, '/logout/access')
rest_api.add_resource(aaxus.api.authentication.UserLogoutRefresh, '/logout/refresh')
rest_api.add_resource(aaxus.api.authentication.TokenRefresh, '/token/refresh')
rest_api.add_resource(aaxus.api.authentication.SecretResource, '/secret')
rest_api.add_resource(aaxus.api.authentication.ConfirmEmail, '/confirm')

import aaxus.api.users
rest_api.add_resource(aaxus.api.users.UserProfile, '/profile/update')
rest_api.add_resource(aaxus.api.users.FindProfile, '/profile/find')

import aaxus.api.organizations
rest_api.add_resource(aaxus.api.organizations.ManageOrganization, '/organization/manage')
rest_api.add_resource(aaxus.api.organizations.ViewOrganization, '/organization/view')

import aaxus.api.org_groups
rest_api.add_resource(aaxus.api.org_groups.ManageOrgGroup, '/group/manage')
rest_api.add_resource(aaxus.api.org_groups.ViewOrgGroup, '/group/view')

import aaxus.api.tickets
rest_api.add_resource(aaxus.api.tickets.ManageTickets, '/ticket/manage')


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return aaxus.models.token.RevokedToken.is_jti_blacklisted(jti)
