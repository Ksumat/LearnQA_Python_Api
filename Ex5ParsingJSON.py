import json

json_text = '{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}'
pars_json = json.loads(json_text)

second_message = pars_json['messages'][1]
print(f"это сообщение из задания:  {second_message['message']}")

for i in pars_json['messages']:
    print(f"это парсинг двух сообщений {i['message']}")