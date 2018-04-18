""" The Comment model """
from mongoengine import *
from aaxus.models.user import User
from aaxus.models.organization import Organization

class Comment(Document):
    
    meta = {'collection':'comments', 'allow_inheritance': True}

    ticket_id = StringField(required=True)
    user = ReferenceField(User, required=True)
    body = StringField(required=True)
    #datetime
    

    def add_user(self, target_user):
        for user in self.target_users:
            if user == target_user:
                return False
        self.target_users.append(target_user)
    
    @classmethod
    def find_by_id(self, ID):
        for ticket in Ticket.objects(ticket_id = ID):
            return ticket