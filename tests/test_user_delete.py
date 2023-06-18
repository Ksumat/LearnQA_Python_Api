from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


class TestUserDelete(BaseCase):

    def test_delete_main_user(self):
        main_user_data = {
            'id': '2',
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response1 = MyRequests.post("/user/login", data=main_user_data)
        Assertions.assert_code_status(response1, 200)

        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")

        response2 = MyRequests.delete(
            f"/user/{main_user_data['id']}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response2, 400)
        assert response2.content.decode(
            "utf_8") == "Please, do not delete test users with ID 1, 2, 3, 4 or 5.", f"user with id {main_user_data['id']} was delete"

    # Второй - позитивный. Создать пользователя, авторизоваться из-под него, удалить, затем попробовать получить его данные по ID и убедиться, что пользователь действительно удален.
    def test_just_delete_user(self):
        register_data = self.prepare_registration_data()
        response1 = MyRequests.post("/user/", data=register_data)

        Assertions.assert_code_status(response1, 200)
        Assertions.assert_json_has_key(response1, "id")

        email = register_data['email']
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

        # DELETE
        response3 = MyRequests.delete(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response3, 200)
        response4 = MyRequests.get(
            f"/user/{user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )
        Assertions.assert_code_status(response4, 404)
        assert response4.content.decode("utf_8") == "User not found", f"The user has not been deleted"

    # Третий - негативный, попробовать удалить пользователя, будучи авторизованными другим пользователем.
    def test_delete_another_user(self):
        # Создаем пользователя которого будем удалять
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
        password = register_data['password']

        # Login
        login_data = {
            'email': email,
            'password': password
        }
        response2 = MyRequests.post("/user/login", data=login_data)

        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")

        response3 = MyRequests.delete(
            f"/user/{f_user_id}",
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid},
        )

        Assertions.assert_code_status(response3, 200)  # думаю код должен быть 400, так как мы даляем не своего юзера

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
        Assertions.assert_code_status(response4, 200)
        assert response4.content.decode("utf-8") != "User not found", "User was deleted"

    #  response5 = MyRequests.get(
    #      f"/user/{user_id}",
    #      headers={"x-csrf-token": token},
    #      cookies={"auth_sid": auth_sid},
    #  )
    # # Вне зависимости от айди который мы подставляем в PUT, удаляется Юзер, под котором мы залогинились
    #  print(response5.content)
