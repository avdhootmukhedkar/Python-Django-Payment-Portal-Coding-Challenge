import requests, json

login_url = 'http://127.0.0.1:8000/users/login/'

payload = {
    "username": "avdhootmukhedkar@gmail.com",
    "email": "avdhootmukhedkar@gmail.com",
    "password": "QWerasdf!@#20"
}

response = requests.post(login_url, data = payload).json()
access_token = response['access_token']

print (access_token)

checkout_url = "http://127.0.0.1:8000/payment/checkout"

payload = {
    "user": 1,
    "total_paid": 600,
    #"order_key": "43256",
    "payment_option": "54543",
    "order_items": [{"product" : "books", "price" : 100, "quantity": 3}, {"product" : "pens", "price" : 200, "quantity": 3}]
}

headers = {"Authorization" : "Bearer "+access_token}

response = requests.post(checkout_url, data = payload, headers = headers)
print (response.text)




