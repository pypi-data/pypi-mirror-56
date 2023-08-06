from enum import IntEnum, auto


class QueryType(IntEnum):
    select = auto()
    update = auto()
    delete = auto()
    insert = auto()
    etc = auto()
