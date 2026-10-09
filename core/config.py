from dataclasses import dataclass, field


@dataclass(frozen=True)
class GameConfig:

    max_turns: int = 20
    move_cost: int = 1
    mine_cost: int = 1
    collision_damage: int = 10
    ore_sell_price: int = 5
    arrival_threshold: float = 0.5
    ai_step: float = 1.0


@dataclass(frozen=True)
class ShipConfig:

    max_fuel: int = 100
    max_cargo: int = 10
    collision_radius: float = 1.5


@dataclass(frozen=True)
class AsteroidConfig:

    collision_radius: float = 2.0
    damage: int = 10


@dataclass(frozen=True)
class OreConfig:

    value: int = 5
    collision_radius: float = 1.0


@dataclass
class LocationConfig:

    name: str = "Неизвестный сектор"
    width: int = 20
    height: int = 20
    asteroid_positions: list = field(default_factory=list)
    ore_spawns: list = field(default_factory=list)
