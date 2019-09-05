import pytest
import requests
from flask import jsonify

API_ENDPOINT = 'https://animal-hospital-prototype-back.herokuapp.com/api/accounts'


class TestAccounts:

    def test_post(self):
        parameters = {'first_name': 'test', 'last_name':'case', 'email': 'test@email.com', 'password': 'test'}
        request = requests.post(url=API_ENDPOINT, json=parameters)
        assert(request.status_code == 200)
        return

    def test_put(self):
        parameters = {'first_name': 'test update', 'last_name': 'put case', 'email': 'test@email.com',
                      'password': 'put test'}
        request = requests.put(url=API_ENDPOINT, json=parameters)
        assert (request.status_code == 200)
        return
