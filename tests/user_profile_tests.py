import requests
import json

token = ''

print("######## Pass ########")
target = 'http://127.0.0.1:5000/login'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {'username': 'jon@aaxus.com', 'password': 'password125'}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)
data = json.loads(r.text)
token = data['access_token']

print("######## Pass ########")
target = 'http://127.0.0.1:5000/profile/update'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
r = requests.get(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/profile/update'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'display_name': 'jon@aaxus.com',
    'password': 'password125', 
    'phone_number': '4409880123', 
    'what_i_do': 'Nothing',
    'description': 'A test user.',
    'full_name': 'Test User'
}
r = requests.put(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/profile/find'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {'display_name': 'test@testing.com'}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)