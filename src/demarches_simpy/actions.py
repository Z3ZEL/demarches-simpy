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
# TODO: Annotation : implement general annotation modifier to modify any annotation checkbox, text, etc...

class MessageSender(ILog):
    r'''
        Class to send message to a dossier
    '''
    def __init__(self, profile : Profile, dossier : Dossier, instructeur_id = None, **kwargs):
        r'''
            Parameters
            ----------
            profile : Profile
                The profile to use to perform the action
            dossier : Dossier
                The dossier to send message to
            instructeur_id : str, optional
                The instructeur id to use to perform the action, if not provided, the profile instructeur id will be used

        '''
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
        r'''
            Send a message to the dossier
            
            Parameters
            ----------
            mess : str
                The message to send

        '''
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
    
class AnnotationModifier(ILog):
    '''
        Class to modify anotation of a dossier

        Parameters
        ----------
        profile : Profile
            The profile to use to perform the action
        dossier : Dossier
            The dossier to modify
        instructeur_id : str
            The instructeur id to use to perform the action, if not provided, the profile instructeur id will be used

    '''
    def __init__(self, profile : Profile, dossier : Dossier, instructeur_id = None, **kwargs):
        r'''
            Parameters
            ----------
            profile : Profile
                The profile to use to perform the action
            dossier : Dossier
                The dossier to modify
            instructeur_id : str, optional
                The instructeur id to use to perform the action, if not provided, the profile instructeur id will be used
        '''
        super().__init__(header="ANOTATION MODIFIER", profile=profile, **kwargs)

        if not profile.has_instructeur_id() and instructeur_id == None:
            self.error('No instructeur id was provided to the profile, cannot modify anotation.')

        self.profile = profile
        self.dossier = dossier
        self.instructeur_id = profile.get_instructeur_id() if instructeur_id == None else instructeur_id

        # Create RequestBuilder
        try:
            self.request = RequestBuilder(self.profile, './query/actions.graphql')
        except DemarchesSimpyException as e:
            self.error('Error during creating request : '+ e.message)
        
        self.input = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
        }

    def set_annotation(self, anotation : dict[str, str], value : str = None) -> bool:
        r'''
            Set anotation to the dossier

            Parameters
            ----------
            anotation : dict[str, str]
                The anotation to set, must be a valid anotation structure:

                .. highlight:: python
                .. code-block:: python

                    {
                        "id" : "anotation_id",
                        "stringValue" : "anotation_value"
                    }

                If the anotation is not valid, the method will return False

            value : str
                The value to set to the anotation, if not provided, the anotation will be set to its default value

     

            Returns
            -------
            True 
                if anotation was set
            False
                otherwise
        '''
        #Check if anotation is valid
        if not 'id' in anotation or (not 'stringValue' in anotation and value == None):
            self.error('Invalid anotation provided : '+str(anotation))

        self.input['annotationId'] = anotation['id'] 
        self.input['value'] = anotation['stringValue'] if value == None else value


        self.request.add_variable('input',self.input)

        custom_body = {
            "query": self.request.get_query(),
            "operationName": "dossierModifierAnnotationText",
            "variables": self.request.get_variables()
        }

        try:
            resp = self.request.send_request(custom_body)
        except DemarchesSimpyException as e:
            self.warning('Anotation not set : '+e.message)
            return False
        self.info('Anotation set to '+self.dossier.get_id())
        return True




class StateModifier(ILog):
    r'''
        Class to change state of a dossier
    '''

    def __init__(self, profile : Profile, dossier : Dossier, instructeur_id=None, **kwargs):
        r'''
            Parameters
            ----------
            profile : Profile
                The profile to use to perform the action
            dossier : Dossier
                The dossier to change state
            instructeur_id : str, optional
                The instructeur id to use to perform the action, if not provided, the profile instructeur id will be used
        '''
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
        self.input = {
                "dossierId" : self.dossier.get_id(),
                "instructeurId" : self.instructeur_id,
        }


    def change_state(self, state: DossierState, msg=""):
        r'''
            Change the state of the dossier

            Parameters
            ----------
            state : DossierState
                The state to set to the dossier
            msg : str, optional
                The message to set to the dossier, if not provided, the message will be set to its default value : ""

        '''

        if state == DossierState.ACCEPTER or state == DossierState.REFUSER or state == DossierState.SANS_SUITE:
            self.input['motivation'] = msg

        self.request.add_variable('input',self.input)
        operation_name = "dossier"
        operation_name += ("Passer" if (state == DossierState.INSTRUCTION and self.dossier.get_dossier_state() == 'en_construction') else "")
        operation_name += ("Repasser" if (state == DossierState.INSTRUCTION and self.dossier.get_dossier_state() != 'en_construction') else "")
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
        if resp.json()['data'][operation_name]['errors'] != None:
            self.warning('State not changed : '+resp.json()['data'][operation_name]['errors'][0]['message'])
            return False
        self.info('State changed to '+state+' for '+self.dossier.get_id())
        return True