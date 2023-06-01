import requests

response = requests.get("https://playground.learnqa.ru/api/get_text")
print(response.text)
data = {
            'email':'vinkotov@example.com',
            'password':'1234'
        }

response1 = requests.post("https://playground.learnqa.ru/api/user/login", data=data)
print(response1.text)
print(response1.json())
print(response1.headers)