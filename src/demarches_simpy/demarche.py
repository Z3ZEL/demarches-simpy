from .data_interface import IData
from .connection import RequestBuilder
from .utils import ILog
#TODO: Add multiple pages retrieval for dossiers
#TODO: o<ptimisation for retrieving file
class Demarche(IData,ILog):
    '''
    This class represents a demarche in the demarches-simplifiees.fr API.
    It is used to retrieve and modify the data of a demarche.
    '''
    from .connection import Profile
    def __init__(self, number : int, profile : Profile, id : str = None,**kwargs) :
        # Building the request
        request = RequestBuilder(profile, './query/demarche.graphql')
        request.add_variable('demarcheNumber', number)
        
        # Call the parent constructor
        self.id = id
        self.number = number
        self.dossiers = []

        IData.__init__(self, request, profile)
        ILog.__init__(self, header="DEMARCHE", profile=profile, **kwargs)

        self.debug('Demarche class class created')

    def get_id(self) -> str:
        return self.id
    def get_number(self) -> int:
        return self.number
      
    def get_dossier_infos(self) -> list:
        ids = []
        for node in self.get_data()['demarche']['dossiers']['nodes']:
            ids.append((node['id'], node['number']))
        return ids
    def get_dossiers_count(self) -> int:
        return len(self.get_dossier_infos())
    
    def get_dossiers(self) -> list:
        if len(self.dossiers) == 0 or self.get_dossiers_count() != len(self.dossiers):
            from .dossier import Dossier
            dossiers = []
            for (id,number) in self.get_dossier_infos():
                dossiers.append(Dossier(number=number, id=id, profile=self.profile))
            self.dossiers = dossiers
        return self.dossiers

    #Champs retrieve
    def get_fields(self) -> list:
        if self.request.is_variable_set('includeRevision'):
            return self.get_data()['demarche']['activeRevision']['champDescriptors']
        else:
            self.request.add_variable('includeRevision', True)
            return self.force_fetch().get_data()['demarche']['activeRevision']['champDescriptors']    

    #TODO: Make a whole object for instructeurs
    def get_instructeurs_info(self):
        if not self.request.is_variable_set('includeInstructeurs'):
            self.request.add_variable('includeInstructeurs', True)
            self.request.add_variable('includeGroupeInstructeurs', True)
            groupes = self.force_fetch().get_data()['demarche']['groupeInstructeurs']
            instructeurs = []
            for groupe in groupes:
                for instructeur in groupe['instructeurs']:
                    instructeurs.append(instructeur)
            self.instructeurs = instructeurs
        return self.instructeurs


        ''''''

    def __str__(self) -> str:
        return str("Id : "+self.get_data()['demarche']['id']) + ' Number : ' + str(self.get_data()['demarche']['number'])

