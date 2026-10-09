class Ship:
    def __init__(self, name):
        self.name = name
        self.x = 0.0
        self.y = 0.0
        self.fuel = 100
        self.cargo = 0
        self.active = True

    def move(self, dx, dy):
        if not self.active:
            print(f"{self.name}: неактивен, не может двигаться")
            return
        if self.fuel < 1:
            print(f"{self.name}: нет топлива")
            return
        self.fuel -= 1
        self.x += dx
        self.y += dy
        print(
            f"{self.name}: -> ({self.x:.1f}, {self.y:.1f}), "
            f"топливо={self.fuel}"
        )

    def mine(self, ore):
        if self.cargo >= 10:
            print(f"{self.name}: трюм полон")
            return 0
        if self.fuel < 1:
            print(f"{self.name}: нет топлива для добычи")
            return 0
        self.fuel -= 1
        value = ore.extract()
        if value <= 0:
            print(f"{self.name}: руда {ore.name} уже выработана")
            return 0
        self.cargo += 1
        print(f"{self.name}: добыто {ore.name} (+{value}), груз={self.cargo}")
        return value

    def unload(self):
        amount = self.cargo
        self.cargo = 0
        if amount:
            print(f"{self.name}: разгружено {amount} ед.")
        return amount

    def take_damage(self, amount):
        self.fuel = max(0, self.fuel - amount)
        print(f"{self.name}: получен урон {amount}, топливо={self.fuel}")
        if self.fuel <= 0:
            print(f"{self.name}: обездвижен")
            self.active = False

    def collides_with(self, other):
        dist = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return dist < 1.5 + other.collision_radius

    @property
    def collision_radius(self):
        return 1.5

    def draw(self):
        return (f"🚀 {self.name} @ ({self.x:.0f},{self.y:.0f}) "
                f"fuel={self.fuel} cargo={self.cargo}")


class Asteroid:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.active = True
        self.collision_radius = 2.0
        self.damage = 10

    def collides_with(self, other):
        dist = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return dist < self.collision_radius + other.collision_radius

    def draw(self):
        return f"☄️  {self.name} @ ({self.x:.0f},{self.y:.0f})"


class Ore:
    def __init__(self, name, x, y, value=5):
        self.name = name
        self.x = x
        self.y = y
        self.value = value
        self.active = True
        self.collision_radius = 1.0
        self.extracted = False

    def extract(self):
        if self.extracted:
            return 0
        self.extracted = True
        self.active = False
        return self.value

    def collides_with(self, other):
        dist = ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5
        return dist < self.collision_radius + other.collision_radius

    def draw(self) -> str:
        mark = "💎" if self.active else "·"
        return (
            f"{mark} {self.name} @ ({self.x:.0f},{self.y:.0f}) "
            f"value={self.value}"
        )


class Station:
    def __init__(self, name="Станция", x=0.0, y=0.0):
        self.name = name
        self.x = x
        self.y = y
        self.active = True
        self.credits = 0

    def sell_cargo(self, ship):
        amount = ship.unload()
        if amount == 0:
            print(f"{self.name}: пустой трюм")
            return 0
        value = amount * 5
        self.credits += value
        print(f"{self.name}: принято {amount} ед., оплачено {value} "
              f"(всего {self.credits})")
        return value

    def draw(self):
        return (f"🏠 {self.name} @ ({self.x:.0f},{self.y:.0f}) "
                f"credits={self.credits}")


class Game:
    def __init__(self):
        self.ship = Ship("Скиталец")
        self.station = Station("Дом")
        self.asteroids = []
        self.ores = []
        self.max_turns = 20

    def setup(self):
        self.asteroids = [
            Asteroid("A-1", 5, 5),
            Asteroid("A-2", 10, 8),
        ]
        self.ores = [
            Ore("Железо", 3, 7, value=5),
            Ore("Золото", 12, 3, value=15),
            Ore("Платина", 7, 12, value=25),
        ]

    def run(self):
        self.setup()
        for turn in range(1, self.max_turns + 1):
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

    def _render(self):
        for obj in [self.ship, self.station, *self.asteroids, *self.ores]:
            print(" ", obj.draw())

    def _ship_ai(self):
        if self.ship.cargo >= 10:
            if self._step_towards(self.station):
                self.station.sell_cargo(self.ship)
            return
        target = self._nearest_ore()
        if target is None:
            return
        if self._step_towards(target):
            self.ship.mine(target)
        for ast in self.asteroids:
            if self.ship.collides_with(ast):
                self.ship.take_damage(ast.damage)

    def _nearest_ore(self):
        alive = [o for o in self.ores if o.active]
        if not alive:
            return None
        return min(
            alive,
            key=lambda o: (o.x - self.ship.x) ** 2 + (o.y - self.ship.y) ** 2,
        )

    def _step_towards(self, target):
        dx = target.x - self.ship.x
        dy = target.y - self.ship.y
        if abs(dx) < 0.5 and abs(dy) < 0.5:
            return True
        sx = max(-1.0, min(1.0, dx))
        sy = max(-1.0, min(1.0, dy))
        self.ship.move(sx, sy)
        return self.ship.collides_with(target)


def main():
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
