""" Token Model """
from mongoengine import *

class RevokedToken(Document):
    jti = StringField(max_length=120, required=True)

    @classmethod
    def is_jti_blacklisted(self, jtokeni):
        for token in RevokedToken.objects(jti = jtokeni):
            return True
        return False
