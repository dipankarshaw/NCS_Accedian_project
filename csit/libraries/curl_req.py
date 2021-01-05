import requests
from pprint import pprint
payload = {'username': 'administrator', 'password': 'password'}
r = requests.get('http://httpbin.org/get')
print(r.text)
r = requests.post('http://httpbin.org/post', data=payload)
print(r.history)
print(r.text)
r = requests.post('http://github.com')
print(r.history)
print(r.status_code)