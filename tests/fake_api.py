import sys
sys.path.append('..')
from src.demarches_simpy.connection import RequestBuilder, Profile
from requests import Response


class FakeRequestBuilder(RequestBuilder):
    '''
        Fake a request returning a response or error
    '''
    def __init__(self,profile, response):
        super().__init__(profile, "query/empty.graphql")
        self.response = response
        self.response.set_request(self)
    
    def send_request(self):
        return self.response

class FakeResponse(Response):
    '''
        Fake a response with status code and json
    '''
    def __init__(self, status_code, f_content, **kwargs):
        super().__init__()
        self.status_code = status_code
        self.f_content = f_content

        for key, value in kwargs.items():
            setattr(self, key, value)

    def set_request(self, request):
        self.request = request

    def json(self):
        return self.f_content(self.request)
    