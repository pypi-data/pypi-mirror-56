from typing import Type, List, Mapping


class GlueColumn:
    def __init__(self, col_type: Type, proto_type: str):
        self.col_type: Type = col_type
        self.proto_type: str = proto_type

    def __str__(self):
        return self.proto_type

    def __repr__(self):
        return self.__str__()


class GlueColumnString(GlueColumn):
    def __init__(self):
        super().__init__(col_type=str, proto_type='string')


class GlueColumnBoolean(GlueColumn):
    def __init__(self):
        super().__init__(col_type=bool, proto_type='bool')


class GlueColumnStruct(GlueColumn):
    def __init__(self, content: Mapping[str, object], content_name: str):
        super().__init__(col_type=Mapping[str, object], proto_type='message')
        self.content = content
        self.content_name = ''.join([w.capitalize() for w in content_name.lower().split('_')])

    def __str__(self):
        return f'{self.content}'


class GlueColumnArray(GlueColumn):
    def __init__(self, content: [GlueColumn, GlueColumnStruct], content_name: str):
        super().__init__(col_type=List[type(content)], proto_type='repeated')
        self.content = content
        self.content_name = content_name

    def __str__(self):
        if type(self.content) == GlueColumnStruct:
            return f'{self.proto_type} {self.content.content_name}'
        else:
            return f'{self.proto_type} {self.content}'
