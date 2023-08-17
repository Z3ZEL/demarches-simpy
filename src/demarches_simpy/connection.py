from pathlib import Path
import requests
import json
from requests import Response 
from .interfaces import ILog

class Profile(ILog):
    r'''
    The profile class handling connection information and can allow you to pass configuration parameters and diffuse it to all object using this profile

    - Exemple : Passing the args verbose=True will activate the verbose to all object using this profile instance.
    '''
    def __init__(self, api_key : str, instructeur_id : str = None, **kwargs) -> None:
        super().__init__(header='PROFILE', profile=None, **kwargs)
        self.api_key = api_key
        self.instructeur_id = instructeur_id

        self.debug('Profile class created')


    ## GETTERS
    def get_api_key(self) -> str:
        r'''
        Returns
        -------
            The démarches simplifiées api key
        '''
        return self.api_key

    def get_instructeur_id(self) -> str:
        r'''
        Returns
        -------
        str 
            the unique id of the associated instructeur using this profile
        None
            if the instructeur id is not provided
        '''
        return self.instructeur_id
    
    def has_instructeur_id(self) -> bool:
        r'''
        Returns
        -------
        True
            if an instructeur id was provided
        False
            otherwise

        '''
        return self.instructeur_id != None
    
    def set_instructeur_id(self, instructeur_id : str) -> None:
        r'''
        Assign a unique instructeur id

        Parameters
        ----------
        instructeur_id : str
            the unique instructeur id
        
        '''
        self.instructeur_id = instructeur_id
    
    def get_url(self) -> str:
        return 'https://www.demarches-simplifiees.fr/api/v2/graphql'




class RequestBuilder(ILog):
    r'''
    Internal class handling request and fetching data from démarches simplifiées, you won't have to use (except for dev)
    '''

    def __init__(self, profile : Profile, graph_ql_query_path : str, **kwargs) -> None:
        super().__init__(header='REQUEST BUILDER', profile=profile, **kwargs)
        self.profile = profile
        self.variables = {}
        try:
            path = Path(__file__).parent / graph_ql_query_path
            self.query = open(path, 'r').read()
        except:
            self.error('Cannot open file '+graph_ql_query_path)
        
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

    def add_variable(self, key : str, value : any) -> 'RequestBuilder':
        self.variables[key] = value
        return self
    
    def is_variable_set(self, key : str) -> bool:
        return key in self.variables

    def send_request(self, custom_body=None) -> Response:
        resp = requests.post(
            self.profile.get_url(),
            json = self.__get_body__() if custom_body == None else custom_body,
            headers = self.__get_header__()
        )
        if 'errors' in resp.json() and resp.json()['errors'] != None: 
            self.error('Request not sent : '+resp.json()['errors'][0]['message'])
        else:
            return resp


class FileUploadRequestBuilder(RequestBuilder):

    def send_request(self, file_path, custom_body=None) -> Response:
        resp = super().send_request(custom_body)

        if 'errors' in resp.json() and resp.json()['errors'] != None:
            self.error('Message not sent : '+resp.json()['errors'][0]['message'])
        
        if resp.ok:
            self.debug('File upload request sent')
        else:
            self.error('File upload request not sent : '+str(resp.status_code)+'\n'+resp.text)

        #Upload file 
        info = resp.json()['data']['createDirectUpload']['directUpload']
        url = info['url']
        headers = json.loads(info['headers'])

        upload_resp = requests.put(url, data=open(file_path, 'rb'), headers=headers)


        if upload_resp.ok:
            self.debug('File uploaded')
        else:
            self.error("\nCode error : "+str(upload_resp.status_code)+"\n"+ upload_resp.text)

        return info['signedBlobId']
