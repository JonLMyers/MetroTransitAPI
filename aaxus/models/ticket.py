""" The Ticket model """
from mongoengine import *
from aaxus.models.user import User
from aaxus.models.organization import Organization

class Ticket(Document):
    
    meta = {'collection':'tickets', 'allow_inheritance': True}

    ticket_id = StringField(required=True)
    start = StringField(max_length=256, required=True)
    end = StringField(required=True)
    cost = StringField(required=True)

    @classmethod
    def find_by_id(self, ID):
        for ticket in Ticket.objects(ticket_id = ID):
            return ticket
    @classmethod
    def find_tickets(self):
        tickets = []
        for ticket in Ticket.objects():
            tickets.append(ticket)
        return tickets