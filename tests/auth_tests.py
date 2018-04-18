import requests
import json

token = ''
email_token = ''

print("######## Pass/Fail ########")
target = 'http://127.0.0.1:5000/registration'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {'username': 'test@testing.com', 'password': 'password123'}
r = requests.post(target, data=json.dumps(data), headers=headers)
data = json.loads(r.text)
email_token = data['email_token']
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/confirm?token=' + email_token
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' +token}
r = requests.get(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Fail ########")
target = 'http://127.0.0.1:5000/registration'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {'username': 'test@testing.com', 'password': ''}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/login'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {'username': 'test@testing.com', 'password': 'password123'}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)
data = json.loads(r.text)
token = data['access_token']
print(token)

print("######## Fail ########")
target = 'http://127.0.0.1:5000/login'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {'username': 'test@testing.com', 'password': 'password321'}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/secret'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' +token}
r = requests.get(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Pass ########")
target = 'http://127.0.0.1:5000/logout/access'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' +token}
r = requests.post(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)

print("######## Fail ########")
target = 'http://127.0.0.1:5000/secret'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' +token}
r = requests.get(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)



