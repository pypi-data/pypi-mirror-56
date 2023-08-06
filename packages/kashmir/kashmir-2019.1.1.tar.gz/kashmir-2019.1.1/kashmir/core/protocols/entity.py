from typing import Union
from typing_extensions import Protocol


class Entity(Protocol):
    id: Union[int, str]
