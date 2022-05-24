from dataclasses import dataclass, asdict
from datetime import datetime



@dataclass
class Bill:
    BillID: int
    Name: str
    KnessetNum: int
    StatusID: int
    PrivateNumber: int
    LastUpdatedDate: datetime

    def __repr__(self):

        # Taken help from: https://stackoverflow.com/questions/11637293/iterate-over-object-attributes-in-python

        result = ''
        for attribute in [i for i in dir(self) if not i.startswith('__')]:
            result += f'{attribute}: {self.__getattribute__(attribute)}\n'
        return result

    def convert_to_dict(self):
        return asdict(self)