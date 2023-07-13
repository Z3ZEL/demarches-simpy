from .utils import bcolors, ILog, DemarchesSimpyException
class IData(ILog):
    from .connection import Profile, RequestBuilder
    def __init__(self, request : RequestBuilder, profile : Profile, **kwargs) -> None:
        self.profile = profile
        self.has_been_fetched = False
        self.data = None
        self.request = request
    def fetch(self) -> None:
        if not self.has_been_fetched:
            response = self.request.send_request()
            if response.status_code != 200:
                self.error("Could not fetch data : "+str(response.status_code)+" "+response.reason)
            #check if errors key is in response
            if 'errors' in response.json():
                self.error("Could not fetch data : "+str(response.json()['errors']))
            self.data = response.json()['data']
            self.has_been_fetched = True
            self.debug('Data fetched')
    def get_data(self) -> dict:
        self.fetch()
        return self.data
    
    def force_fetch(self):
        self.has_been_fetched = False
        self.fetch()
        return self

    def get_id(self) -> str:
        pass
    def get_number(self) -> int:
        pass