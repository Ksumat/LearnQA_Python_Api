import requests

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
    POST = requests.post("https://playground.learnqa.ru/api/compare_query_type", data=i)
    PUT = requests.put("https://playground.learnqa.ru/api/compare_query_type", data=i)
    DELETE = requests.delete("https://playground.learnqa.ru/api/compare_query_type", data=i)
    print(f"{i},это GET = {GET.text},это POST = {POST.text},это PUT= {PUT.text},это delete = {DELETE.text}")