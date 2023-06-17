from json.decoder import JSONDecodeError
import requests


payload = {"name":"Ksusha"}
response = requests.get("https://playground.learnqa.ru/api/hello", params=payload)
print(response)
try:
    parsed_response_text = response.json()
    print(parsed_response_text["answer"])
except JSONDecodeError:
    print("Response is not a JSON format")


response300 = requests.post("https://playground.learnqa.ru/api/get_301", allow_redirects=True)
first_response = response300.history[0]
second_response = response300
for i in response300.history:
    print(i)
    print(i.url)

print(response300.status_code)
print(first_response.url)
print(second_response.url)



headers1 = {"some_header":"123"}
responseh = requests.get("https://playground.learnqa.ru/api/show_all_headers", headers=headers1)

print(responseh.text)
print(responseh.headers)


payload1 = {"login":"secret_login", "password":"secret_pass"}
response1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload1)

cookie_value = response1.cookies.get('auth_cookie')

cookies = {}
if cookie_value is not None:
    cookies.update({'auth_cookie': cookie_value})

response2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", cookies=cookies)

print(response2.text)
