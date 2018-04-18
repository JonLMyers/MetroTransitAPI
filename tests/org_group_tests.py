import requests
import json

token = ''
email_token = ''

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
target = 'http://127.0.0.1:5000/group/manage'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'name': 'Dev Ops',
    'description': 'Devops', 
    'org_name': 'Aaxus'
}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/group/manage'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'org_name': 'Aaxus',
    'id': 'Dev Ops',
    'description': 'Developer Operations Organization',
    'member_username': ['spiro@aaxus.com', 'anthony@aaxus.com', 'ben@aaxus.com'],
    'admin_username': ['spiro@aaxus.com', 'anthony@aaxus.com'] 
}
r = requests.put(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/group/manage'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'org_name': 'Aaxus',
    'id': 'Dev Ops',
    'remove_admin': ['spiro@aaxus.com'],
    'remove_member': ['ben@aaxus.com']
}
r = requests.put(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/group/manage'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'name': 'Executives',
    'description': 'Devops',
    'org_name': 'Aaxus' 
}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/group/view'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'org_name': 'Aaxus',
    'id': 'Dev Ops', 
}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/group/view?org_name=Aaxus'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
r = requests.get(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)