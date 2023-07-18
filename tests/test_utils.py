import pytest
import sys
sys.path.append('..')
from src.demarches_simpy.utils import bcolors, ILog, DemarchesSimpyException

def test_DemarchesSimpyException():
    with pytest.raises(DemarchesSimpyException) as excinfo:
        raise DemarchesSimpyException()
    assert str(excinfo.value) == f"{bcolors.FAIL} [ERROR] [[MAIN]] There was an error{bcolors.ENDC}"

