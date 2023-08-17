from .interfaces import IData, ILog
from .connection import Profile
from .demarche import Demarche
from .fields import FieldFactory, Field

from enum import Enum
class DossierState(Enum):
    '''
    This enum represents the state of a dossier in the demarches-simplifiees.fr API.

    Attributes
    ----------
        CONSTRUCTION
            The dossier is in construction
        ACCEPTE
            The dossier is accepted
        REFUSE
            The dossier is refused
        SANS_SUITE
            The dossier is classified without following
    '''
    # ARCHIVE = "Archiver"
    # CONSTRUCTION = "EnConstruction"
    # INSTRUCTION = "EnInstruction"
    # ACCEPTER = "Accepter"
    # REFUSER = "Refuser"
    # SANS_SUITE = "ClasserSansSuite"

    CONSTRUCTION = "en_construction"
    INSTRUCTION = "en_instruction"
    ACCEPTE = "accepte"
    REFUSE = "refuse"
    SANS_SUITE = "sans_suite"

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, DossierState):
            return self.value == __o.value
        elif isinstance(__o, str):
            return self.value == __o
        else:
            return super().__eq__(__o)

    def __str__(self) -> str:
        return self.value

    @staticmethod
    def from_str(str : str) -> 'DossierState':
        for state in DossierState:
            if state.value == str:
                return state
        raise ValueError("The string provided is not a valid DossierState")

    @staticmethod
    def __build_query_suffix__(state) -> str:
        if state == DossierState.CONSTRUCTION:
            return "EnConstruction"
        elif state == DossierState.INSTRUCTION:
            return "EnInstruction"
        elif state == DossierState.ACCEPTE:
            return "Accepter"
        elif state == DossierState.REFUSE:
            return "Refuser"
        elif state == DossierState.SANS_SUITE:
            return "ClasserSansSuite"
    # @staticmethod
    # def get_from_string(str):
    #     if str == 'en_construction':
    #         return DossierState.CONSTRUCTION
    #     elif str == 'en_instruction':
    #         return DossierState.INSTRUCTION
    #     elif str == 'accepter':
    #         return DossierState.ACCEPTER
    #     elif str == 'refuser':
    #         return DossierState.REFUSER
    #     elif str == 'sans_suite':
    #         return DossierState.SANS_SUITE



class Dossier(IData, ILog):
    r'''This class represents a dossier in the demarches-simplifiees.fr API.
    It is used to retrieve and modify the data of a dossier.

    - Log header : DOSSIER

    Properties
    ----------
        id : str
            the dossier id
        number : int
            the dossier number
        profile : Profile
            the dossier attached profile
        state : DossierState
            the dossier state


    Request Variables (for fetching)
    --------------------------------
        includeFields : bool
            if True, the dossier fields will be fetched
        includeAnnotations : bool
            if True, the dossier annotations will be fetched
        
    '''

    def __init__(self, number : int, profile : Profile, id : str = None, **kwargs):
        r'''
        Create manually a dossier

        Parameters
        ----------
        number : int
            the unique associated dossier number needed to identify and fetch the associated dossier.
        profile : Profile
            The connection profile
        id : str , optional
            the associated unique id

        **kwargs : dict, optional
            IData and ILog optional arguments (see IData and ILog documentation)
        
        Notes
        -----
        Currently fetching a dossier is possible only with its unique number, id fetching is not currently supported
        '''
        # Building the request
        from .connection import RequestBuilder
        if 'request' in kwargs:
            request = kwargs['request']
            del kwargs['request']
        else:
            request = RequestBuilder(profile, './query/dossier_data.graphql')
        
        request.add_variable('dossierNumber', number)

        # Add custom variables
        self._id = id
        self._number = number

        # Call the parent constructor
        IData.__init__(self, request, profile, **kwargs)
        ILog.__init__(self, header='DOSSIER', profile=profile, **kwargs)

        self.debug('Dossier class created')

        if not self._profile.has_instructeur_id():
            self.warning('No instructeur id was provided to the profile, some features will be missing.')
    def __init_cache__(self):
        self.fields = None
        self.instructeurs = None
        self.annotations = None

    @property
    def id(self):
        return self._id
    
    @property
    def number(self):
        return self._number

    @property
    def state(self):
        return self.get_dossier_state()

    def get_id(self) -> str:
        r'''
        Get the associated unique id of the dossier.

        Returns
        -------
            the unique id 
        '''
        if self.id is None:
            self._id = self.get_data()['dossier']['id']
        return self.id
    def get_number(self) -> int:
        r'''
            Get the associated unique dossier number.

            Returns
            -------
                the number of the dossier

        '''
        if self.number is None:
            return self.get_data()['dossier']['number']
        else:
            return self.number
    def get_deposit_date(self) -> str:
        r'''
            Get the deposit date of the dossier.

            Returns
            -------
                the deposit date of the dossier
        '''
        return self.get_data()['dossier']['dateDepot']

        
    def get_dossier_state(self) -> DossierState:
        r'''
        Get the dossier current state

        A state can be :

        - en_construction

        - en_instruction

        - accepte

        - refuse

        - sans_suite

        Returns
        -------
            The current dossier state
        '''
        return DossierState.from_str(self.get_data()['dossier']['state'])
    
    

    def get_attached_demarche_id(self) -> str:
        r'''
            Return the associated demarche unique id

            Returns
            -------
                the associated id string
            
        '''
        return self.get_data()['dossier']['demarche']['id']
    def get_attached_demarche(self) -> Demarche:
        r'''
            Get the associated demarche object

            Returns
            -------
                the associated demarche object

            Notes
            -----
                Take consider that a new Demarche object will be instantiated. For instance if you want to just get the id, prefer get_attached_demarche_id()
                
            See Also
            --------
                get_attached_demarche_id
        '''
        from .demarche import Demarche
        return Demarche(number=self.get_data()['dossier']['demarche']['number'], profile=self._profile)
    def get_attached_instructeurs_info(self):
        if self.instructeurs is None:
            if self.request.get_variables().get('includeInstructeurs') is None:
                self.request.add_variable('includeInstructeurs', True)
                self.force_fetch()
            self.instructeurs = self.get_data()['dossier']['instructeurs']
        return self.instructeurs
    def get_pdf_url(self) -> str:
        r'''Returns the url of the pdf of the dossier

        Returns
        -------
            The url of the pdf of the dossier
    
        '''
        return self.get_data()['dossier']['pdf']['url']
    #Champs retrieve TODO: revoir le typage
    def get_fields(self) -> list[Field]:
        r'''
        Returns the fields of the dossier as a dict 

        .. highlight:: python
        .. code-block:: python

            {
                'field_label' : 
                {
                    'stringValue':'foo',
                    'id':'foo'
                },
                ...
            }
            

        Returns
        -------
            a dict of fields value

        
        '''
        if self.fields is None:
            if self.request.get_variables().get('includeFields') is None:
                self.request.add_variable('includeFields', True)
                self.force_fetch()
            raw_fields = self.get_data()['dossier']['champs']
            fields = list(map(lambda x : {'label':x['label'],'stringValue' : x['stringValue'], "id":x['id'], 'type':x['__typename']}, raw_fields))
            self.fields = []
            factory = FieldFactory(self)
            for field in fields:
                self.fields.append(factory.create_field(field['id'], field['label'], field['stringValue'], field['type']))
        return self.fields

    #Annotations retrieve TODO: revoir type
    def get_annotations(self) -> list[dict[str, dict]]:
        r'''Returns the annotations of the dossier as a dict 
        
        .. highlight:: python
        .. code-block:: python

            {
                'annotation_label' :
                {
                    'stringValue' : 'foo',
                    'id' : 'foo'
                },
                ...
            }
        
        Returns
        -------
            Annotations dict

        
        '''
        if self.annotations is None:
            if self.request.get_variables().get('includeAnnotations') is None:
                self.request.add_variable('includeAnnotations', True)
                self.force_fetch()
            raw_annotations = self.get_data()['dossier']['annotations']
            annotations = dict(map(lambda x : (x['label'], {'stringValue' : x['stringValue'], "id":x['id']}), raw_annotations))
            self.annotations = annotations
        return self.annotations
    


    def __str__(self) -> str:
        return str("Dossier id : "+self.get_data()['dossier']['id']) + '\n' + "Dossier number " + str(self.get_data()['dossier']['number']) + "\n" + '(' + str(self.get_data()['dossier']['usager']['email']) + ')'



    


