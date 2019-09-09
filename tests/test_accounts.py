import pytest
import requepipsts
from flask import jsonify

API_ENDPOINT = 'https://animal-hospital-prototype-back.herokuapp.com/api/accounts'


class TestAccounts:

    @staticmethod
    def test_post():
        parameters = {'first_name': 'test', 'last_name': 'case', 'email': 'test@email.com', 'password': 'test'}
        request = requests.post(url=API_ENDPOINT, json=parameters)
        assert(request.status_code == 200)
        return

    @staticmethod
    def test_put():
        parameters = {'first_name': 'test update', 'last_name': 'put case', 'email': 'test@email.com',
                      'password': 'put test'}
        request = requests.put(url=API_ENDPOINT, json=parameters)
        assert (request.status_code == 200)
        return

    @staticmethod
    def test_delete():
        parameters = {'email': 'test@email.com'}
        request = requests.delete(url = API_ENDPOINT, json=parameters)
        assert(request.status_code == 200)
        return
