import pytest
import sys
sys.path.append('..')
from src.demarches_simpy.utils import bcolors, ILog, DemarchesSimpyException

def test_bcolors():
    assert bcolors.OKGREEN == '\033[92m'
    assert bcolors.ENDC == '\033[0m'
    assert bcolors.WARNING == '\033[93m'
    assert bcolors.FAIL == '\033[91m'
    assert bcolors.BOLD == '\033[1m'
    assert bcolors.UNDERLINE == '\033[4m'

def test_DemarchesSimpyException():
    with pytest.raises(DemarchesSimpyException) as excinfo:
        raise DemarchesSimpyException()
    assert str(excinfo.value) == f"{bcolors.FAIL} [ERROR] [[MAIN]] There was an error{bcolors.ENDC}"

import pytest

class TestILog:
    @pytest.fixture
    def log(self):
        header = "Test"
        profile = None
        return ILog(header, profile)

    def test_set_verbose(self, log):
        log.set_verbose(True)
        assert log.get_verbose() == True

    def test_get_verbose(self, log):
        assert log.get_verbose() == False

    def test_info(self, log, capsys):
        log.info("Test message")
        captured = capsys.readouterr()
        assert captured.out == "\x1b[92m[Test] Test message\x1b[0m\n"

    def test_error(self, log):
        with pytest.raises(DemarchesSimpyException):
            log.error("Test error")

    def test_warning_displaying_warning_true(self, log, capsys):
        log.warning("Test warning")
        captured = capsys.readouterr()
        assert captured.out == "\x1b[93m[Test] Test warning\x1b[0m\n"

    def test_warning_displaying_warning_false(self, log, capsys):
        log.displaying_warning = False
        log.warning("Test warning")
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_debug_verbose_true(self, log, capsys):
        log.verbose = True
        log.debug("Test debug")
        captured = capsys.readouterr()
        assert captured.out == "\x1b[94m[Test] Test debug\x1b[0m\n"

    def test_debug_verbose_false(self, log, capsys):
        log.debug("Test debug")
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_bold(self, log, capsys):
        log.bold("Test bold")
        captured = capsys.readouterr()
        assert captured.out == "\x1b[1m[Test] Test bold\x1b[0m\n"
