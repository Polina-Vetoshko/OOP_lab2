from dataclasses import FrozenInstanceError

import pytest

from core.config import (
    AsteroidConfig,
    GameConfig,
    LocationConfig,
    OreConfig,
    ShipConfig,
)


def test_game_config_is_frozen():
    cfg = GameConfig()
    with pytest.raises(FrozenInstanceError):
        cfg.max_turns = 999


def test_ship_config_is_frozen():
    cfg = ShipConfig()
    with pytest.raises(FrozenInstanceError):
        cfg.max_fuel = 999


def test_asteroid_config_is_frozen():
    cfg = AsteroidConfig()
    with pytest.raises(FrozenInstanceError):
        cfg.damage = 999


def test_ore_config_is_frozen():
    cfg = OreConfig()
    with pytest.raises(FrozenInstanceError):
        cfg.value = 999


def test_game_config_defaults():
    cfg = GameConfig()
    assert cfg.max_turns == 20
    assert cfg.move_cost == 1
    assert cfg.mine_cost == 1
    assert cfg.ore_sell_price == 5


def test_ship_config_defaults():
    cfg = ShipConfig()
    assert cfg.max_fuel == 100
    assert cfg.max_cargo == 10
    assert cfg.collision_radius == 1.5


def test_asteroid_config_defaults():
    cfg = AsteroidConfig()
    assert cfg.collision_radius == 2.0
    assert cfg.damage == 10


def test_ore_config_defaults():
    cfg = OreConfig()
    assert cfg.value == 5
    assert cfg.collision_radius == 1.0


def test_game_config_equality():
    assert GameConfig() == GameConfig()
    assert GameConfig(max_turns=5) != GameConfig()
    assert GameConfig(max_turns=5) == GameConfig(max_turns=5)


def test_ship_config_equality():
    a = ShipConfig(max_fuel=50)
    b = ShipConfig(max_fuel=50)
    c = ShipConfig(max_fuel=100)
    assert a == b
    assert a != c


def test_frozen_config_is_hashable():
    cfg = GameConfig()
    assert hash(cfg) == hash(GameConfig())
    # можно использовать как ключ словаря
    d = {cfg: "value"}
    assert d[GameConfig()] == "value"


def test_location_config_lists_are_independent():
    a = LocationConfig()
    b = LocationConfig()
    a.ore_spawns.append("gold")
    a.asteroid_positions.append((1, 1))
    assert b.ore_spawns == []
    assert b.asteroid_positions == []


def test_location_config_three_instances_independent():
    a = LocationConfig()
    b = LocationConfig()
    c = LocationConfig()
    a.ore_spawns.append("x")
    b.ore_spawns.append("y")
    assert c.ore_spawns == []
    assert a.ore_spawns == ["x"]
    assert b.ore_spawns == ["y"]


def test_location_config_not_frozen():
    cfg = LocationConfig()
    cfg.name = "Сектор-7"
    assert cfg.name == "Сектор-7"


def test_location_config_defaults():
    cfg = LocationConfig()
    assert cfg.name == "Неизвестный сектор"
    assert cfg.width == 20
    assert cfg.height == 20
    assert cfg.asteroid_positions == []
    assert cfg.ore_spawns == []


def test_frozen_config_supports_replace():
    from dataclasses import replace

    easy = ShipConfig(max_fuel=200)
    hard = replace(easy, max_fuel=50)
    assert easy.max_fuel == 200
    assert hard.max_fuel == 50
