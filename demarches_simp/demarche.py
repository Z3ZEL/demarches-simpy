from demarches_simp.data_interface import IData
from demarches_simp.connection import RequestBuilder
#TODO: Add multiple pages retrieval for dossiers
class Demarche(IData):
    from demarches_simp.connection import Profile
    def __init__(self, number : int, profile : Profile) :
        # Building the request
        request = RequestBuilder(profile, './demarches_simp/query/demarche.graphql')
        request.add_variable('demarcheNumber', number)
        
        # Call the parent constructor
        self.dossiers = []
        super().__init__(number, request, profile)
    def get_dossier_infos(self) -> list:
        ids = []
        for node in self.get_data()['demarche']['dossiers']['nodes']:
            ids.append((node['id'], node['number']))
        return ids
    def get_dossiers_count(self) -> int:
        return len(self.get_dossier_infos())
    
    def get_dossiers(self) -> list:
        if len(self.dossiers) == 0 or self.get_dossiers_count() != len(self.dossiers):
            from demarches_simp.dossier import Dossier
            dossiers = []
            for (id,number) in self.get_dossier_infos():
                dossiers.append(Dossier(number=number, id=id, profile=self.profile))
            self.dossiers = dossiers
        return self.dossiers

    #Champs retrieve
    def get_fields(self) -> list:
        if self.request.is_variable_set('includeRevision'):
            return self.force_fetch().get_data()['demarche']['activeRevision']['champDescriptors']
        else:
            self.request.add_variable('includeRevision', True)
            return self.force_fetch().get_data()['demarche']['activeRevision']['champDescriptors']    


    def __str__(self) -> str:
        return str("Id : "+self.get_data()['demarche']['id']) + ' Number : ' + str(self.get_data()['demarche']['number'])

