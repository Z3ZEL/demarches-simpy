from demarches_simp.data_interface import IData

class Dossier(IData):
    from demarches_simp.connection import Profile
    def __init__(self, number : int, id : str, profile : Profile) :

        # Building the request
        from demarches_simp.connection import RequestBuilder
        request = RequestBuilder(profile, './demarches_simp/query/dossier_data.graphql')
        request.add_variable('dossierNumber', number)

        # Add custom variables
        self.id = id

        # Call the parent constructor
        super().__init__(number=number, request=request, profile=profile)

    def get_dossier_state(self) -> dict:
        return self.get_data()['dossier']['state']



    def __str__(self) -> str:
        return str("Démarche id : "+self.get_data()['dossier']['id']) + ' (' + str(self.get_data()['dossier']['usager']['email']) + ')'



    


