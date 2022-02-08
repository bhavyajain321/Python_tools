import requests

target_url = "" #your target url
data_dict = {"username": "admin", "password": "password", "Login": "submit"} #data_dict based on the form input fields, u cn see it by inspect on it
response = requests.post(target_url, data=data_dict)
print(response.content)