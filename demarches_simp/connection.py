class Profile():
    '''
    This is tjhe profile class.
    '''
    def __init__(self, api_key : str) -> None:
        self.api_key = api_key
        print('Profile class created')


    ## GETTERS
    def get_api_key(self) -> str:
        return self.api_key
    
    def get_url(self) -> str:
        return 'https://www.demarches-simplifiees.fr/api/v2/graphql'



class RequestBuilder():
    '''
    This is the request builder class.
    '''
    from requests import Response 

    def __init__(self, profile : Profile, graph_ql_query_path : str) -> None:
        self.profile = profile
        self.variables = {}
        try:
            self.query = open(graph_ql_query_path, 'r').read()
        except:
            raise Exception('Could not open the GraphQL query file.')
        print('RequestBuilder class created from '+graph_ql_query_path)

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

    def add_variable(self, key : str, value : str) -> None:
        self.variables[key] = value
    
    def is_variable_set(self, key : str) -> bool:
        return key in self.variables

    def send_request(self) -> Response:
        import requests
        return requests.post(
            self.profile.get_url(),
            json = self.__get_body__(),
            headers = self.__get_header__()
        )
    

    