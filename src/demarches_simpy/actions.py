from .connection import RequestBuilder, Profile
from .utils import ILog, DemarchesSimpyException
from .dossier import DossierState, Dossier

#######################
#       ACTIONS       #
# action -> dossier   #
# Pattern:            #
#   - action          #
#   - action          #
# Dossier won't
# implement any action
# on its own
#######################

# TODO: Add an interface action which implement a regular perform action method

class MessageSender(ILog):
    def __init__(self, profile : Profile, dossier : Dossier, instructeur_id = None, **kwargs):
        ILog.__init__(self, header="MESSAGE_SENDER", profile=profile, **kwargs)

        if not profile.has_instructeur_id() and instructeur_id == None:
            self.error('No instructeur id was provided to the profile, cannot send message.')

        self.profile = profile
        self.dossier = dossier
        self.instructeur_id = profile.get_instructeur_id() if instructeur_id == None else instructeur_id

        # Create RequestBuilder
        try:
            self.request = RequestBuilder(self.profile, './query/send_message.graphql')
        except DemarchesSimpyException as e:
            self.error('Error during creating request : '+ e.message)


    def send(self, mess : str):
        variables = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
                "body" : mess
        }
        self.request.add_variable('input',variables)
        try:
            resp = self.request.send_request()
        except DemarchesSimpyException as e:
            self.warning('Message not sent : '+e.message)
            return False
        self.info('Message sent to '+self.dossier.get_id())
        return True
    


class StateChanger(ILog):

    def __init__(self, profile : Profile, dossier : Dossier, instructeur_id=None, **kwargs):
        ILog.__init__(self, header="STATECHANGER", profile=profile, **kwargs)

        if not profile.has_instructeur_id() and instructeur_id == None:
            self.error('No instructeur id was provided to the profile, cannot change state.')
            

        self.profile = profile
        self.dossier = dossier
        self.instructeur_id = profile.get_instructeur_id() if instructeur_id == None else instructeur_id

        # Create RequestBuilder
        try:
            self.request = RequestBuilder(self.profile, './query/actions.graphql')
        except DemarchesSimpyException as e:
            self.error('Error during creating request : '+ e.message)
        self.variables = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
        }


    def change_state(self, state,msg=""):

        if state == DossierState.ACCEPTER or state == DossierState.REFUSER or state == DossierState.SANS_SUITE:
            self.variables['motivation'] = msg

        self.request.add_variable('input',self.variables)
        operation_name = "dossier"
        operation_name += ("Passer" if state == DossierState.INSTRUCTION else "")
        operation_name += ("Repasser" if state == DossierState.CONSTRUCTION else "")
        operation_name += state


        custom_body = {
            "query" : self.request.get_query(),
            "operationName" : operation_name,
            "variables" : self.request.get_variables()
        }
        try:
            resp = self.request.send_request(custom_body)
        except DemarchesSimpyException as e:
            self.warning('State not changed : '+e.message)
            return False
        self.info('State changed to '+state+' for '+self.dossier.get_id())
        return True