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
target = 'http://127.0.0.1:5000/ticket/manage'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'start': 'Rochester',
    'end': 'Boston',
    'cost': '20.00' 
}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)
data = json.loads(r.text)
ticket = data['id']
print(ticket)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/ticket/manage'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
data = {
    'start': 'Boston',
    'end': 'Chicago',
    'cost': '100.00' 
}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)
data = json.loads(r.text)
ticket = data['id']
print(ticket)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/ticket/manage'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'authorization': 'Bearer ' + token}
r = requests.get(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)
data = json.loads(r.text)
print(data)