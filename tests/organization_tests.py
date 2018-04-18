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
print(token)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/organization/manage'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'name': 'Aaxus'
}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/organization/manage'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'id': 'Aaxus',
    'member_username': ['spiro@aaxus.com', 'anthony@aaxus.com', 'ben@aaxus.com', 'test@testing.com'],
    'admin_username': ['spiro@aaxus.com', 'anthony@aaxus.com'] 
}
r = requests.put(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/organization/manage'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'id': 'Aaxus',
    'remove_admin': ['spiro@aaxus.com'],
    'remove_member': ['test@testing.com']
}
r = requests.put(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/organization/view'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'id': 'Aaxus', 
}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)