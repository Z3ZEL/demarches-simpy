from .data_interface import IData
from .utils import ILog
from .connection import Profile
from .demarche import Demarche
class DossierState:
    '''
    This class represents the state of a dossier in the demarches-simplifiees.fr API.
    '''
    ARCHIVE = "Archiver"
    CONSTRUCTION = "EnConstruction"
    INSTRUCTION = "EnInstruction"
    ACCEPTER = "Accepter"
    REFUSER = "Refuser"
    SANS_SUITE = "ClasserSansSuite"

    @staticmethod
    def get_from_string(str):
        if str == 'en_construction':
            return DossierState.CONSTRUCTION
        elif str == 'en_instruction':
            return DossierState.INSTRUCTION
        elif str == 'accepter':
            return DossierState.ACCEPTER
        elif str == 'refuser':
            return DossierState.REFUSER
        elif str == 'sans_suite':
            return DossierState.SANS_SUITE



class Dossier(IData, ILog):
    '''
    This class represents a dossier in the demarches-simplifiees.fr API.
    It is used to retrieve and modify the data of a dossier.

    Attributes
    ----------

    id : str
        The id of the dossier
    number : int
        The number of the dossier
    profile : Profile
        The profile used to connect to the API
    fields : dict
        The fields of the dossier as a dict of {field_id : field_value}
    anotations : dict
        The annotations of the dossier as a dict of {annotation_id : annotation_value}
    instructeurs : dict
        The instructeurs of the dossier as a dict of {instructeur_id : instructeur_value}

    
    '''

    def __init__(self, number : int, profile : Profile, id : str = None, **kwargs) :

        # Building the request
        from .connection import RequestBuilder
        request = RequestBuilder(profile, './query/dossier_data.graphql')
        request.add_variable('dossierNumber', number)

        # Add custom variables
        self.id = id
        self.fields = None
        self.instructeurs = None
        self.anotations = None
        self.profile = profile

        # Call the parent constructor
        IData.__init__(self,number, request, profile)
        ILog.__init__(self, header='DOSSIER', profile=profile, **kwargs)


        self.debug('Dossier class created')

        if not self.profile.has_instructeur_id():
            self.warning('No instructeur id was provided to the profile, some features will be missing.')


        

    def get_dossier_state(self) -> dict:
        return self.get_data()['dossier']['state']
    def get_attached_demarche_id(self) -> str:
        return self.get_data()['dossier']['demarche']['id']
    def get_attached_demarche(self) -> Demarche:
        from .demarche import Demarche
        return Demarche(number=self.get_data()['dossier']['demarche']['number'], profile=self.profile)
    def get_attached_instructeurs_info(self):
        if self.instructeurs is None:
            self.request.add_variable('includeInstructeurs', True)
            self.instructeurs = self.force_fetch().get_data()['dossier']['instructeurs']
        return self.instructeurs
    
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
     
    def __str__(self) -> str:
        return str("Dossier id : "+self.get_data()['dossier']['id']) + '\n' + "Dossier number " + str(self.get_data()['dossier']['number']) + "\n" + ' (' + str(self.get_data()['dossier']['usager']['email']) + ')'



    


