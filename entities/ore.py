from core.game_object import GameObject
from core.config import OreConfig
from core.protocols import Collidable


class Ore(GameObject):

    __slots__ = ("_x", "_y", "_config", "_extracted")

    def __init__(
        self,
        name: str,
        x: float,
        y: float,
        config: OreConfig | None = None,
    ) -> None:
        super().__init__(name)
        self._x = x
        self._y = y
        self._config = config or OreConfig()
        self._extracted = False

  
    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def value(self) -> int:
        return self._config.value

    @property
    def collision_radius(self) -> float:
        return self._config.collision_radius

    # --- добыча ---
    def extract(self) -> int:
        if self._extracted:
            return 0
        self._extracted = True
        self.deactivate()
        return self._config.value


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
        mark = "💎" if self._active else "·"
        return (
            f"{mark} {self._name} @ ({self._x:.0f},{self._y:.0f}) "
            f"value={self._config.value}"
        )