import pytest
import sys
sys.path.append('..')
from src.demarches_simpy.utils import bcolors, DemarchesSimpyException

def test_DemarchesSimpyException():
    with pytest.raises(DemarchesSimpyException) as excinfo:
        raise DemarchesSimpyException()
    assert str(excinfo.value) == f"{bcolors.FAIL} [ERROR] [MAIN] There was an error{bcolors.ENDC}"


from src.demarches_simpy.dossier import DossierState


def test_DossierState_valid_from_str():
    assert DossierState.from_str('en_construction') == DossierState.CONSTRUCTION
    assert DossierState.from_str('en_instruction') == DossierState.INSTRUCTION
    assert DossierState.from_str('accepte') == DossierState.ACCEPTE
    assert DossierState.from_str('refuse') == DossierState.REFUSE
    assert DossierState.from_str('sans_suite') == DossierState.SANS_SUITE

def test_DossierState_invalid_from_str():
    with pytest.raises(ValueError) as excinfo:
        DossierState.from_str('invalid')
    
    with pytest.raises(ValueError) as excinfo:
        DossierState.from_str(None)

def test_DossierState_build_query():
    assert DossierState.__build_query_suffix__(DossierState.CONSTRUCTION) == 'EnConstruction'
    assert DossierState.__build_query_suffix__(DossierState.INSTRUCTION) == 'EnInstruction'
    assert DossierState.__build_query_suffix__(DossierState.ACCEPTE) == 'Accepter'
    assert DossierState.__build_query_suffix__(DossierState.REFUSE) == 'Refuser'
    assert DossierState.__build_query_suffix__(DossierState.SANS_SUITE) == 'ClasserSansSuite'
    