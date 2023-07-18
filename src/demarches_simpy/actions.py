from .connection import RequestBuilder, Profile
from .utils import ILog, DemarchesSimpyException
from .dossier import DossierState, Dossier
from pathlib import Path
import os;
import hashlib
#######################
#       ACTIONS       #
# action -> dossier   #
# Pattern:            #
#   - action          #
#   - action          #
# Dossier won't
# implement any action
# on its own
#######################

# TODO: Add an interface action which implement a regular perform action method
# TODO: Annotation : implement general annotation modifier to modify any annotation checkbox, text, etc...

class MessageSender(ILog):
    def __init__(self, profile : Profile, dossier : Dossier, instructeur_id = None, **kwargs):
        ILog.__init__(self, header="MESSAGE_SENDER", profile=profile, **kwargs)

        if not profile.has_instructeur_id() and instructeur_id == None:
            self.error('No instructeur id was provided to the profile, cannot send message.')

        self.profile = profile
        self.dossier = dossier
        self.instructeur_id = profile.get_instructeur_id() if instructeur_id == None else instructeur_id

        # Create RequestBuilder
        try:
            self.request = RequestBuilder(self.profile, './query/send_message.graphql')
        except DemarchesSimpyException as e:
            self.error('Error during creating request : '+ e.message)


    def send(self, mess : str, attachement_id: str = None):
        variables = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
                "body" : mess,
                "attachment" : attachement_id
        }
        self.request.add_variable('input',variables)
        try:
            resp = self.request.send_request()
        except DemarchesSimpyException as e:
            self.warning('Message not sent : '+e.message)
            return False
        self.info('Message sent to '+self.dossier.get_id())
        return True
    
class AnnotationModifier(ILog):
    '''
        Class to modify anotation of a dossier

        Parameters
        ----------
        profile : Profile
            The profile to use to perform the action
        dossier : Dossier
            The dossier to modify
        instructeur_id : str
            The instructeur id to use to perform the action, if not provided, the profile instructeur id will be used

    '''
    def __init__(self, profile : Profile, dossier : Dossier, instructeur_id = None, **kwargs):
        super().__init__(header="ANOTATION MODIFIER", profile=profile, **kwargs)

        if not profile.has_instructeur_id() and instructeur_id == None:
            self.error('No instructeur id was provided to the profile, cannot modify anotation.')

        self.profile = profile
        self.dossier = dossier
        self.instructeur_id = profile.get_instructeur_id() if instructeur_id == None else instructeur_id

        # Create RequestBuilder
        try:
            self.request = RequestBuilder(self.profile, './query/actions.graphql')
        except DemarchesSimpyException as e:
            self.error('Error during creating request : '+ e.message)
        
        self.input = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
        }

    def set_annotation(self, anotation : dict[str, str], value : str = None):
        '''
            Set anotation to the dossier
            anotation : dict[str, str]
            {
                "id" : "123",
                "stringValue" : "foo"
            }

            Parameters
            ----------
            anotation : dict[str, str]
                Anotation to set

            Returns
            -------
            bool
                True if anotation was set, False otherwise
        '''
        #Check if anotation is valid
        if not 'id' in anotation or (not 'stringValue' in anotation and value == None):
            self.error('Invalid anotation provided : '+str(anotation))

        self.input['annotationId'] = anotation['id'] 
        self.input['value'] = anotation['stringValue'] if value == None else value


        self.request.add_variable('input',self.input)

        custom_body = {
            "query": self.request.get_query(),
            "operationName": "dossierModifierAnnotationText",
            "variables": self.request.get_variables()
        }

        try:
            resp = self.request.send_request(custom_body)
        except DemarchesSimpyException as e:
            self.warning('Anotation not set : '+e.message)
            return False
        self.info('Anotation set to '+self.dossier.get_id())
        return True


class FileUploader(ILog):
    def __init__(self, profile: Profile, dossier: Dossier, **kwargs):
        super().__init__(header="FILE UPLOADER", profile=profile, **kwargs)

        self.profile = profile
        self.dossier = dossier

        # Create RequestBuilder
        try:
            self.request = RequestBuilder(self.profile, './query/actions.graphql')
        except DemarchesSimpyException as e:
            self.error('Error during creating request : '+ e.message)

        self.input = {
            "dossierId": self.dossier.get_id(),
        }

    def upload_file(self, file_path: str, file_name: str, file_type: str="application/pdf"):
        self.input['filename'] = file_name
        self.input['contentType'] = file_type

        # path = Path(__file__).parent.absolute()
        # file_path = os.path.join(path, file_path)


        with open(file_path, 'rb') as f:
            self.input['byteSize'] = os.path.getsize(file_path)
            self.input['checksum'] = hashlib.md5(f.read()).hexdigest()
        
        self.request.add_variable('input', self.input)

        custom_body = {
            "query": self.request.get_query(),
            "operationName": "createDirectUpload",
            "variables": self.request.get_variables()
        }

        try:
            resp = self.request.send_request(custom_body,file={'file_path': file_path, 'file_type' : file_type})
        except DemarchesSimpyException as e:
            self.warning('File not uploaded : '+e.message)
            return False
        self.info('File uploaded to '+self.dossier.get_id())
        return resp.json()['data']['createDirectUpload']['directUpload']['signedBlobId']





class StateModifier(ILog):

    def __init__(self, profile : Profile, dossier : Dossier, instructeur_id=None, **kwargs):
        ILog.__init__(self, header="STATECHANGER", profile=profile, **kwargs)

        if not profile.has_instructeur_id() and instructeur_id == None:
            self.error('No instructeur id was provided to the profile, cannot change state.')
            

        self.profile = profile
        self.dossier = dossier
        self.instructeur_id = profile.get_instructeur_id() if instructeur_id == None else instructeur_id

        # Create RequestBuilder
        try:
            self.request = RequestBuilder(self.profile, './query/actions.graphql')
        except DemarchesSimpyException as e:
            self.error('Error during creating request : '+ e.message)
        self.input = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
        }


    def change_state(self, state,msg=""):

        if state == DossierState.ACCEPTER or state == DossierState.REFUSER or state == DossierState.SANS_SUITE:
            self.input['motivation'] = msg

        self.request.add_variable('input',self.input)
        operation_name = "dossier"
        operation_name += ("Passer" if state == DossierState.INSTRUCTION else "")
        operation_name += ("Repasser" if state == DossierState.CONSTRUCTION else "")
        operation_name += state


        custom_body = {
            "query" : self.request.get_query(),
            "operationName" : operation_name,
            "variables" : self.request.get_variables()
        }
        try:
            resp = self.request.send_request(custom_body)
        except DemarchesSimpyException as e:
            self.warning('State not changed : '+e.message)
            return False
        self.info('State changed to '+state+' for '+self.dossier.get_id())
        return True