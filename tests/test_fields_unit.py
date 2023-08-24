import pytest
import sys
sys.path.append('..')

from tests.fake_api import FakeRequestBuilder, FakeResponse

from src.demarches_simpy import Dossier, Profile, MapField, TextField
from src.demarches_simpy.utils import GeoArea, GeoSource
from src.demarches_simpy.connection import RequestBuilder

class TestUnitMapField():
    def CONTENT(request : RequestBuilder):
        return {
            "data":{
                "dossier":{
                    "champs":[
                        {
                            "__typename":"CarteChamp",
                            "id":"123",
                            "label":"foo",
                            "stringValue":"",
                            "rawAreas":[
                            {
                                "description":"ceci est une aire de surface",
                                "geometry":{
                                    "coordinates":[
                                        [
                                        [
                                            2.429863680245006,
                                            46.53848325962056
                                        ],
                                        [
                                            2.428963312124239,
                                            46.53777544505013
                                        ],
                                        [
                                            2.429936031253959,
                                            46.53711739041577
                                        ],
                                        [
                                            2.4325524506892577,
                                            46.53765219330455
                                        ],
                                        [
                                            2.4318289405916573,
                                            46.5381498775169
                                        ],
                                        [
                                            2.4305427004191245,
                                            46.53840977745929
                                        ],
                                        [
                                            2.430663285435429,
                                            46.53836000948158
                                        ],
                                        [
                                            2.4301970233737507,
                                            46.53845954539139
                                        ],
                                        [
                                            2.4301312108187005,
                                            46.53866989768392
                                        ],
                                        [
                                            2.429863680245006,
                                            46.53848325962056
                                        ]
                                        ]
                                    ],
                                    "type":"Polygon"
                                },
                                "id":"area_123",
                                "source":"selection_utilisateur"
                            }
                            ]
                        }
                    ]
                }
            }
            }

    @pytest.fixture
    def field(self):
        profile = Profile('')
        resp = FakeResponse(200, TestUnitMapField.CONTENT)
        request = FakeRequestBuilder(profile, resp)
        field = MapField('123', 'foo', '', 'CarteChamp', Dossier(123,profile,request=request),request=request)
        return field

    def test_field_geo_areas(self, field : MapField):
        assert len(field.geo_areas) == 1
        area = field.geo_areas[0]
        assert area.source == GeoSource.USER_SELECTION
        assert area.wkt_geometry == 'POLYGON ((2.429863680245006 46.53848325962056, 2.428963312124239 46.53777544505013, 2.429936031253959 46.53711739041577, 2.4325524506892577 46.53765219330455, 2.4318289405916573 46.5381498775169, 2.4305427004191245 46.53840977745929, 2.430663285435429 46.53836000948158, 2.4301970233737507 46.53845954539139, 2.4301312108187005 46.53866989768392, 2.429863680245006 46.53848325962056))'
        assert area.id == 'area_123'
        assert area.geojson_feature == {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                 "coordinates":[[
                                [
                                    2.429863680245006,
                                    46.53848325962056
                                ],
                                [
                                    2.428963312124239,
                                    46.53777544505013
                                ],
                                [
                                    2.429936031253959,
                                    46.53711739041577
                                ],
                                [
                                    2.4325524506892577,
                                    46.53765219330455
                                ],
                                [
                                    2.4318289405916573,
                                    46.5381498775169
                                ],
                                [
                                    2.4305427004191245,
                                    46.53840977745929
                                ],
                                [
                                    2.430663285435429,
                                    46.53836000948158
                                ],
                                [
                                    2.4301970233737507,
                                    46.53845954539139
                                ],
                                [
                                    2.4301312108187005,
                                    46.53866989768392
                                ],
                                [
                                    2.429863680245006,
                                    46.53848325962056
                                ]
                                ]]
                }
            }
        assert area.geometry_type == 'Polygon'
    def test_field(self, field : MapField):
        assert field.id == '123'
        assert field.label == 'foo'
        assert field.type == 'CarteChamp'

class TestUnitTextField():
    def CONTENT(request : RequestBuilder):
        return {
        "data":
            {
            "dossier":
                {
                    "champs":
                    [
                        {
                            "__typename":"TextChamp",
                            "id":"123",
                            "label":"foo",
                            "stringValue":"bar",
                            "value" : "bar"
                        }
                    ]
                }
            }
        }

    @pytest.fixture
    def field(self):
        profile = Profile('')
        resp = FakeResponse(200, TestUnitTextField.CONTENT)
        request = FakeRequestBuilder(profile, resp)
        field = TextField('123', 'foo', '', 'TextField', Dossier(123,profile,request=request),request=request)
        return field
    
    def test_field(self, field : TextField):
        assert field.id == '123'
        assert field.label == 'foo'
        assert field.type == 'TextField'
        assert field.value == 'bar'