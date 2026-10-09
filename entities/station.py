from core.game_object import GameObject
from core.mixins import LoggingMixin
from core.config import GameConfig


class Station(LoggingMixin, GameObject):

    __slots__ = ("_x", "_y", "_credits", "_game_config")

    def __init__(
        self,
        name: str = "Станция",
        x: float = 0.0,
        y: float = 0.0,
        game_config: GameConfig | None = None,
    ) -> None:
        super().__init__(name)
        self._x = x
        self._y = y
        self._credits = 0
        self._game_config = game_config or GameConfig()
        self.log(f"Станция {name} открыта")


    @property
    def x(self) -> float:
        return self._x

    @property
    def y(self) -> float:
        return self._y

    @property
    def credits(self) -> int:
        return self._credits

  
    def sell_cargo(self, ship) -> int:
        amount = ship.unload()
        if amount == 0:
            self.log_warning("Попытка продать пустой трюм")
            return 0
        value = amount * self._game_config.ore_sell_price
        self._credits += value
        self.log(
            f"Принято {amount} ед., оплачено {value} кредитов "
            f"(всего {self._credits})"
        )
        return value


    def update(self, dt: float) -> None:
        pass

    def draw(self) -> str:
        return (
            f"🏠 {self._name} @ ({self._x:.0f},{self._y:.0f}) "
            f"credits={self._credits}"
        )