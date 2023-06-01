import requests
import time

response = requests.get("https://playground.learnqa.ru/api/longtime_job")
parse_token = response.json()['token']

response1 = requests.get("https://playground.learnqa.ru/api/longtime_job", params={"token":parse_token})
status = response1.json()['status']

assert status == 'Job is NOT ready'
print(f"status = {status}")


seconds = response.json()['seconds']
time.sleep(seconds)

response2 = requests.get("https://playground.learnqa.ru/api/longtime_job", params={"token":parse_token})

status2 = response2.json()['status']
assert status2 == 'Job is ready'
print(f"status = {status2}")
pars_response2 = response2.json()
result = 'result'
if result in pars_response2:
    print(f"Result = {pars_response2[result]}")
else:
    print(f"Поля {result} в Json нет")