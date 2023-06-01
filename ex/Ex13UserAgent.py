import pytest
import requests



class TestUserAgent:
    user_agent = [
        (('1_agent'),('Mozilla/5.0 (Linux; U; Android 4.0.2; en-us; Galaxy Nexus Build/ICL53F) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'),({'platform': 'Mobile', 'browser': 'No', 'device': 'Android'})),
        (('2_agent'), (
            'Mozilla/5.0 (iPad; CPU OS 13_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/91.0.4472.77 Mobile/15E148 Safari/604.1'),
         ({'platform': 'Mobile', 'browser': 'Chrome', 'device': 'iOS'})),
        (('3_agent'), (
            'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'),
         ({'platform': 'Googlebot', 'browser': 'Unknown', 'device': 'Unknown'})),
        (('4_agent'), (
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.100.0'),
         ({'platform': 'Web', 'browser': 'Chrome', 'device': 'No'})),
        (('5_agent'), (
            'Mozilla/5.0 (iPad; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1'),
         ({'platform': 'Mobile', 'browser': 'No', 'device': 'iPhone'})),

    ]

    @pytest.mark.parametrize("agent, user_agents, expected_value", user_agent)
    def test_user_agent(self, agent, user_agents, expected_value):
        response = requests.get(
            "https://playground.learnqa.ru/ajax/api/user_agent_check",
            headers={
                "User-Agent": user_agents}
        )
        assert response.json()['platform'] == expected_value['platform'], f" {agent},expected platform = {expected_value['platform']}, actual = {response.json()['platform']}"
        assert response.json()['browser'] == expected_value['browser'], f" {agent},expected browser = {expected_value['browser']}, actual = {response.json()['browser']}"
        assert response.json()['device'] == expected_value['device'], f" {agent},expected device = {expected_value['device']}, actual = {response.json()['device']}"
