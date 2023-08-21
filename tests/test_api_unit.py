import pytest
import sys
from dotenv import load_dotenv
from os import getenv
sys.path.append('..')
from src.demarches_simpy import Demarche, Profile
from src.demarches_simpy.utils import DemarchesSimpyException

load_dotenv()

API_DS_KEY = getenv("API_DS_KEY", False)
if not API_DS_KEY:
    raise Exception("No API_DS_KEY env var found")


class TestDemarcheNoError():
    @pytest.fixture
    def demarche(self) -> Demarche:
        profile = Profile(API_DS_KEY)
        return Demarche(78680, profile)

    def test_len_dossier(self, demarche : Demarche):
        assert demarche.get_dossiers_count() == 1
    def test_fields_structure(self, demarche : Demarche):
        '''Test if the fields structure is correct'''
        for field in demarche.get_fields().values():
            assert field['__typename'] is not None
            assert field['id'] is not None
            assert field['label'] is not None
            assert field['description'] is not None
            assert len(field.keys()) == 4
    def test_fields_values(self, demarche : Demarche):
        '''Test if the fields values are correct'''
        field = demarche.get_fields()["test-field-1"]
        assert field['label'] == "test-field-1"
        assert field['description'] == "content"
        assert field['__typename'] == "TextChampDescriptor"
        assert field['id'] == "Q2hhbXAtMzQ2Mzk0NA=="
    def test_demarche_info(self, demarche : Demarche):
        assert demarche.get_id() == "UHJvY2VkdXJlLTc4Njgw"
        assert demarche.get_number() == 78680

    def test_str_content(self, demarche : Demarche):
        str_demarche = str(demarche)
        id = demarche.get_id()
        number = demarche.get_number()
        assert id in str_demarche
        assert str(number) in str_demarche

    def test_dossier_info(self, demarche : Demarche):
       assert len(demarche.get_dossier_infos()) == 1

class TestUnknownDemarcheError():
    @pytest.fixture
    def demarche(self) -> Demarche:
        profile = Profile(API_DS_KEY)
        return Demarche(0, profile)

    def test_len_dossier(self, demarche : Demarche):
        #raise because the demarche doesn't exist
        with pytest.raises(DemarchesSimpyException):
            demarche.get_dossiers_count()
    def test_fields_structure(self, demarche : Demarche):
        #raise because the demarche doesn't exist
        with pytest.raises(DemarchesSimpyException):
            demarche.get_fields()
    def test_fields_values(self, demarche : Demarche):
        #raise because the demarche doesn't exist
        with pytest.raises(DemarchesSimpyException):
            demarche.get_fields()
