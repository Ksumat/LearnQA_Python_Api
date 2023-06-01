import requests
import json

response = requests.post("https://playground.learnqa.ru/api/compare_query_type")
print(response.text, response.status_code)
#1 Возвращается текст : "Wrong method provided", статус код при этом = 200

response = requests.head("https://playground.learnqa.ru/api/compare_query_type",data={"method":"HEAD"})
print(response.text, response.status_code)
#2 Возвращается ошибка 400 (Нет разницы указывать параметр method или нет)

response = requests.get("https://playground.learnqa.ru/api/compare_query_type", params={"method":"GET"})
print(response.text, response.status_code)
#3 Возвращается JSON : "{"success":"!"}", статус код = 200



method = [{"method":"GET"},{"method":"POST"},{"method":"PUT"},{"method":"DELETE"}]

for i in method:
    GET = requests.get("https://playground.learnqa.ru/api/compare_query_type", params=i)
    print(f"GET {i['method']} {GET.text} {GET.status_code}")
    if i['method'] == 'GET' and GET.text != '{"success":"!"}':
        print(f"если запрос GET,а параметр method = {i['method']}, возвращается неправильный ответ = {GET.text}")
    elif i['method'] != 'GET' and GET.text != 'Wrong method provided':
        print(f"если запрос GET,а параметр method = {i['method']}, возвращается неправильный ответ = {GET.text}")

    POST = requests.post("https://playground.learnqa.ru/api/compare_query_type", data=i)
    print(f"POST {i['method']} {POST.text} {POST.status_code}")
    if i['method'] == 'POST' and POST.text != '{"success":"!"}':
        print(f"если запрос POST,а параметр method = {i['method']}, возвращается неправильный ответ = {POST.text}")
    elif i['method'] != 'POST' and POST.text != 'Wrong method provided':
        print(f"если запрос POST,а параметр method = {i['method']}, возвращается неправильный ответ = {POST.text}")

    PUT = requests.put("https://playground.learnqa.ru/api/compare_query_type", data=i)
    print(f"PUT {i['method']} {PUT.text} {PUT.status_code}")
    if i['method'] == 'PUT' and PUT.text != '{"success":"!"}':
        print(f"если запрос PUT,а параметр method = {i['method']}, возвращается неправильный ответ = {PUT.text}")
    elif i['method'] != 'PUT' and PUT.text != 'Wrong method provided':
        print(f"если запрос PUT,а параметр method = {i['method']}, возвращается неправильный ответ = {PUT.text}")

    DELETE = requests.delete("https://playground.learnqa.ru/api/compare_query_type", data=i)
    print(f"DELETE {i['method']} {DELETE.text} {DELETE.status_code}")
    if i['method'] == 'DELETE' and DELETE.text != '{"success":"!"}':
        print(f"если запрос DELETE,а параметр method = {i['method']}, возвращается неправильный ответ = {DELETE.text}")
    elif i['method'] != 'DELETE' and DELETE.text != 'Wrong method provided':
        print(f"если запрос DELETE,а параметр method = {i['method']}, возвращается неправильный ответ = {DELETE.text}")
#4 если запрос DELETE,а параметр method = GET, возвращается неправильный ответ = {"success":"!"}