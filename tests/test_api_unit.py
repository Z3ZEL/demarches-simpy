import pytest
import sys
from dotenv import load_dotenv
from os import getenv
sys.path.append('..')
from src.demarches_simpy import Demarche, Profile

load_dotenv()

API_DS_KEY = getenv("API_DS_KEY", "None")
print(API_DS_KEY)


class TestDemarcheNoError():
    @pytest.fixture
    def demarche(self) -> Demarche:
        profile = Profile(API_DS_KEY)
        return Demarche(78680, profile)

    def test_len_dossier(self, demarche : Demarche):
        assert demarche.get_dossiers_count() == 1