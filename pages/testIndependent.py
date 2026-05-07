import requests
import requests

response = requests.post(
    "https://automationexercise.com/api/verifyLogin",
    data={"email": "test2028now@yopmail.com", "password": "test"}
)
print(response.status_code)
print(response.text)