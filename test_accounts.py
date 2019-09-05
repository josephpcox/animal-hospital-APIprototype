import pytest
import requests

API_ENDPOINT = 'https://animal-hospital-prototype-back.herokuapp.com/api/accounts'

class Test_Accounts:

    def test_post(self):
        parameters = {'first_name':'test','last_name':'case','email':'test@email.com', 'password':'test'}
        request = requests.post(API_ENDPOINT, parameters)
        response = request.text
        print('The server responded with: ' + response)
        return
