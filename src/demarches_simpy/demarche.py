from __future__ import annotations

from .interfaces import IData, ILog
from .connection import RequestBuilder

from typing import TYPE_CHECKING, Callable


if TYPE_CHECKING:
    from .connection import Profile
    from .dossier import Dossier


class Demarche(IData,ILog):
    r'''
    This class represents a demarche in the demarches-simplifiees.fr API.
    It is used to retrieve and modify the data of a demarche.

    - Log header : DEMARCHE


    Request Variables (For fetching)
    --------------------------------
        - includeRevision -> For fields and annotations
        - includeInstructeurs -> For instructeurs info
    '''
    def __init__(self, number : int, profile : Profile, id : str = None,**kwargs) :
        # Building the request
        request = RequestBuilder(profile, './query/demarche.graphql')
        request.add_variable('demarcheNumber', number)
        
        # Call the parent constructor
        self._id = id
        self._number = number
      

        IData.__init__(self, request, profile, **kwargs)
        ILog.__init__(self, header="DEMARCHE", profile=profile, **kwargs)

        self.debug('Demarche class class created')

        
    def __init_cache__(self):
        self.dossiers = []
        self.fields = None
        self.annotations = None

    def __next_dossier_cursor__(self, background_fetching : bool = False, **dossier_kwargs) -> bool:
        from .dossier import Dossier
        for node in self.get_data()['demarche']['dossiers']['nodes']:
            self.dossiers.append(Dossier(node['number'], self._profile, node['id'], background_fetching=background_fetching, **dossier_kwargs))
        self.request.add_variable('cursor', self.get_data()['demarche']['dossiers']['pageInfo']['endCursor'])
        has_next = self.get_data()['demarche']['dossiers']['pageInfo']['hasNextPage']
        self.has_been_fetched = False # Not force_fetch otherwise it would erase the dossiers cache /!\
        return has_next
    



    @property
    def id(self) -> str:
        return self._id
    @property
    def number(self) -> int:
        return self._number

    def get_id(self) -> str:
        r'''
        Returns
        -------
            The unique id associated to the demarche
        '''
        if self.id is None:
            self._id = self.get_data()['demarche']['id']
        return self.id
    def get_number(self) -> int:
        r'''
        Returns
        -------
            THe unique number associated to the demarche
        '''
        return self.number
      
    def get_dossier_infos(self, limit=100) -> list[tuple[str,int]]:
        r'''
            Get a list of minimum info about all dossiers, allows you to quickly retrieved all dossier without all their data

            Parameters
            ----------
                limit : int, optional
                    The maximum number of dossiers to retrieve, -1 for no limit (default : 100)

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

        while self.__next_dossier_cursor__():
            if len(self.dossiers) > limit and limit != -1:
                return list(map(lambda d : (d.id, d.number), self.dossiers[:limit]))
            elif len(self.dossiers) == limit and limit != -1:
                return list(map(lambda d : (d.id, d.number), self.dossiers))
        return list(map(lambda d : (d.id, d.number), self.dossiers))
   
    def get_dossiers_count(self) -> int:
        r'''
        Returns
        -------
            The total dossier count
        '''
        return len(self.get_dossier_infos(limit=-1))
    
    def get_dossiers(self, limit : int = 100, dossier_filter : Callable[[Dossier],bool] = lambda _ : True, background_fetching : bool = False, **dossier_kwargs) -> list[Dossier]:
        r'''
            Get all dossier objects

            Parameters
            ----------
                limit : int, optional
                    The maximum number of dossiers to retrieve, -1 for no limit (default : 100)
                dossier_filter : Callable[[Dossier],bool], optional
                    A function that takes a dossier as parameter and return a boolean, if the function return True, the dossier will be added to the list, otherwise it will be ignored (default : lambda _ : True)
                background_fetching : bool, optional
                    If set to True, all fields of all dossiers will be fetched while fetching them, this will avoid synchronous fetching of each dossier (default : False) Use this if you want to filter dossiers by other fields than id and number
                dossier_kwargs : dict, optional
                    A dict of kwargs that will be passed to the dossier constructor (useful for passing default_variables for example)

            Returns
            -------
                A list of all dossiers

            Notes
            -----
                This method will fetch all dossiers, if you want to filter them, use the dossier_filter parameter, by default dossier object contains only number and id,
                if you want filter them by other fields, you need to set background_fetching to True, this will fetch all fields of all dossiers while fetching them avoiding
                synchronous fetching of each dossier.
        '''




        while self.__next_dossier_cursor__(background_fetching=background_fetching, **dossier_kwargs):
            filtered = list(filter(dossier_filter, self.dossiers))
            if len(filtered) > limit and limit != -1:
                return filtered[:limit]
            elif len(filtered) == limit and limit != -1:
                return filtered
        return list(filter(dossier_filter, self.dossiers))


            
        
        

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
        if self.fields == None:
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
        if self.annotations == None:
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

