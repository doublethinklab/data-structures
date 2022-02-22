from abc import ABC
from collections.abc import MutableMapping
from datetime import datetime, date
import json
from typing import Any


def dict_equal_with_debug(a: Any, b: Any) -> bool:
    # this is really just for testing so far
    if isinstance(b, type(a)):
        if a.__dict__ != b.__dict__:
            for attr, value in a.__dict__.items():
                if a.__dict__[attr] != b.__dict__[attr]:
                    print('%s\t%s != %s' % (attr,
                                            a.__dict__[attr],
                                            b.__dict__[attr]))
        else:
            return True
    return False


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code.

    https://stackoverflow.com/questions/11875770/how-to-overcome-datetime-datetime-not-json-serializable
    """

    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    elif isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    elif isinstance(obj, DataBase):
        return obj.to_json()
    else:
        raise TypeError("Type %s not serializable" % type(obj))


class DataBase(MutableMapping, ABC):
    # https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))

    def __eq__(self, other):
        return dict_equal_with_debug(self, other)

    def __getitem__(self, key: str) -> Any:
        return self.store[key]

    def __setitem__(self, key: str, value: Any):
        self.store[key] = value

    def __delitem__(self, key: str) -> None:
        del self.store[key]

    def __iter__(self):
        return iter(self.store)

    def __len__(self) -> int:
        return len(self.store)

    def to_json(self) -> str:
        return json.dumps(self.store, default=json_serial)
