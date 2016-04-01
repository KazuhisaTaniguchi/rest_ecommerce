import requests

base_url = 'http://127.0.0.1:8000/api/'

login_url = base_url + 'auth/token/'
products_url = base_url + 'products/'
refresh_url = login_url + 'refresh/'


data = {
    'username': 'taniguchi',
    'password': 'kazuhisa96',
}
login_request = requests.post(login_url, data=data)

json_data = login_request.json()

import json
print json.dumps(json_data, indent=2)
# get token
token = json_data['token']

headers = {
    'Authorization': 'JWT %s' % (token),
}
product_request = requests.get(products_url, headers=headers)
print product_request.text
print (json.dumps(product_request.json(), indent=2))


# Refresh URL TOKEN
data = {
    'token': token,
}
refresh_request = requests.post(refresh_url, data=data)
print refresh_request.json()
token = refresh_request.json()['token']
