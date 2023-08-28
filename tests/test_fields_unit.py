import pytest
import sys
sys.path.append('..')

from tests.fake_api import FakeRequestBuilder, FakeResponse

from src.demarches_simpy import Dossier, Profile, MapField, TextField, DateField, AttachedFileField, MultipleDropDownField
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

class TestUnitDateField():
    def CONTENT(request : RequestBuilder):
        return {
        "data":
            {
            "dossier":
                {
                    "champs":
                    [
                        {
                            "__typename":"DateChamp",
                            "id":"123",
                            "label":"foo",
                            "stringValue":"10 août 2020",
                            "date" : "2020-08-10"
                        }
                    ]
                }
            }
        }
    
    @pytest.fixture
    def field(self):
        profile = Profile('')
        resp = FakeResponse(200, TestUnitDateField.CONTENT)
        request = FakeRequestBuilder(profile, resp)
        field = DateField('123', 'foo', '', 'DateField', Dossier(123,profile,request=request),request=request)
        return field

    def test_field(self, field : DateField):
        assert field.id == '123'
        assert field.label == 'foo'
        assert field.type == 'DateField'
        assert field.date == '2020-08-10'
        assert field.timestamp == 1597010400

class TestUnitAttachedFileField():
    def CONTENT(request : RequestBuilder):
        return {
        "data":
            {
            "dossier":
                {
                    "champs":
                    [
                        {
                            "__typename":"PieceJustificativeChamp",
                            "id":"123",
                            "label":"foo",
                            "stringValue":"",
                            "files" : [
                                {
                                    "byteSizeBigInt" : 6000,
                                    "contentType" : "application/pdf",
                                    "filename" : "foo.pdf",
                                    "url" : "https://foo.bar"
                                },
                                {
                                    "byteSizeBigInt" : 6000,
                                    "contentType" : "application/pdf",
                                    "filename" : "foo.pdf",
                                    "url" : "https://foo.bar/2"
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
        resp = FakeResponse(200, TestUnitAttachedFileField.CONTENT)
        request = FakeRequestBuilder(profile, resp)
        field = AttachedFileField('123', 'foo', '', 'PieceJustificativeChamp', Dossier(123,profile,request=request),request=request)
        return field
    
    def test_field(self, field : AttachedFileField):
        assert field.id == '123'
        assert field.label == 'foo'
        assert field.type == 'PieceJustificativeChamp'

        assert len(field.files.keys()) == 2
        urls = list(field.files.keys())
        url = urls[0]
        assert field.files[url]["filename"] == 'foo.pdf'
        assert field.files[url]["url"] == 'https://foo.bar'
        assert field.files[url]["type"] == 'application/pdf'
        assert field.files[url]["size"] == 6000


class TestUnitMultipleDropDownField():
    def CONTENT(request : RequestBuilder):
        return {
        "data":
            {
            "dossier":
                {
                    "champs":
                    [
                        {
                            "__typename":"MultipleDropDownListChamp",
                            "id":"123",
                            "label":"foo",
                            "stringValue":"foo, bar",
                            "values" : [
                                "foo",
                                "bar"
                            ]
                        }
                    ]
                }
            }
        }

    @pytest.fixture
    def field(self):
        profile = Profile('')
        resp = FakeResponse(200, TestUnitMultipleDropDownField.CONTENT)
        request = FakeRequestBuilder(profile, resp)
        field = MultipleDropDownField('123', 'foo', '', 'MultipleDropDownListChamp', Dossier(123,profile,request=request),request=request)
        return field

    def test_field(self, field : MultipleDropDownField):
        assert field.id == '123'
        assert field.label == 'foo'
        assert field.type == 'MultipleDropDownListChamp'
        assert isinstance(field.values, list)
        assert len(field.values) == 2
        assert field.values[0] == 'foo'
        assert field.values[1] == 'bar'

