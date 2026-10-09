from abc import ABC, abstractmethod


class GameObject(ABC):

    __slots__ = ("_id", "_name", "_active")

    _next_id: int = 0

    def __init__(self, name: str) -> None:
        GameObject._next_id += 1
        self._id: int = GameObject._next_id
        self._name: str = name
        self._active: bool = True

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @property
    def active(self) -> bool:
        return self._active

    def deactivate(self) -> None:
        self._active = False

    @abstractmethod
    def update(self, dt: float) -> None:
        ...

    @abstractmethod
    def draw(self) -> str:
        ...

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._id}, name={self._name!r})"
