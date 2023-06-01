import requests

def test_print_cookie():
    response = requests.post("https://playground.learnqa.ru/api/homework_header")
    print(response.headers)
    assert response.headers["x-secret-homework-header"] == 'Some secret value', f"Header - x-secret-homework-header != Some secret value"