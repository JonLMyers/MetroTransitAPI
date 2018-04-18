import requests
import json, time


token = ''

print("######## Pass/Fail ########")
target = 'http://127.0.0.1:5000/registration'
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
data = {'username': 'ben@aaxus.com', 'password': 'password123'}
r = requests.post(target, data=json.dumps(data), headers=headers)
print(r.status_code, r.reason)
print(r.text)
data = json.loads(r.text)
email_token = data['email_token']

print("######## Pass ########")
target = 'http://127.0.0.1:5000/confirm?token=' + email_token
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' +token}
r = requests.get(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)


print("######## Pass/Fail ########")
target = 'http://127.0.0.1:5000/registration'
data2 = {'username': 'anthony@aaxus.com', 'password': 'password124'}
r = requests.post(target, data=json.dumps(data2), headers=headers)
print(r.status_code, r.reason)
print(r.text)
data = json.loads(r.text)
email_token = data['email_token']

print("######## Pass ########")
target = 'http://127.0.0.1:5000/confirm?token=' + email_token
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' +token}
r = requests.get(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)


data3 = {'username': 'jon@aaxus.com', 'password': 'password125'}
target = 'http://127.0.0.1:5000/registration'
r = requests.post(target, data=json.dumps(data3), headers=headers)
print(r.status_code, r.reason)
print(r.text)
data = json.loads(r.text)
email_token = data['email_token']

print("######## Pass ########")
target = 'http://127.0.0.1:5000/confirm?token=' + email_token
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' +token}
r = requests.get(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)


data4 = {'username': 'spiro@aaxus.com', 'password': 'password126'}
target = 'http://127.0.0.1:5000/registration'
r = requests.post(target, data=json.dumps(data4), headers=headers)
print(r.status_code, r.reason)
print(r.text)
data = json.loads(r.text)
email_token = data['email_token']

print("######## Pass ########")
target = 'http://127.0.0.1:5000/confirm?token=' + email_token
headers = {'Content-type': 'application/json', 'Accept': 'text/plain', 'Authorization': 'Bearer ' +token}
r = requests.get(target, headers=headers)
print(r.status_code, r.reason)
print(r.text)