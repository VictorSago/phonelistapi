import requests

def get_phone(name):
    request = requests.get(f'http://localhost:5000/api?action=phone&name={name}')
    return request.text

def get_name(phone):
    request = requests.get(f'http://localhost:5000/api?action=name&phone={phone}')
    return request.text
