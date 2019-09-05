import pytest
import requests
from flask import jsonify

API_ENDPOINT = 'https://animal-hospital-prototype-back.herokuapp.com/api/accounts'

class Test_Accounts:

    def test_post(self):
        parameters = {'first_name':'test','last_name':'case','email':'test@email.com', 'password':'test'}
        request = requests.post(url=API_ENDPOINT, json=parameters)
        return
