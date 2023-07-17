import pytest
import sys
sys.path.append('..')
from requests import Response
from src.demarches_simpy.dossier import Dossier
from src.demarches_simpy.connection import RequestBuilder, Profile


    

class FakeRequestBuilder(RequestBuilder):
    '''
        Fake a request returning a response or error
    '''
    def __init__(self,profile, response):
        super().__init__(profile, "query/empty.graphql")
        self.response = response
        self.response.set_request(self)
    
    def send_request(self):
        return self.response

class FakeResponse(Response):
    '''
        Fake a response with status code and json
    '''
    def __init__(self, status_code, f_content):
        super().__init__()
        self.status_code = status_code
        self.f_content = f_content

    def set_request(self, request):
        self.request = request

    def json(self):
        return self.f_content(self.request)
    

    

class TestDossierNoError():
    def CONTENT(request : RequestBuilder):
        # RAW
        data = {
            "data": {
                "dossier": {
                    "id": "123",
                    "numero": 123,
                    "state": "en_instruction",
                    "attestation": {
                        "filename" : "",
                        "url": ""
                    },
                    "usager" : {
                        "email" : "foo@foo.fr"
                    },
                    "demarche" : {
                        "id" : "123",
                        "number" : 123,
                    }
                }
            }     
        }
        if request.is_variable_set('includeInstructeurs'):
            data['data']['dossier']['instructeurs'] = [
                {
                    "id" : "123",
                    "email" : "instructeur1@foo.fr"
                },
                {
                    "id" : "456",
                    "email" : "instructeur2@foo.fr"
                }
            ]
        if request.is_variable_set("includeChamps"):
            data['data']['dossier']['champs'] = [
                {
                    "id" : "123",
                    "label" : "foo",
                    "stringValue" : "value"
                }
            ]
        if request.is_variable_set('includeAnotations'):
            data['data']['dossier']['anotations'] = [
                {
                    "id" : "123",
                    "label" : "foo",
                    "stringValue" : "value"
                }
            ]
        return data
            


    @pytest.fixture
    def dossier(self):
        profile = Profile('')
        resp = FakeResponse(200, TestDossierNoError.CONTENT)
        request = FakeRequestBuilder(profile, resp)
        dossier = Dossier(123,profile,request=request)
        return dossier
    
    def test_get_id(self, dossier):
        assert dossier.get_id() == "123"

    def test_get_number(self, dossier):
        assert dossier.get_number() == 123

    def test_get_dossier_state(self, dossier):
        assert dossier.get_dossier_state() == "en_instruction"





    



    