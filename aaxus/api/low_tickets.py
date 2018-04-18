""" Tickets API """
import json, re, uuid
from flask import jsonify, request
from flask_restful import Resource
from aaxus import rest_api
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from aaxus.models.organization import Organization
from aaxus.models.user import User
from aaxus.models.ticket import Ticket

create_ticket_parser = reqparse.RequestParser()
create_ticket_parser.add_argument('start', help = 'Ticket Tite Required', required = True)
create_ticket_parser.add_argument('end', help = 'Ticket Description Required', required = True)
create_ticket_parser.add_argument('cost', help = 'Ticket Price Required', required = True)

update_ticket_parser = reqparse.RequestParser()
update_ticket_parser.add_argument('id', help = 'Ticket ID Required', required = True)

class ManageTickets(Resource):
    def get(self):
        response = []
        identifier = 1
        tickets = Ticket.find_tickets()
        for tic in tickets:
            ticket_dict = dict(id=tic.ticket_id, start=tic.start, end=tic.end, cost=tic.cost)
            response.append(ticket_dict)
        print(response)
        return jsonify(items=response)


    @jwt_required
    def post(self):
        #target_users = []
        #target_option = 0
        user = User.find_by_username(get_jwt_identity())
        if not user:
            return {'Error': 'User {} does not exist'.format(get_jwt_identity())}

        req_data = create_ticket_parser.parse_args()
        data = request.get_json()

        ID = uuid.uuid4()
        new_ticket = Ticket(
            ticket_id = str(ID),
            start = data['start'],
            end = data['end'],
            cost = data['cost']
        )

        try:
            new_ticket.save()
            return{'id': str(ID)}
        except:
            return{'message': 'Something went wrong'}, 500
    
    @jwt_required
    def put(self):
        target_users = []
        message = {'Ticket': 'Updated'}
        user = User.find_by_username(get_jwt_identity())
        if not user:
            return {'Error': 'User {} does not exist'.format(get_jwt_identity())}
        data = request.get_json()

        ticket = Ticket.find_by_id(data['id'])
        if not ticket:
            return {'Error': 'Ticket does not exist'}

        for setting in data:
            if setting == 'id':
                pass
            elif setting == 'target_users':
                for target_user in data['target_users']:
                    volitile_user = User.find_by_username(target_user)
                    if not volitile_user:
                        return {'Error': 'User {} does not exist'.format(target_user)}
                    else:
                        ticket.add_target_user(volitile_user)

            elif setting == 'target_organization':
                target_org = Organization.find_by_name(data['target_organization'])
                if target_org == None:
                    return {'Error': 'Organization {} does not exist'.format(target_org)}
                else:
                    ticket.target_organization = target_org
            
            elif setting == 'is_active':
                if data['is_active'] == 'True':
                    ticket.is_active = True
                elif data['is_active'] == 'False':
                    ticket.is_active = False
                else:
                    return {'Error': 'Invalid is_active Option.'.format(data['is_active'])}

            elif setting == 'title':
                if data['title'] == None:
                    return {'Error': 'Invalid title.'}
                else:
                  ticket.title = data['title']

            elif setting == 'description':
                if data['description'] == None:
                    return {'Error': 'Invalid Description.'}
                else:
                    ticket.title = data['description']
            else:
                message.update({'Setting_Error': '{} Setting is invalid'.format(setting)})
                
        try:
            ticket.save()
            return message

        except:
            message.update({'Save_Error': 'Something went wrong'})
            return message, 500




        



        


class TicketsApi(Resource):
    """Defines the tickets api endpoint"""
    def post(self):
        """Creates a ticket document and inserts it into the ticket collection"""
        ticket = Ticket.from_json(request.get_data())
        ticket.save()
        return jsonify(ticket)

    def get(self):
        """Searches the tickets collection for tickets"""
        tickets = Ticket.objects(
            description__contains=request.args['description']
        )
        return jsonify(tickets)


class TicketApi(Resource):
    """Defines the ticket api endpoint"""
    def get(self, ticket_id):
        """Gets from the ticket collection the ticket with specified id"""
        ticket = Ticket.objects.get_or_404(id=ticket_id)
        return jsonify(ticket)

    def put(self, ticket_id):
        """Updates the ticket with specified id"""
        ticket = Ticket.objects.get_or_404(id=ticket_id)
        ticket.update()
        return jsonify(ticket)

    def delete(self, ticket_id):
        """Deletes a ticket from the ticket collection"""
        return jsonify({
            'entity':'tickets',
            'method':'DELETE',
            'entityId':ticket_id
        })

