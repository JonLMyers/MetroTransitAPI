""" User Model """
from werkzeug.security import check_password_hash, generate_password_hash
from mongoengine import *
import datetime
import aaxus.config
import jwt

class User(Document):
    username = StringField(max_length=50, required=True, unique=True)
    password_hash = StringField(max_length=128, required=True)
    full_name = StringField(max_length=50, required=False, default='')
    display_name = StringField(max_length=50, required=False, default='', unique=True)
    what_i_do = StringField(max_length=256, required=False, default='')
    phone_number = StringField(max_length=14, required=False, defaut='1-000-000-0000')
    time_zone = StringField(max_length=256, required=False, default='')
    description = StringField(max_length=(256*8), required=False, default='')
    confirmed = BooleanField(deafult=False)

    meta = {'unique': True}

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @classmethod
    def find_by_username(self, user_name):
        for user in User.objects(username = user_name):
            return user

    @classmethod
    def find_by_displayname(self, displayname):
        for user in User.objects(display_name = displayname):
            return user