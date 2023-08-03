from __future__ import annotations
from .interfaces import ILog

class Field(ILog):
    def __init__(self, id : str, stringValue : str, type : str, **kwargs):
        ILog.__init__(self, header="FIELD", **kwargs)
        self.id = id
        self.stringValue = stringValue
        self.type = type
        self.kwargs = kwargs

    @staticmethod
    def from_field(field : Field) -> Field:
        return Field(field.id, field.stringValue, field.type, **field.kwargs)


class TextField(Field):
    def __init__(self, id : str, stringValue : str, **kwargs):
        Field.__init__(self, id, stringValue, "TextChamp", **kwargs)
    
    @staticmethod
    def from_field(field : Field) -> TextField:
        return TextField(field.id, field.stringValue, **field.kwargs)






class FieldFactory():
    @staticmethod
    def create_field(field : Field) -> Field:
        if field.type == "TextChamp":
            return TextField.from_field(field)
        else:
            return Field.from_field(field)