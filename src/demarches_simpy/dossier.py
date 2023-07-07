from .data_interface import IData
from .utils import ILog
from .actions import MessagerSender

class DossierState:
    ARCHIVE = "Archiver"
    INSTRUCTION = "EnInstruction"
    ACCEPTER = "Accepter"
    REFUSER = "Refuser"
    SANS_SUITE = "ClasserSansSuite"



class Dossier(IData, ILog):
    from .connection import Profile
    def __init__(self, number : int, profile : Profile, id : str = None, **kwargs) :

        # Building the request
        from .connection import RequestBuilder
        request = RequestBuilder(profile, './query/dossier_data.graphql', **kwargs)
        request.add_variable('dossierNumber', number)

        # Add custom variables
        self.id = id
        self.fields = None
        self.anotations = None
        self.profile = profile
        self.kwargs = kwargs

        # Call the parent constructor
        IData.__init__(self,number, request, profile)
        ILog.__init__(self, header='DOSSIER', **kwargs)


        self.debug('Dossier class created')

        if not self.profile.has_instructeur_id():
            self.warning('No instructeur id was provided to the profile, some features will be missing.')


        

    def get_dossier_state(self) -> dict:
        return self.get_data()['dossier']['state']

    
    #Champs retrieve
    def get_fields(self) -> dict:
        '''Returns the fields of the dossier as a dict of {field_id : field_value}'''
        if self.fields is None:
            self.request.add_variable('includeChamps', True)
            raw_fields = self.force_fetch().get_data()['dossier']['champs']
            fields = dict(map(lambda x : (x['label'], {'stringValue' : x['stringValue'], "id":x['id']}), raw_fields))
            self.fields = fields
        return fields

    #Annotations retrieve
    def get_anotations(self) -> list:
        '''Returns the annotations of the dossier as a list of {annotation_id : annotation_value}'''
        if self.anotations is None:
            self.request.add_variable('includeAnotations', True)
            raw_annotations = self.force_fetch().get_data()['dossier']['annotations']
            anotations = dict(map(lambda x : (x['label'], {'stringValue' : x['stringValue'], "id":x['id']}), raw_annotations))
            self.anotations = anotations
        return self.anotations

    def send_message(self, msg : str):
        if not self.profile.has_instructeur_id():
            self.error('No instructeur id was provided to the profile, cannot send message.')
            return
        sender = MessagerSender(self.profile, self.id, **self.kwargs)
        sender.send(msg)
     
    def __str__(self) -> str:
        return str("Dossier id : "+self.get_data()['dossier']['id']) + '\n' + "Dossier number " + str(self.get_data()['dossier']['number']) + "\n" + ' (' + str(self.get_data()['dossier']['usager']['email']) + ')'



    


