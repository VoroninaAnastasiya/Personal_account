import requests

connect = requests.get('https://mail.ru')
print(connect.text)
print(connect.__dict__)