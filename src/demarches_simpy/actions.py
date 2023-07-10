from .connection import RequestBuilder
from .utils import ILog
import json

#TODO: Refacto to ift state changer
class MessagerSender(ILog):
    from .connection import Profile
    def __init__(self, profile : Profile, dossier_id : str, **kwargs):
        ILog.__init__(self, header="MESSAGER", profile=profile, **kwargs)
        self.profile = profile
        self.dossier_id = dossier_id
        self.instructeur_id = profile.get_instructeur_id()
        self.kwargs = kwargs

    def send(self, mess : str):
        self.request = RequestBuilder(self.profile, './query/send_message.graphql')
        variables = {
                "dossierId" : self.dossier_id,
                "instructeurId" : self.instructeur_id,
                "body" : mess
        }
        self.request.add_variable('input',variables)
        resp = self.request.send_request()
        self.debug('Message sent to dossier '+self.dossier_id)
        if 'errors' in resp.json() and resp.json()['errors'] != None:
            self.error('Message not sent : '+resp.json()['errors'][0]['message'])
        return resp
    


class StateChanger(ILog):
    from .connection import Profile

    def __init__(self, profile : Profile, dossier, **kwargs):
        ILog.__init__(self, header="STATECHANGER", profile=profile, **kwargs)

        if not profile.has_instructeur_id():
            self.error('No instructeur id was provided to the profile, cannot change state.')
            return

        self.profile = profile
        self.dossier = dossier
        self.instructeur_id = profile.get_instructeur_id()
        self.kwargs = kwargs

    def change_state(self, state):
        from .dossier import DossierState


        self.request = RequestBuilder(self.profile, './query/actions.graphql')
        variables = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
        }
        if state == DossierState.ACCEPTER or state == DossierState.REFUSER or state == DossierState.SANS_SUITE:
            variables['motivation'] = "Test"

        self.request.add_variable('input',variables)
        operation_name = "dossier"
        operation_name += ("Passer" if state == DossierState.INSTRUCTION else "")
        operation_name += ("Repasser" if state == DossierState.CONSTRUCTION else "")
        operation_name += state


        custom_body = {
            "query" : self.request.get_query(),
            "operationName" : operation_name,
            "variables" : self.request.get_variables()
        }

        resp = self.request.send_request(custom_body)
        if 'errors' in resp.json() and resp.json()['errors'] != None:
            self.error('State not changed : '+resp.json()['errors'][0]['message'])
        else:
            self.info('State changed to '+state+' for dossier '+self.dossier.get_id())
        return True