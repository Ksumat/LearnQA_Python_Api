import requests

response = requests.get("https://playground.learnqa.ru/api/long_redirect")

for i in response.history:
    print(i.status_code, i.url)

print(response.status_code, response.url)
