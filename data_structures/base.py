from collections.abc import MutableMapping
from typing import Any


class DataBase(MutableMapping):
    # https://stackoverflow.com/questions/3387691/how-to-perfectly-override-a-dict

    def __init__(self, *args, **kwargs):
        self.store = dict()
        self.update(dict(*args, **kwargs))

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
