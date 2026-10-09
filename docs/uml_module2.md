classDiagram
    class GameObject {
        <<abstract>>
        +id int
        +name str
        +active bool
        +update(dt) void
        +draw() str
    }
    class Movable {
        <<protocol>>
        +move(dx, dy) void
    }
    class Drawable {
        <<protocol>>
        +draw() str
    }
    class Collidable {
        <<protocol>>
        +collision_radius float
        +collides_with(other) bool
    }
    class LoggingMixin {
        +log(msg) void
        +log_warning(msg) void
        +log_error(msg) void
    }
    class MinerShip {
        +move(dx, dy)
        +mine(ore)
        +unload()
    }
    class Asteroid {
        +collides_with(other)
    }
    class Ore {
        +extract()
    }
    class Station {
        +sell_cargo(ship)
    }
    class Game

    GameObject <|-- MinerShip
    GameObject <|-- Asteroid
    GameObject <|-- Ore
    GameObject <|-- Station
    LoggingMixin <|-- MinerShip
    LoggingMixin <|-- Station
    MinerShip ..|> Movable
    MinerShip ..|> Drawable
    MinerShip ..|> Collidable
    Asteroid ..|> Drawable
    Asteroid ..|> Collidable
    Ore ..|> Drawable
    Ore ..|> Collidable
    Station ..|> Drawable
    Game *-- MinerShip
    Game *-- Station
    Game *-- Asteroid
    Game *-- Ore