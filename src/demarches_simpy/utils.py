from __future__ import annotations
from enum import Enum
from shapely.geometry import shape
from shapely import Geometry

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class DemarchesSimpyException(Exception):
    def __init__(self,message="There was an error", header="MAIN",*args: object) -> None:
        super().__init__(message, *args)
        self.header = header
        self.message = message
    def __str__(self) -> str:
        return f"{bcolors.FAIL} [ERROR] [{self.header}] {super().__str__()}{bcolors.ENDC}"


class GeoSource(Enum):
    USER_SELECTION = 0,
    CADASTRE = 1

    @staticmethod
    def from_str(str: str) -> GeoSource:
        if str == 'selection_utilisateur':
            return GeoSource.USER_SELECTION
        elif str == 'cadastre':
            return GeoSource.CADASTRE
        else:
            raise DemarchesSimpyException("The string wasn't in the correct format", "GEO_SOURCE")
class GeoArea():
    def __init__(self, id : str, source: str, description : str, geometry : dict) -> None:
        self._id = id
        self._source = source
        self._description = description
        self._geometry = geometry
        self._shapely_geom = shape(geometry)

    @property
    def id(self) -> str:
        return self._id
    @property
    def source(self) -> str:
        return self._source
    @property
    def description(self) -> str:
        return self._description
    
    @property
    def wkt_geometry(self) -> str:
        return self._shapely_geom.wkt
    @property
    def geometry(self) -> Geometry:
        return self._shapely_geom
    @property
    def geometry_type(self) -> str:
        return self._shapely_geom.geom_type
    @property
    def geojson_feature(self) -> str:
        return {
            "type" : "Feature",
            "properties":{},
            "geometry":self._geometry
        }
    @property
    def geojson(self) -> str:
        return {
            "type": "FeatureCollection",
            "features":[
                self.geojson_feature
            ]
        }

    def __str__(self) -> str:
        return f"{self.description} : {self.geometry_type}"
    


       