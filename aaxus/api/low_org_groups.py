""" Org Group Managment API """
import json, re
from flask import jsonify, request
from flask_restful import Resource
from aaxus import rest_api
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from aaxus.models.org_group import OrgGroup
from aaxus.models.organization import Organization
from aaxus.models.user import User

create_group_parser = reqparse.RequestParser()
create_group_parser.add_argument('name', help = 'Group Name Required', required = True)
create_group_parser.add_argument('description', help = 'Group Description Required', required = True)
create_group_parser.add_argument('org_name', help = 'Organization Name Required', required = True)

update_group_parser = reqparse.RequestParser()
update_group_parser.add_argument('id', help = 'Group Name Required', required = True)
update_group_parser.add_argument('org_name', help = 'Organization Name Required', required = True)

view_group_parser = reqparse.RequestParser()
view_group_parser.add_argument('id', help = 'Group Name Required', required = True)
view_group_parser.add_argument('org_name', help = 'Organization Name Required', required = True)

class ManageOrgGroup(Resource):
    def post(self):
        user = User.find_by_username(data['user'])
        if not user:
            return {'Error': 'User {} does not exist'.format(data['user'])}

        data = create_group_parser.parse_args()
        
        org = Organization.find_by_name(data['org_name'])
        if(org):
            if(org.is_member(user)):
                if OrgGroup.find_by_name(data['name']):
                    return {'error': 'Organization already exists'}, 500
                else:
                    pass
            else:
                return {'error': 'Not a Member of this organization'}
        else:
            return {'error': 'Organization does not exist.'}

        new_group = OrgGroup(
            name = data['name'],
            description = data['description']
        )
        new_group.add_member(user)
        new_group.add_admin(user)

        try:
            new_group.save()
            org.add_org_group(new_group)
            return{
                'message': 'Organization {} was created'.format(data['name'])
            }
        except:
            return{'message': 'Something went wrong'}, 500

    def put(self):
        memberadd = 0
        adminadd = 0
        memberremove = 0
        adminremove = 0

        message = {'Organization': 'Updated'}
        user = User.find_by_username(data['user'])
        if not user:
            return {'Invalid_User_Error': 'User {} does not exist'.format(data['user'])}

        #data = update_org_parser.parse_args()
        data = request.get_json()
        org = Organization.find_by_name(data['org_name'])
        org_group = OrgGroup.find_by_name(data['id'])
        if org == None:
            return {'No_Org_Error': 'Organization does not exist'}, 500
        elif org_group == None:
            return {'No_Org_Group_Error': 'Group does not exist'}, 500

        if not org_group.is_admin(user.username):
            return {'Not_Authorized_Error': 'Not an admin of this organization'}, 500

        for setting in data:
            if setting == 'id' or data[setting] == None or setting == 'org_name':
                pass
            elif setting == 'new_name':
                if OrgGroup.find_by_name(data['new_name']):
                    message.update({'New_Name_Error': 'Organization already exists'})
                else:
                    org_group.name = data['new_name']
                    message.update({'Name': 'Updated'})

            elif setting == 'admin_username':
                for user in data['admin_username']:
                    target_user = User.find_by_username(user)
                    if not target_user:
                        message.update({'Admin_Add_Error': 'User does not exist'})
                    org_group.add_admin(target_user)
                    adminadd += 1
                    message.update({'Admin_Added{}'.format(adminadd): '{}'.format(user)})

            elif setting == 'member_username':
                for user in data['member_username']:
                    target_user = User.find_by_username(user)
                    if not target_user:
                        message.update({'Member_Add_Error': 'User does not exist'})
                    org_group.add_member(target_user)
                    memberadd += 1
                    message.update({'User_Added{}'.format(memberadd): '{}'.format(user)})

            elif setting == 'description':
                org_group.description == data['description']
                message.update({'Description': 'Updated'})

            elif setting == 'remove_admin':
                for user in data['remove_admin']:
                    target_user = User.find_by_username(user)
                    if not target_user:
                        message.update({'Admin_Remove_Error': 'User does not exist'})
                    org_group.remove_admin(target_user)
                    adminremove += 1
                    message.update({'Admin_Removed{}'.format(adminremove): '{}'.format(user)})

            elif setting == 'remove_member':
                for user in data['remove_member']:
                    target_user = User.find_by_username(user)
                    if not target_user:
                        message.update({'Member_Remove_Error': 'User does not exist'})
                    org_group.remove_member(target_user)
                    memberremove += 1
                    message.update({'User_Removed{}'.format(memberremove): '{}'.format(user)})
            else:
                message.update({'Setting_Error': '{} Setting is invalid'.format(setting)})       
        try:
            org_group.save()
            return message
        except:
            message.update({'Save_Error': 'Something went wrong'})
            return message, 500

class ViewOrgGroup(Resource):
    def get(self):

        user = User.find_by_username(data['user']
        if not user:
            return {'Invalid_User_Error': 'User {} does not exist'.format(data['user'])}

        org_name = request.args.get('org_name')
        org = Organization.find_by_name(org_name)

        if org == None:
            return {'No_Org_Error': 'Organization does not exist'}, 500

        if not org.is_member(user):
            return {'Not_Authorized_Error': 'Not an admin of this organization'}, 500

        group_names = []
        org_groups = org.find_all_org_groups()
        for group in org_groups:
            print (group.name)
            group_names.append(group.name)

        message = {'Organizations': group_names}
        return message, 200

    def post(self):
        message = {'Group': 'List'}
        user = User.find_by_username(data['user']
        if not user:
            return {'Invalid_User_Error': 'User {} does not exist'.format(data['user'])}

        data = view_group_parser.parse_args()
        org = Organization.find_by_name(data['org_name'])
        if org == None:
            return {'No_Org_Error': 'Organization does not exist'}, 500

        org_group = org.find_org_group_by_name(data['id'])
        print (org_group)

        if org_group:
            message = {'Organization': org_group.name}
            message.update({'Description': org.description})
            
            for member in org_group.members:
                member_list.append(member.username)
            for admin in org_group.administrators:
                admin_list.append(admin.username)

            message.update({'Members': member_list})
            message.update({'Administrators': admin_list})

        return message