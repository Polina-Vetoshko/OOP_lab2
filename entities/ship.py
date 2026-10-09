from core.game_object import GameObject
from core.mixins import LoggingMixin
from core.config import ShipConfig, GameConfig
from core.protocols import Collidable


class MinerShip(LoggingMixin, GameObject):
    __slots__ = (
        "_x", "_y", "_fuel", "_cargo",
        "_config", "_game_config",
    )

    def __init__(
        self,
        name: str,
        config: ShipConfig | None = None,
        game_config: GameConfig | None = None,
    ) -> None:
        super().__init__(name)
        self._config = config or ShipConfig()
        self._game_config = game_config or GameConfig()
        self._x: float = 0.0
        self._y: float = 0.0
        self._fuel: int = self._config.max_fuel
        self._cargo: int = 0
        self.log(f"Создан корабль {name}")

    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def fuel(self) -> int:
        return self._fuel

    @property
    def cargo(self) -> int:
        return self._cargo

    @property
    def collision_radius(self) -> float:
        return self._config.collision_radius


    def move(self, dx: float, dy: float) -> None:
        if not self._active:
            self.log_warning("Неактивный корабль не может двигаться")
            return
        cost = self._game_config.move_cost
        if self._fuel < cost:
            self.log_error("Недостаточно топлива для перемещения")
            return
        self._fuel -= cost
        self._x += dx
        self._y += dy
        self.log(
            f"Перемещение -> ({self._x:.1f}, {self._y:.1f}), "
            f"топливо={self._fuel}"
        )


    def collides_with(self, other: Collidable) -> bool:
        if not isinstance(other, Collidable):
            return False
        ox = getattr(other, "x", 0.0)
        oy = getattr(other, "y", 0.0)
        dist = ((self._x - ox) ** 2 + (self._y - oy) ** 2) ** 0.5
        return dist < self.collision_radius + other.collision_radius


    def mine(self, ore) -> int:
        if self._cargo >= self._config.max_cargo:
            self.log_warning("Трюм полон")
            return 0
        cost = self._game_config.mine_cost
        if self._fuel < cost:
            self.log_error("Недостаточно топлива для добычи")
            return 0
        self._fuel -= cost
        value = ore.extract()
        if value <= 0:
            self.log_warning(f"Руда {ore.name} уже выработана")
            return 0
        self._cargo += 1
        self.log(f"Добыто: {ore.name} (+{value}), груз={self._cargo}")
        return value

    def unload(self) -> int:
        """Выгрузить весь груз. Возвращает выгруженное количество."""
        amount = self._cargo
        self._cargo = 0
        if amount:
            self.log(f"Разгружено {amount} единиц груза")
        return amount

    def take_damage(self, amount: int) -> None:
        """Получить урон — уменьшить топливо."""
        self._fuel = max(0, self._fuel - amount)
        self.log_warning(f"Получен урон {amount}, топливо={self._fuel}")
        if self._fuel <= 0:
            self.log_error("Корабль обездвижен")
            self.deactivate()


    def update(self, dt: float) -> None:
        if self._fuel <= 0:
            self.deactivate()

    def draw(self) -> str:
        return (
            f"🚀 {self._name} @ ({self._x:.0f},{self._y:.0f}) "
            f"fuel={self._fuel} cargo={self._cargo}"
        )