from __future__ import annotations
from typing import TYPE_CHECKING, Any
if TYPE_CHECKING:
    from .dossier import Dossier

from .interfaces import ILog, IData
from .utils import GeoSource, GeoArea
from .connection import RequestBuilder

class Field(IData, ILog):
    r'''
        Represent a field of a dossier, it's a generic class, you should use more specific class if you want to access to more specific properties

        Properties
        ----------
            id : str
                The id of the field
            label : str
                The label of the field
            stringValue : str
                The value of the field
            type : str
                The type of the field
            dossier : Dossier
                The dossier which the field is attached

    '''
    def __init__(self, id : str, label : str, stringValue : str, type : str, dossier : Dossier, **kwargs):
        self.request = RequestBuilder(dossier.profile, 'query/fields.graphql')
        self.request.add_variable('dossierNumber', dossier.get_number())
        self.request.add_variable('champId',id)
        IData.__init__(self,self.request, dossier.profile)
        ILog.__init__(self, "FIELD", dossier.profile,**kwargs)

        #Properties Read-Only
        self._id = id
        self._label = label
        self._stringValue = stringValue
        self._type = type
        self._dossier = dossier
        self._kwargs = kwargs

        self.reset_properties()

    @property
    def id(self) -> str:
        return self._id
    @property
    def label(self) -> str:
        return self._label
    @property
    def stringValue(self) -> str:
        return self._stringValue
    @property
    def dossier(self) -> Dossier:
        return self._dossier
    @property
    def type(self) -> str:
        return self._type
    
    def reset_properties(self):
        pass


    def __str__(self) -> str:
        return f'{self.label} : {self.stringValue}'


    def __set_fields__(self):
        self.fetch()
        data = self.get_data()['dossier']['champs'][0]
        for key in self.__get_keys__():
            if key in data:
                setattr(self, key, data[key])
                setattr(self, f'_{key}_type_hint', type(data[key]))
                setattr(self, f'_{key}_docstring', f'This is the {key} property.')

    def __getattribute__(self, __name: str) -> Any:
        try:
            return super().__getattribute__(__name)
        except AttributeError:
            self.__set_fields__()
            return super().__getattribute__(__name)
            
    @staticmethod
    def from_field(field : Field) -> Field:
        return Field(field.id, field.stringValue, field.type, **field.kwargs)
    @staticmethod
    def __get_keys__() -> list[str]:
        r'''
            Internal methods, providing a list of key value which the resquest need to find in the data fetched
        '''
        return []


class TextField(Field):
    r'''
        Represent a text field of a dossier (all properties of Field are available)

        Properties
        ----------
            value : str
                The value of the field (same as stringValue but with a different name and maybe it can hold a better encoding)

    '''
    value : str
    @staticmethod
    def __get_keys__() -> list[str]:
        return ['value']


    #Specific variable
    def __str__(self) -> str:
        return f'{self.label} : {self.value}'


class MapField(Field):
    r"""
    
    Properties
    ----------
        geoAreas : list[:doc:`GeoArea</refs/demarches_simpy.utils>`]
            The list of GeoArea of the field

    """
    def reset_properties(self):
        self._geo_areas = None

    @property
    def geo_areas(self) -> list[GeoArea]:
        if self._geo_areas == None:
            self._geo_areas = []
            for raw_areas in self.rawAreas:
                self._geo_areas.append(GeoArea(raw_areas['id'], raw_areas['source'], raw_areas['description'], raw_areas['geometry']))
        return self._geo_areas
    
    def geo_areas_to_geojson(self) -> dict:
        r'''
            The geojson representation of the geo_areas

            Returns
            -------
                The geojson representation of the geo_areas
        '''
        return {
            "type":"FeatureCollection",
            "features":[geo.geojson_feature for geo in self.geo_areas]
        }
    
    @staticmethod
    def __get_keys__() -> list[str]:
        return ['rawAreas']
    
    def __str__(self) -> str:
        return f"{self.label} : Contains {len(self.geo_areas)} GeoAreas"


class FieldFactory():
    def __init__(self, dossier : Dossier):
        self.dossier = dossier

    def create_field(self, id : str, label : str, stringValue : str, type : str, **kwargs) -> Field:
        if type == "TextChamp":
            return TextField(id, label, stringValue, type, self.dossier, **kwargs)
        elif type == "CarteChamp":
            return MapField(id, label, stringValue, type, self.dossier, **kwargs)
        else:
            return Field(id, label, stringValue, type, self.dossier, **kwargs)