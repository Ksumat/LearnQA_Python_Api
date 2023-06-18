import pytest
import random
import string
from datetime import datetime
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests

class TestUserEdit(BaseCase):
    edit_params = [
        ("username"),
        ("firstName"),
        ("lastName"),
        ("email")
    ]
    def test_edit_just_created_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Edit
        new_name = "Changed Name"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 200)
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong name of the user after edit"
        )

# - Попытаемся изменить данные пользователя, будучи неавторизованными
    @pytest.mark.parametrize("param", edit_params)
    def test_edit_user_without_auth(self, param):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        user_id = self.get_json_value(response1, "id")

        #Edit
        new_value = "Changed Value"

        response2 = MyRequests.put(
            f"/user/{user_id}",
            data={param: new_value}
        )

        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode("utf-8") == f"Auth token not supplied"

# - Попытаемся изменить данные пользователя, будучи авторизованными другим пользователем
    @pytest.mark.parametrize('param', edit_params)
    def test_edit_user_auth_as_another_user(self, param):
        #создаем юзера которого будем редактировать
        register_data_first = self.prepare_registration_data()
        f_response1 = MyRequests.post("/user/", data=register_data_first)

        Assertions.assert_code_status(f_response1, 200)
        Assertions.assert_json_has_key(f_response1, "id")

        f_email = register_data_first['email']
        f_password = register_data_first['password']
        f_user_id = self.get_json_value(f_response1, "id")

        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, "id")

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Edit
        new_value = f"test" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + "@test.ru"

        response3 = MyRequests.put(
            f"/user/{f_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={param: new_value}
        )

        Assertions.assert_code_status(response3, 200) #думаю код должен быть 400, так как мы редактируем не своего юзера

        f_login_data = {
            'email': f_email,
            'password': f_password
        }
        f_response2 = MyRequests.post("/user/login", data=f_login_data)

        f_auth_sid = self.get_cookie(f_response2, "auth_sid")
        f_token = self.get_header(f_response2, "x-csrf-token")

        response4 = MyRequests.get(
            f"/user/{f_user_id}",
            headers={"x-csrf-token": f_token},
            cookies={"auth_sid": f_auth_sid},
        )

        # response5 = MyRequests.get(
        #     f"/user/{user_id}",
        #     headers={"x-csrf-token": token},
        #     cookies={"auth_sid": auth_sid},
        # Вне зависимости от айди который мы подставляем в PUT, редактируется Юзер, под котором мы залогинились

        Assertions.assert_json_value_by_name(
            response4,
            param,
            register_data_first[param],
            f"For another user was changed param = {param}"
        )

#
# - Попытаемся изменить email пользователя, будучи авторизованными тем же пользователем, на новый email без символа @

    def test_edit_email_without_sym(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Edit
        new_email = f"test" + str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")) + "test.ru"

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"email": new_email}
        )

        Assertions.assert_code_status(response3, 400)
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response4,
            "email",
            register_data["email"],
            F"Email was changed ='{new_email}'"
        )

# - Попытаемся изменить firstName пользователя, будучи авторизованными тем же пользователем, на очень короткое значение в один символ
    def test_edit_firstname_on_short(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
        first_name = register_data['firstName']
        password = register_data['password']
        user_id = self.get_json_value(response1, 'id')

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        #Edit
        new_name = random.choice(string.ascii_letters)

        response3 = MyRequests.put(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
            data={"firstName": new_name}
        )

        Assertions.assert_code_status(response3, 400)
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            register_data["firstName"],
            f"First Name was changed on short ='{new_name}'"
        )