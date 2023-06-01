import requests


def test_print_cookie():
    response = requests.post("https://playground.learnqa.ru/api/homework_cookie")
    print(response.cookies)
    assert response.cookies["HomeWork"] == 'hw_value', f"Cookies != HomeWork=hw_value"
