import pytest
import sys
from dotenv import load_dotenv
from os import getenv
sys.path.append('..')
from src.demarches_simpy import StateModifier, Profile, Demarche, Dossier, DossierState, MessageSender, AnnotationModifier, FileUploader
from src.demarches_simpy.utils import DemarchesSimpyException
load_dotenv()

API_DS_KEY = getenv("API_DS_KEY", False)
if not API_DS_KEY:
    raise Exception("No API_DS_KEY env var found")
profile = Profile(API_DS_KEY, verbose=True)
demarche = Demarche(78680, profile)



class TestActionStateModifier():
    def reset_state(self, dossier : Dossier, state_modifier : StateModifier):
        state_modifier = StateModifier(profile=profile, dossier=dossier)
        state_modifier.perform(DossierState.INSTRUCTION)
        assert dossier.force_fetch().get_dossier_state() == 'en_instruction'


    @pytest.fixture
    def dossier(self) -> Dossier:
        dossier = demarche.get_dossiers()[0]
        instructeur_id = demarche.get_instructeurs_info()[0]['id']
        profile.set_instructeur_id(instructeur_id)
        return dossier
    @pytest.fixture
    def state_modifier(self, dossier : Dossier) -> StateModifier:
        return StateModifier(profile=profile, dossier=dossier)
    

    def test_state_modifier_with_no_error(self, dossier : Dossier, state_modifier : StateModifier):
        self.reset_state(dossier, state_modifier)
        assert dossier.get_dossier_state() == 'en_instruction'
        assert state_modifier.perform(DossierState.ACCEPTE) == 0
        assert dossier.force_fetch().get_dossier_state() == 'accepte'
        self.reset_state(dossier, state_modifier)


class TestActionMessageModifier():
    @pytest.fixture
    def dossier(self) -> Dossier:
        print(demarche.get_dossiers())
        dossier = demarche.get_dossiers()[0]
        instructeur_id = demarche.get_instructeurs_info()[0]['id']
        profile.set_instructeur_id(instructeur_id)
        return dossier
    @pytest.fixture
    def sender(self, dossier : Dossier) -> MessageSender:
        return MessageSender(profile=profile, dossier=dossier)
    
    def test_message_sender_with_no_error(self, dossier : Dossier, sender : MessageSender):
        assert sender.perform("Test message") == 0

class TestActionAnnotationModifier():
    def reset_annotation(self, dossier: Dossier, annotation_modifier: AnnotationModifier):
        annotation = dossier.get_annotations()['test-field-1']
        annotation['stringValue'] = ''
        assert annotation_modifier.perform(annotation) == 0
        assert dossier.force_fetch().get_annotations()['test-field-1']['stringValue'] == ''
    @pytest.fixture
    def dossier(self) -> Dossier:
        dossier = demarche.get_dossiers()[0]
        instructeur_id = demarche.get_instructeurs_info()[0]['id']
        profile.set_instructeur_id(instructeur_id)
        return dossier
    @pytest.fixture
    def annotation_modifier(self, dossier : Dossier) -> AnnotationModifier:
        return AnnotationModifier(profile=profile, dossier=dossier)
    
    def test_annotation_modifier_with_no_error(self, dossier : Dossier, annotation_modifier : AnnotationModifier):
        self.reset_annotation(dossier, annotation_modifier)
        annotation = dossier.get_annotations()['test-field-1']
        annotation['stringValue'] = 'test'
        assert annotation_modifier.perform(annotation) == 0
        assert dossier.force_fetch().get_annotations()['test-field-1']['stringValue'] == 'test'
        self.reset_annotation(dossier, annotation_modifier)

class TestActionFileUploader():
    @pytest.fixture
    def dossier(self) -> Dossier:
        dossier = demarche.get_dossiers()[0]
        instructeur_id = demarche.get_instructeurs_info()[0]['id']
        profile.set_instructeur_id(instructeur_id)
        return dossier
    @pytest.fixture
    def file_uploader(self, dossier : Dossier) -> FileUploader:
        return FileUploader(profile=profile, dossier=dossier)

    def test_file_uploader_with_no_error(self, dossier : Dossier, file_uploader : FileUploader):
        assert file_uploader.perform('tests/test.txt', 'test.txt', 'text/plain') == FileUploader.SUCCESS
        last_file = file_uploader.get_files_uploaded()
        assert len(last_file) == 1
        last_file = file_uploader.get_last_file_uploaded()
        assert last_file['fileName'] == 'test.txt'
        assert last_file['contentType'] == 'text/plain'
        assert last_file['signedBlobId'] != ''


        
class TestActionMessageModifierError():
    @pytest.fixture
    def dossier(self) -> Dossier:
        profile.instructeur_id = None
        dossier = demarche.get_dossiers()[0]
        return dossier
    
    def test_create_sender_without_instructor_id(self, dossier : Dossier) -> MessageSender:
        with pytest.raises(DemarchesSimpyException):
            sender = MessageSender(profile=profile, dossier=dossier)


    
