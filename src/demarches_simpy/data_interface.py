from .utils import bcolors
class IData():
    from .connection import Profile, RequestBuilder
    def __init__(self, number, request : RequestBuilder, profile : Profile) -> None:
        self.number = number
        self.profile = profile
        self.has_been_fetched = False
        self.data = None
        self.request = request
    def fetch(self) -> None:
        if not self.has_been_fetched:
            response = self.request.send_request()
            if response.status_code != 200:
                raise Exception('Could not fetch data.')
            #check if errors key is in response
            if 'errors' in response.json():
                raise Exception(bcolors.FAIL + 'Could not fetch data : ' + response.json()['errors'][0]['message'] + bcolors.ENDC)
                
            self.data = response.json()['data']
            self.has_been_fetched = True
    def get_data(self) -> dict:
        self.fetch()
        return self.data
    
    def force_fetch(self):
        self.has_been_fetched = False
        self.fetch()
        return self

    def get_id(self) -> str:
        return self.id