import requests

session = requests.Session()  # Maintain session across requests

# Set session data via POST
response = session.post('http://127.0.0.1:5000/login_post', json={"username": "andy",
                                                                  "password": "pass"})
print(response.json())

# Retrieve session data via GET
response = session.get('http://127.0.0.1:5000/api/group_list')
print(response.json())
response = session.get('http://127.0.0.1:5000/delete_session')
print(response.json())
