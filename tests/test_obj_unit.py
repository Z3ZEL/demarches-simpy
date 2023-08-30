import pytest
import sys
sys.path.append('..')
from src.demarches_simpy.dossier import Dossier, DossierState
from src.demarches_simpy.connection import RequestBuilder, Profile
from src.demarches_simpy.fields import Field
from src.demarches_simpy.utils import DemarchesSimpyException

from tests.fake_api import FakeRequestBuilder, FakeResponse


    

class TestDossierNoError():
    def CONTENT(request : RequestBuilder):
        # RAW
        data = {
            "data": {
                "dossier": {
                    "id": "123",
                    "number": 1234,
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
        if request.is_variable_set("includeFields"):
            data['data']['dossier']['champs'] = [
                {
                    "__typename" : "None",
                    "id" : "123",
                    "label" : "foo",
                    "stringValue" : "value",
                }
            ]
        if request.is_variable_set('includeAnnotations'):
            data['data']['dossier']['anotations'] = [
                {
                    "__typename" : "None",
                    "id" : "123",
                    "label" : "foo",
                    "stringValue" : "value",
                }
            ]
        return data
            


    @pytest.fixture
    def dossier(self):
        profile = Profile('')
        resp = FakeResponse(200, TestDossierNoError.CONTENT)
        request = FakeRequestBuilder(profile, resp)
        dossier = Dossier(None,profile,request=request)
        return dossier
    
    def test_get_id(self, dossier):
        assert dossier.get_id() == "123"

    def test_str(self, dossier):
        string = str(dossier)
        assert "123" in string
    
    def test_demarche_id(self, dossier : Dossier):
        assert dossier.get_attached_demarche_id() == "123"
    def test_get_number(self, dossier : Dossier):
        assert dossier.get_number() == 1234
        assert dossier.number == 1234

    def test_get_dossier_state(self, dossier):
        assert dossier.get_dossier_state() == "en_instruction"
        assert dossier.get_dossier_state() == DossierState.INSTRUCTION

    def test_get_fields(self, dossier : Dossier):
        fields = dossier.get_fields()
        assert len(fields) == 1
        field = fields[0]
        assert field.label == "foo"
        assert field.stringValue == "value"
        assert field.id == "123"
    def test_get_instructeurs_info(self, dossier: Dossier):
        instructeurs = dossier.instructeurs_info
        assert len(instructeurs) == 2
        instructeur1 = instructeurs[0]
        instructeur2 = instructeurs[1]

        assert instructeur1['id'] == "123"
        assert instructeur1['email'] == "instructeur1@foo.fr"
        assert instructeur2['id'] == "456"
        assert instructeur2['email'] == "instructeur2@foo.fr"


class TestDossierError():
    @pytest.fixture
    def dossier(self):
        profile = Profile('')
        resp = FakeResponse(400, lambda _ : {'data':{}}, reason="Bad Request") 
        request = FakeRequestBuilder(profile, resp)
        dossier = Dossier(None,profile,request=request)
        return dossier
    
    def test_get_id(self, dossier):
        with pytest.raises(DemarchesSimpyException):
            dossier.get_id()





    



    