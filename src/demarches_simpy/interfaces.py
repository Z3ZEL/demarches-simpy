from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .connection import Profile
    from .dossier import Dossier
    from .connection import RequestBuilder



from .utils import bcolors, DemarchesSimpyException


class ILog():
    def __init__(self, header, profile, **kwargs):
        self.header = header

        # ----------------- VERBOSE -----------------
        # Low priority
        self.verbose = profile.get_verbose() if profile != None else False

        if 'verbose' in kwargs:
            self.verbose = kwargs['verbose']

        # High priority
        import sys
        #check if -v or --verbose is in the arguments
        if '-v' in sys.argv or '--verbose' in sys.argv:
            self.verbose = True


        # ----------------- WARNING DISPLAY -----------------
        
        self.displaying_warning = profile.__displaying_warning__() if profile != None else True

        if 'warning' in kwargs:
            self.displaying_warning = kwargs['warning']

        # High priority

        if '--no-warning' in sys.argv:
            self.displaying_warning = False



    def set_verbose(self, verbose):
        self.verbose = verbose
    def get_verbose(self):
        return self.verbose

    def __displaying_warning__(self):
        return self.displaying_warning


    def info(self, msg):
        msg = str(msg)
        print(f"{bcolors.OKGREEN}[{self.header}] {msg}{bcolors.ENDC}") 

    def error(self, msg):
        msg = str(msg)
        raise DemarchesSimpyException(header=self.header, message=msg)

    def warning(self, msg):
        if not self.displaying_warning:
            return
        msg = str(msg)
        print(f"{bcolors.WARNING}[{self.header}] {msg}{bcolors.ENDC}")

    def debug(self, msg):
        if not self.verbose:
            return
        msg = str(msg)
        print(f"{bcolors.OKBLUE}[{self.header}] {msg}{bcolors.ENDC}")

    def bold(self, msg):
        msg = str(msg)
        print(f"{bcolors.BOLD}[{self.header}] {msg}{bcolors.ENDC}") 

class IAction(ILog):
    SUCCESS = 0
    NETWORK_ERROR = 1
    REQUEST_ERROR = 2

    def __init__(self, profile : Profile, dossier : Dossier, **kwargs) -> None:
        r'''
            Internal function to create an action interface

            Parameters
            ----------
            **kwargs : dict, optional
                verbose parameter enable verbose
                query_path : str, optional
                    The path to the request graphql file (default : ./query/actions.graphql)
                instructeur_id : str, optional
                    The instructeur id to use to perform the action, if not provided, the profile instructeur id will be used
                no_instructeur_id : bool, optional
                    If set to True, the action will not be performed if no instructeur id is provided to the profile or to the action
                request_builder : RequestBuilder, optional
                    The request builder to use to perform the action, if not provided, a new one will be created using the query_path

        '''
        from .connection import RequestBuilder

        self.profile = profile
        self.dossier = dossier

        self.query_path = './query/actions.graphql'

        self.__instructeur_id = None

        if not 'no_instructeur_id' in kwargs:
            if 'instructeur_id' in kwargs:
                self.__instructeur_id = kwargs['instructeur_id']
        #Test instructeur id
        self.instructeur_id           


        if 'query_path' in kwargs:
            self.query_path = kwargs['query_path']


        self.debug(self.query_path)

        # Create RequestBuilder
        try:
            if 'request_builder' in kwargs:
                self.request = kwargs['request_builder']
            else:
                self.request = RequestBuilder(self.profile, self.query_path)
        except DemarchesSimpyException as e:
            self.error('Error during creating request : '+ e.message)
    
    @property
    def instructeur_id(self):
        if self.profile.has_instructeur_id():
            return self.profile.get_instructeur_id()
        elif self.__instructeur_id != None:
            return self.__instructeur_id
        else:
            self.error('No instructeur id was provided to the profile, cannot send message.')

    def perform(self) -> int:
        r'''
            Perform the action
            
            Returns
            -------
            0
                If the action was performed successfully
            1
                If the action failed
            
            Notes
            -----
            
            - This method should be overriden by the child class

            - More error code can be added by the child class
        '''
        pass

class IData(ILog):
    r'''
        Internal class to create a data interface
        All data object inherit from this class (Dossiern, Demarche for example)

        Parameters
        ----------
        **kwargs : dict, optional
            verbose parameter enable verbose
            background_fetching : bool, optional
                If set to True, the data will be fetched in background
            default_variables : dict, optional
                A dict of default variables to add to the request

    '''
    def __init__(self, request : RequestBuilder, profile : Profile, **kwargs) -> None:
        self._profile = profile
        self.has_been_fetched = False
        self.data = None
        self.request = request


        if 'default_variables' in kwargs and isinstance(kwargs['default_variables'], dict):
            for key, value in kwargs['default_variables'].items():
                self.request.add_variable(key, value)
            
        # Add background fetching
        if 'background_fetching' in kwargs and kwargs['background_fetching']:
            from threading import Thread
            Thread(target=self.fetch).start()


        self.__init_cache__()
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
        self.__init_cache__()
        self.fetch()
        return self

    def __init_cache__(self):
        pass
    def __init_persistent_cache__(self):
        pass

    @property
    def profile(self):
        return self._profile

    def get_id(self) -> str:
        pass
    def get_number(self) -> int:
        pass

