import json

string_as_json_format = '{"answer": "Hello, Ksusha"}'
obj = json.loads(string_as_json_format)
print(obj['answer'])

key = "answer"

if key in obj:
    print(obj[key])
else:
    print(f"Ключа {key} в Json нет")