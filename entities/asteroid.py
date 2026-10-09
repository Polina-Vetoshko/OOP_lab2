from core.game_object import GameObject
from core.config import AsteroidConfig
from core.protocols import Collidable


class Asteroid(GameObject):

    __slots__ = ("_x", "_y", "_config")

    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        config: AsteroidConfig | None = None,
    ) -> None:
        super().__init__(name)
        self._x = x
        self._y = y
        self._config = config or AsteroidConfig()

   
    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def collision_radius(self) -> float:
        return self._config.collision_radius

    @property
    def damage(self) -> int:
        return self._config.damage

 
    def collides_with(self, other: Collidable) -> bool:
        if not isinstance(other, Collidable):
            return False
        ox = getattr(other, "x", 0.0)
        oy = getattr(other, "y", 0.0)
        dist = ((self._x - ox) ** 2 + (self._y - oy) ** 2) ** 0.5
        return dist < self.collision_radius + other.collision_radius


    def update(self, dt: float) -> None:
        pass

    def draw(self) -> str:
        return f"☄️  {self._name} @ ({self._x:.0f},{self._y:.0f})"