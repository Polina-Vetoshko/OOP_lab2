from typing import Protocol, runtime_checkable


@runtime_checkable
class Movable(Protocol):

    __slots__ = ()

    def move(self, dx: float, dy: float) -> None:
        ...


@runtime_checkable
class Drawable(Protocol):

    __slots__ = ()

    def draw(self) -> str:
        ...


@runtime_checkable
class Collidable(Protocol):

    __slots__ = ()

    @property
    def collision_radius(self) -> float:
        ...

    def collides_with(self, other: "Collidable") -> bool:
        ...
