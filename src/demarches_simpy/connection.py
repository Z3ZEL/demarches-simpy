from pathlib import Path
from .utils import ILog

class Profile(ILog):
    '''
    This is tjhe profile class.
    '''
    def __init__(self, api_key : str, instructeur_id : str = None, **kwargs) -> None:
        super().__init__(header='PROFILE', profile=None, **kwargs)
        self.api_key = api_key
        self.instructeur_id = instructeur_id

        self.debug('Profile class created')


    ## GETTERS
    def get_api_key(self) -> str:
        return self.api_key

    def get_instructeur_id(self) -> str:
        return self.instructeur_id
    
    def has_instructeur_id(self) -> bool:
        return self.instructeur_id != None
    
    def set_instructeur_id(self, instructeur_id : str) -> None:
        self.instructeur_id = instructeur_id
    
    def get_url(self) -> str:
        return 'https://www.demarches-simplifiees.fr/api/v2/graphql'




class RequestBuilder(ILog):
    '''
    This is the request builder class.
    '''
    from requests import Response 

    def __init__(self, profile : Profile, graph_ql_query_path : str, **kwargs) -> None:
        super().__init__(header='REQUEST BUILDER', profile=profile, **kwargs)
        self.profile = profile
        self.variables = {}
        try:
            path = Path(__file__).parent / graph_ql_query_path
            self.query = open(path, 'r').read()
        except:
            raise Exception('Could not open the GraphQL query file.')
        
        self.debug('RequestBuilder class created from '+graph_ql_query_path)

    def __get_body__(self) -> dict:
        return {
            "query": self.query,
            "variables": self.variables
        }

    def __get_header__(self) -> dict:
        return {
            "Content-Type": "application/json",
            "Authorization" : "Bearer token=" + self.profile.get_api_key()
        }
    
    def get_query(self) -> str:
        return self.query
    def get_variables(self) -> dict:
        return self.variables

    def add_variable(self, key : str, value : any) -> None:
        self.variables[key] = value
    
    def is_variable_set(self, key : str) -> bool:
        return key in self.variables

    def send_request(self, custom_body=None) -> Response:
        import requests
        return requests.post(
            self.profile.get_url(),
            json = self.__get_body__() if custom_body == None else custom_body,
            headers = self.__get_header__()
        )
    

    