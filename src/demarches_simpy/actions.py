import hashlib
import base64

from .connection import FileUploadRequestBuilder, Profile
from .utils import DemarchesSimpyException
from .dossier import DossierState, Dossier
from .interfaces import IAction, ILog

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

class MessageSender(IAction, ILog):
    r'''
        Class to send message to a dossier
    '''
    def __init__(self, profile : Profile, dossier : Dossier, instructeur_id = None, **kwargs):
        r'''
            Parameters
            ----------
            profile : Profile
                The profile to use to perform the action
            dossier : Dossier
                The dossier to send message to
            instructeur_id : str, optional
                The instructeur id to use to perform the action, if not provided, the profile instructeur id will be used

        '''
        ILog.__init__(self, header="MESSAGE_SENDER", profile=profile, **kwargs)
        IAction.__init__(self, profile, dossier, query_path='./query/send_message.graphql', instructeur_id=instructeur_id)

    def     perform(self, mess : str, file_uploaded : dict = None) -> bool:
        r'''
            Send a message to the dossier
            
            Parameters
            ----------
            mess : str
                The message to send
            
            file_uploaded : dict, optional
                The file to send with the message, if not provided, no file will be sent

                The file must be a valid file structure:

                .. highlight:: python
                .. code-block:: python

                    {
                        "signedBlobId" : "file_id",
                        "filename" : "file_name",
                        "contentType" : "file_content_type"
                    }

            Returns
            -------
            SUCCESS
                if message was sent
            ERROR
                otherwise

        '''
        variables = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
                "body" : mess,
                "attachment" : file_uploaded['signedBlobId'] if file_uploaded != None else None,
        }
        self.request.add_variable('input',variables)
        try:
            resp = self.request.send_request()
        except DemarchesSimpyException as e:
            self.warning('Message not sent : '+e.message)
            return IAction.NETWORK_ERROR
        if resp.json()['data']['dossierEnvoyerMessage']['errors'] != None:
            self.warning('Message not sent : '+str(resp.json()['data']['dossierEnvoyerMessage']['errors'][0]['message']))
            return IAction.REQUEST_ERROR
        self.info('Message sent to '+str(self.dossier.get_number()))
        return IAction.SUCCESS
    
class AnnotationModifier(IAction, ILog):
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
        r'''
            Parameters
            ----------
            profile : Profile
                The profile to use to perform the action
            dossier : Dossier
                The dossier to modify
            instructeur_id : str, optional
                The instructeur id to use to perform the action, if not provided, the profile instructeur id will be used
        '''
        ILog.__init__(self, header="ANOTATION MODIFIER", profile=profile, **kwargs)
        IAction.__init__(self, profile, dossier, instructeur_id=instructeur_id)

        self.input = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
        }

    def perform(self, anotation : dict[str, str], value : str = None) -> int:
        r'''
            Set annotation to the dossier

            Parameters
            ----------

            anotation : dict[str, str]
                The anotation to set, must be a valid anotation structure:

                .. highlight:: python
                .. code-block:: python

                    {
                        "id" : "anotation_id",
                        "stringValue" : "anotation_value"
                    }

                If the anotation is not valid, the method will return False

            value : str
                The value to set to the anotation, if not provided, the anotation will be set to its default value

     

            Returns
            -------
            True 
                if anotation was set
            False
                otherwise


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
            return IAction.NETWORK_ERROR
        if not resp.ok:
            self.warning('Anotation not set : '+resp.json()['errors'][0]['message'])
            return IAction.ERROR
        self.info('Anotation set to '+self.dossier.get_id())
        return IAction.SUCCESS

class FileUploader(IAction, ILog):
    r'''
    Class to upload file to a dossier

    Parameters
    ----------

        profile : Profile
            The profile to use to perform the action
        dossier : Dossier
            The dossier to upload file to

    '''
    
    def __init__(self, profile: Profile, dossier: Dossier, **kwargs):
        request_builder = FileUploadRequestBuilder(profile, './query/actions.graphql')
        ILog.__init__(self, header="FILE UPLOADER", profile=profile, **kwargs)
        IAction.__init__(self, profile, dossier, request_builder=request_builder)

        self.files = []

        self.input = {
            "dossierId": self.dossier.get_id(),
        }

    def get_files_uploaded(self) -> list:
        r'''
            Get the list of files uploaded

            Returns
            -------
            list
                The list of files uploaded, each file is a dict with a specific structure, see :func:`FileUploader.get_last_file_uploaded` for more details
        '''
        return self.files

    def get_last_file_uploaded(self) -> dict:
        r'''
            Get the last file uploaded

            Returns
            -------
            dict
                The last file uploaded, the file is a dict with the following structure:
                
                .. highlight:: python
                .. code-block:: python

                    {
                        "fileName" : "file_name",
                        "contentType" : "file_content_type",
                        "signedBlobId" : "file_signed_blob_id"
                    }

                If no file was uploaded, the method will return None
        '''
        if len(self.files) == 0:
            return None
        return self.files[-1]


    def __md5__(value):
        md5_hash = hashlib.md5(value.encode()).digest()
        base64_encoded = base64.b64encode(md5_hash).decode()
        return base64_encoded


    def perform(self, file_path: str, file_name: str, file_type: str="application/pdf") -> int:
        r'''
            Upload a file to the dossier

            Parameters
            ----------
            file_path : str
                The path to the file to upload
            file_name : str
                The name of the file to upload
            file_type : str, optional
                The type of the file to upload, if not provided, the file will be set to its default value : "application/pdf"

            Returns
            -------
            SUCCESS
                if file was uploaded
            ERROR
                otherwise

        '''
        import os;

        self.input['filename'] = file_name
        self.input['contentType'] = file_type

        with open(file_path, 'r') as f:
            self.input['byteSize'] = os.path.getsize(file_path)
            self.input['checksum'] = FileUploader.__md5__(f.read())
        
        self.request.add_variable('input', self.input)

        custom_body = {
            "query": self.request.get_query(),
            "operationName": "createDirectUpload",
            "variables": self.request.get_variables()
        }

        try:
            resp = self.request.send_request(file_path, custom_body=custom_body)
        except DemarchesSimpyException as e:
            self.warning('File not uploaded : '+e.message)
            return IAction.NETWORK_ERROR
        self.files.append({'signedBlobId' : resp, 'fileName' : file_name, 'contentType' : file_type})
        return IAction.SUCCESS





class StateModifier(IAction, ILog):
    r'''
        Class to change state of a dossier
    '''

    def __init__(self, profile : Profile, dossier : Dossier, instructeur_id=None, **kwargs):
        r'''
            Parameters
            ----------
            profile : Profile
                The profile to use to perform the action
            dossier : Dossier
                The dossier to change state
            instructeur_id : str, optional
                The instructeur id to use to perform the action, if not provided, the profile instructeur id will be used
        '''
        ILog.__init__(self, header="STATECHANGER", profile=profile, **kwargs)
        IAction.__init__(self, profile, dossier, instructeur_id=instructeur_id)

        if not profile.has_instructeur_id() and instructeur_id == None:
            self.error('No instructeur id was provided to the profile, cannot change state.')
        
        self.input = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
        }


    def perform(self, state: DossierState, msg="") -> int:
        r'''
            Change the state of the dossier

            Parameters
            ----------
            state : DossierState
                The state to set to the dossier
            msg : str, optional
                The message to set to the dossier, if not provided, the message will be set to its default value : ""

        '''

        if state == DossierState.ACCEPTE or state == DossierState.REFUSE or state == DossierState.SANS_SUITE:
            self.input['motivation'] = msg

        self.request.add_variable('input',self.input)
        operation_name = "dossier"
        operation_name += ("Passer" if (state == DossierState.INSTRUCTION and self.dossier.get_dossier_state() == 'en_construction') else "")
        operation_name += ("Repasser" if (state == DossierState.INSTRUCTION and self.dossier.get_dossier_state() != 'en_construction') else "")
        operation_name += ("Repasser" if state == DossierState.CONSTRUCTION else "")
        operation_name += DossierState.__build_query_suffix__(state)


        custom_body = {
            "query" : self.request.get_query(),
            "operationName" : operation_name,
            "variables" : self.request.get_variables()
        }
        try:
            resp = self.request.send_request(custom_body)
        except DemarchesSimpyException as e:
            self.warning('State not changed : '+e.message)
            return IAction.NETWORK_ERROR
        if resp.json()['data'][operation_name]['errors'] != None:
            self.warning('State not changed : '+resp.json()['data'][operation_name]['errors'][0]['message'])
            return IAction.REQUEST_ERROR
        self.info('State changed to '+str(state)+' for '+self.dossier.get_id())
        return IAction.SUCCESS