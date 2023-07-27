from __future__ import annotations

from .interfaces import IData, ILog
from .connection import RequestBuilder

from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from .connection import Profile
    from .dossier import Dossier

#TODO: Add multiple pages retrieval for dossiers
#TODO: o<ptimisation for retrieving file
class Demarche(IData,ILog):
    '''
    This class represents a demarche in the demarches-simplifiees.fr API.
    It is used to retrieve and modify the data of a demarche.

    - Log header : DEMARCHE
    '''
    def __init__(self, number : int, profile : Profile, id : str = None,**kwargs) :
        # Building the request
        request = RequestBuilder(profile, './query/demarche.graphql')
        request.add_variable('demarcheNumber', number)
        
        # Call the parent constructor
        self.id = id
        self.number = number
        self.dossiers = []
        self.fields = {}
        self.annotations = {}

        IData.__init__(self, request, profile)
        ILog.__init__(self, header="DEMARCHE", profile=profile, **kwargs)

        self.debug('Demarche class class created')

    def get_id(self) -> str:
        r'''
        Returns
        -------
            The unique id associated to the demarche
        '''
        if self.id is None:
            self.id = self.get_data()['demarche']['id']
        return self.id
    def get_number(self) -> int:
        r'''
        Returns
        -------
            THe unique number associated to the demarche
        '''
        return self.number
      
    def get_dossier_infos(self) -> list:
        r'''
            Get a list of minimum info about all dossiers, allows you to quickly retrieved all dossier without all their data

            Returns
            -------
                A list of tuple containing id and number of each dossier.

                .. highlight:: python
                .. code-block:: python
                    
                    [
                        ('uuid-1234-1234',1234567),
                        (...,...)
                    ]
                
        '''
        ids = []
        for node in self.get_data()['demarche']['dossiers']['nodes']:
            ids.append((node['id'], node['number']))
        return ids
    def get_dossiers_count(self) -> int:
        r'''
        Returns
        -------
            The total dossier count
        '''
        return len(self.get_dossier_infos())
    
    def get_dossiers(self) -> list[Dossier]:
        r'''
            Get all dossier objects

            Returns
            -------
                A list of all dossiers

            Notes
            -----
                A bit heavy, prefer using get_dossier_infos(). A pagination system is coming.
        '''
        if len(self.dossiers) == 0 or self.get_dossiers_count() != len(self.dossiers):
            from .dossier import Dossier
            dossiers = []
            for (id,number) in self.get_dossier_infos():
                dossiers.append(Dossier(number=number, id=id, profile=self.profile))
            self.dossiers = dossiers
        return self.dossiers

    #Champs retrieve
    def get_fields(self) -> dict[str,dict[str,str]]:
        r'''
            Get all fields of the demarche

            Returns
            -------
                A dict of all fields, with the label as key and the field as value

                .. highlight:: python
                .. code-block:: python

                    {
                        'a-field' : {
                            'label' : 'a-field',
                            '__typename' : 'type',
                            'description' : 'Le nom de la personne',
                            'id' : 'uuid-1234-1234',
                        },
                        ...
                    }
                            
        '''
        if len(self.fields) == 0:
            self.request.add_variable('includeRevision', True)
            raw = self.force_fetch().get_data()['demarche']['activeRevision']['champDescriptors']    
            self.fields = dict(map(lambda x : (x['label'],x),raw))
        return self.fields
    def get_annotations(self) -> dict[str,dict[str,str]]:
        r'''
            Get all annotation of the demarche

            Returns
            -------
                A dict of all annotations, with the label as key and the field as value

                .. highlight:: python
                .. code-block:: python

                    {
                        'an-annotation' : {
                            'label' : 'an-annotation',
                            '__typename' : 'type',
                            'description' : 'Le nom de la personne',
                            'id' : 'uuid-1234-1234',
                        },
                        ...
                    }
                            
        '''
        if len(self.annotations) == 0:
            self.request.add_variable('includeRevision', True)
            raw = self.force_fetch().get_data()['demarche']['activeRevision']['annotationDescriptors']    
            self.annotations = dict(map(lambda x : (x['label'],x),raw))
        return self.annotations
    #TODO: Make a whole object for instructeurs
    def get_instructeurs_info(self):
        if not self.request.is_variable_set('includeInstructeurs'):
            self.request.add_variable('includeInstructeurs', True)
            self.request.add_variable('includeGroupeInstructeurs', True)
            groupes = self.force_fetch().get_data()['demarche']['groupeInstructeurs']
            instructeurs = []
            for groupe in groupes:
                for instructeur in groupe['instructeurs']:
                    instructeurs.append(instructeur)
            self.instructeurs = instructeurs
        return self.instructeurs


        ''''''

    def __str__(self) -> str:
        return str(f"----- {self.get_data()['demarche']['title']} -----\n"+"Id : "+self.get_data()['demarche']['id']) + '\nNumber : ' + str(self.get_data()['demarche']['number'])+"\n"

