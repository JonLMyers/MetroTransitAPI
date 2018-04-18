""" User Managment API """
import json, re
from flask import jsonify, request
from flask_restful import Resource
from aaxus import rest_api
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from aaxus.models.user import User

parser = reqparse.RequestParser()
parser.add_argument('password', help = 'Optional')
parser.add_argument('full_name', help = 'Optional')
parser.add_argument('display_name', help = 'Optional')
parser.add_argument('what_i_do', help = 'Optional')
parser.add_argument('phone_number', help = 'Optional')
parser.add_argument('time_zone', help = 'Optional')
parser.add_argument('description', help = 'Optional')

lookup_parser = reqparse.RequestParser()
lookup_parser.add_argument('display_name', help='Display_Name Required', required = True)

class UserProfile(Resource):
    @jwt_required
    def put(self):
        data = parser.parse_args()
        message = {'Message': 'Profile for {} Updated'.format(get_jwt_identity())}
        user = User.find_by_username(get_jwt_identity())
        if not user:
            return {'Error': 'User {} does not exist'.format(get_jwt_identity())}

        for setting in data:
            if setting == 'password':
                if data['password'] == '':
                    message.update({'Password_Error': 'Password cannot be blank'})
                else:
                    user.password_hash = User.hash_password(data['password'])
                    message.update({'Password_Message':'Password Updated'})

            elif setting == 'full_name':
                filtered_input = anti_xss(data['full_name'])
                if filtered_input and data['full_name'] != '':
                    user.full_name = filtered_input
                    message.update({'Fullname_Message': 'Full Name: {}'.format(filtered_input)})
                else:
                    message.update({'Fullname_Error': 'Invalid Full Name'})

            elif setting == 'display_name':
                filtered_input = anti_xss(data['display_name'])
                if filtered_input and data['display_name'] != '':
                    user.display_name = filtered_input
                    message.update({'Displayname_Message': 'Display Name: {}'.format(filtered_input)})
                else:
                    message.update({'Displayname_Error': 'Invalid Display Name'})

            elif setting == 'what_i_do':
                if filtered_input and data['what_i_do'] != '':
                    user.what_i_do = filtered_input
                    message.update({'What_I_Do_Message': 'Information: {}'.format(filtered_input)})
                else:
                    message.update({'What_I_Do_Error': 'Malformed "What I do" input'})
            
            elif setting == 'phone_number':
                #We want input 1-555-555-5555
                #The country code can be more than 1 digit :(
                phonePattern = re.compile("(\(?\d{3}\D{0,3}\d{3}\D{0,3}\d{4}).*?")
                matched_num = phonePattern.match(data['phone_number'])
                matched_num = matched_num.group(0)
                print (matched_num)
                if matched_num:
                    user.phone_number = matched_num
                    message.update({'Phone_Message': 'Phone Number: {}'.format(matched_num)})
                else:
                    message.update({'Phone_Error': 'Invalid phone number'})

            elif setting == 'time_zone':
                #Doing this makes me sick.  Someone else please do.
                pass

            elif setting == 'description':
                if filtered_input and data['description'] != '':
                    user.description = filtered_input
                    message.update({'Description_Message': 'Description: {}'.format(filtered_input)})
                else:
                    message.update({'Description_Error': 'Invalid Description'})
            else:
                message.update({'Error': 'Setting: {} is invlaid.'.format(setting)})
        try:
            user.save()
            return message
        except:
            message.update({'Save_Error': 'Something went wrong'})
            return message, 500

    @jwt_required
    def get(self):
        user = User.find_by_username(get_jwt_identity())
        if not user:
            return {'Error': 'User {} does not exist'.format(get_jwt_identity())}
        else:
            return {
                'Message': 'Profile',
                'full_name': '{}'.format(user.full_name),
                'display_name': '{}'.format(user.display_name),
                'what_i_do': '{}'.format(user.what_i_do),
                'phone_number': '{}'.format(user.phone_number),
                'description': '{}'.format(user.description)
            }

class FindProfile(Resource):
    @jwt_required
    def post(self):
        data = parser.parse_args()
        displayname = data['display_name']
        user = User.find_by_displayname(displayname)
        if not user:
            return {'Error': 'User does not exist'}
        else:
            return {
                'Message': 'Profile',
                'full_name': '{}'.format(user.full_name),
                'display_name': '{}'.format(user.display_name),
                'what_i_do': '{}'.format(user.what_i_do),
                'phone_number': '{}'.format(user.phone_number),
                'description': '{}'.format(user.description)
            }




