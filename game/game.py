from core.config import (
    GameConfig,
    ShipConfig,
    AsteroidConfig,
    OreConfig,
)
from entities.ship import MinerShip
from entities.asteroid import Asteroid
from entities.ore import Ore
from entities.station import Station


class Game:

    def __init__(
        self,
        game_config: GameConfig | None = None,
        ship_config: ShipConfig | None = None,
        asteroid_config: AsteroidConfig | None = None,
    ) -> None:
        self.game_config = game_config or GameConfig()
        self.ship_config = ship_config or ShipConfig()
        self.asteroid_config = asteroid_config or AsteroidConfig()

    
        self.ship = MinerShip(
            "Скиталец",
            config=self.ship_config,
            game_config=self.game_config,
        )
        self.station = Station(
            "Дом",
            x=0.0,
            y=0.0,
            game_config=self.game_config,
        )
        self.asteroids: list[Asteroid] = []
        self.ores: list[Ore] = []

    def setup(self) -> None:
        self.asteroids = [
            Asteroid("A-1", 5.0, 5.0, self.asteroid_config),
            Asteroid("A-2", 10.0, 8.0, self.asteroid_config),
        ]
        self.ores = [
            Ore("Железо", 3.0, 7.0, OreConfig(value=5)),
            Ore("Золото", 12.0, 3.0, OreConfig(value=15)),
            Ore("Платина", 7.0, 12.0, OreConfig(value=25)),
        ]

    def run(self) -> int:
        self.setup()
        for turn in range(1, self.game_config.max_turns + 1):
            print(f"\n=== Ход {turn} ===")
            self._render()
            self._ship_ai()
            if not self.ship.active:
                print("Корабль обездвижен. Игра окончена.")
                break
            if all(not o.active for o in self.ores):
                print("Вся руда добыта. Победа!")
                break
        print(f"\nИтоговый счёт: {self.station.credits} кредитов")
        return self.station.credits

  
    def _render(self) -> None:
        for obj in [self.ship, self.station, *self.asteroids, *self.ores]:
            print(" ", obj.draw())

    def _ship_ai(self) -> None:
        # Полный трюм -> летим на станцию и продаём
        if self.ship.cargo >= self.ship_config.max_cargo:
            if self._step_towards(self.station):
                self.station.sell_cargo(self.ship)
            return
        # Иначе — к ближайшей руде
        target = self._nearest_ore()
        if target is None:
            return
        if self._step_towards(target):
            self.ship.mine(target)
        # Столкновения с астероидами
        for ast in self.asteroids:
            if self.ship.collides_with(ast):
                self.ship.take_damage(ast.damage)

    def _nearest_ore(self) -> Ore | None:
        alive = [o for o in self.ores if o.active]
        if not alive:
            return None
        return min(
            alive,
            key=lambda o: (o.x - self.ship.x) ** 2
            + (o.y - self.ship.y) ** 2,
        )

    def _step_towards(self, target) -> bool:
        dx = target.x - self.ship.x
        dy = target.y - self.ship.y
        threshold = self.game_config.arrival_threshold
        if abs(dx) < threshold and abs(dy) < threshold:
            return True
        step = self.game_config.ai_step
        sx = max(-step, min(step, dx))
        sy = max(-step, min(step, dy))
        self.ship.move(sx, sy)
        return self.ship.collides_with(target)