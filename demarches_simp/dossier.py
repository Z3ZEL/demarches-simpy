from demarches_simp.data_interface import IData

class Dossier(IData):
    from demarches_simp.connection import Profile
    def __init__(self, number : int, profile : Profile, id : str = None) :

        # Building the request
        from demarches_simp.connection import RequestBuilder
        request = RequestBuilder(profile, './demarches_simp/query/dossier_data.graphql')
        request.add_variable('dossierNumber', number)

        # Add custom variables
        self.id = id
        self.fields = None
        self.anotations = None

        # Call the parent constructor
        super().__init__(number=number, request=request, profile=profile)

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

    def __str__(self) -> str:
        return str("Dossier id : "+self.get_data()['dossier']['id']) + '\n' + "Dossier number " + str(self.get_data()['dossier']['number']) + "\n" + ' (' + str(self.get_data()['dossier']['usager']['email']) + ')'



    


