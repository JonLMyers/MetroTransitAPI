""" Organization Managment API """
import json, re
from flask import jsonify, request
from flask_restful import Resource
from aaxus import rest_api
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from aaxus.models.organization import Organization
from aaxus.models.user import User
from aaxus.models.org_group import OrgGroup
from aaxus.services.token_service import generate_confirmation_token, confirm_token

create_org_parser = reqparse.RequestParser()
create_org_parser.add_argument('name', help = 'Organization Name Required', required = True)

update_org_parser = reqparse.RequestParser()
update_org_parser.add_argument('id', help = 'Organization Name Required', required = True)

view_org_parser = reqparse.RequestParser()
view_org_parser.add_argument('id', help = 'Organization Name Required', required = True)

class ManageOrganization(Resource):
    @jwt_required
    def post(self):
        user = User.find_by_username(get_jwt_identity())
        if not user:
            return {'Error': 'User {} does not exist'.format(get_jwt_identity())}

        data = create_org_parser.parse_args()
        if Organization.find_by_name(data['name']):
            return {'error': 'Organization already exists'}, 500
        
        token = generate_confirmation_token(data['name'])

        new_org = Organization(
            name = data['name'],
            join_token = token
        )
        new_org.add_member(user)
        new_org.add_admin(user)

        try:
            new_org.save()
            return{
                'message': 'Organization {} was created'.format(data['name'])
            }
        except:
            return{'message': 'Something went wrong'}, 500

    @jwt_required
    def put(self):
        memberadd = 0
        adminadd = 0
        memberremove = 0
        adminremove = 0

        message = {'Organization': 'Updated'}
        user = User.find_by_username(get_jwt_identity())
        if not user:
            return {'Invalid_User_Error': 'User {} does not exist'.format(get_jwt_identity())}

        #data = update_org_parser.parse_args()
        data = request.get_json()
        org = Organization.find_by_name(data['id'])
        if org == None:
            return {'No_Org_Error': 'Organization does not exist'}, 500

        if not org.is_admin(user.username):
            return {'Not_Authorized_Error': 'Not an admin of this organization'}, 500

        for setting in data:
            if setting == 'id' or data[setting] == None:
                pass
            elif setting == 'admin_username':
                for user in data['admin_username']:
                    target_user = User.find_by_username(user)
                    if not target_user:
                        message.update({'Admin_Add_Error': 'User does not exist'})
                    org.add_admin(target_user)
                    adminadd += 1
                    message.update({'Admin_Added{}'.format(adminadd): '{}'.format(user)})

            elif setting == 'member_username':
                for user in data['member_username']:
                    target_user = User.find_by_username(user)
                    if not target_user:
                        message.update({'Member_Add_Error': 'User does not exist'})
                        print (user)
                    org.add_member(target_user)
                    memberadd += 1
                    message.update({'User_Added{}'.format(memberadd): '{}'.format(user)})

            elif setting == 'remove_admin':
                for user in data['remove_admin']:
                    target_user = User.find_by_username(user)
                    if not target_user:
                        message.update({'Admin_Remove_Error': 'User does not exist'})
                    org.remove_admin(target_user)
                    adminremove += 1
                    message.update({'Admin_Removed{}'.format(adminremove): '{}'.format(user)})

            elif setting == 'remove_member':
                for user in data['remove_member']:
                    target_user = User.find_by_username(user)
                    if not target_user:
                        message.update({'Member_Remove_Error': 'User does not exist'})
                    org.remove_member(target_user)
                    memberremove += 1
                    message.update({'User_Removed{}'.format(memberremove): '{}'.format(user)})
            else:
                message.update({'Setting_Error': '{} Setting is invalid'.format(setting)})
                
        try:
            org.save()
            return message
        except:
            message.update({'Save_Error': 'Something went wrong'})
            return message, 500

class ViewOrganization(Resource):
    @jwt_required
    def post(self):
        message = {'Organization':'Info'}
        user = User.find_by_username(get_jwt_identity())
        if not user:
            return {'Invalid_User_Error': 'User {} does not exist'.format(get_jwt_identity())}

        data = view_org_parser.parse_args()
        org = Organization.find_by_name(data['id'])
        if org == None:
            return {'No_Org_Error': 'Organization does not exist'}, 500

        if not org.is_member(user):
            return {'Invalid_User_Error': 'You are not a memeber of this organization.'}
    
        member_list = []
        admin_list = []

        message = {'Organization': org.name}
        
        for member in org.members:
            member_list.append(member.username)
        for admin in org.administrators:
            admin_list.append(admin.username)

        message.update({'Members': member_list})
        message.update({'Administrators': admin_list})
        return message

