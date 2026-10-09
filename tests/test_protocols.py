from core.protocols import Collidable, Drawable, Movable


class Painter:

    def draw(self) -> str:
        return "p"


class Mover:

    def move(self, dx: float, dy: float) -> None:
        pass


class Blob:

    @property
    def collision_radius(self) -> float:
        return 1.0

    def collides_with(self, other) -> bool:
        return False


class AllRounder:

    @property
    def collision_radius(self) -> float:
        return 1.0

    def collides_with(self, other) -> bool:
        return False

    def move(self, dx: float, dy: float) -> None:
        pass

    def draw(self) -> str:
        return "all"



def test_drawable_true():
    assert isinstance(Painter(), Drawable)


def test_drawable_false():
    class NoDraw:
        pass

    assert not isinstance(NoDraw(), Drawable)


def test_drawable_duck_typing():

    class Stranger:
        def draw(self) -> str:
            return "hello"

    assert isinstance(Stranger(), Drawable)


def test_movable_true():
    assert isinstance(Mover(), Movable)


def test_movable_false():
    class NoMove:
        pass

    assert not isinstance(NoMove(), Movable)


def test_drawable_is_not_movable():
    assert not isinstance(Painter(), Movable)


def test_collidable_true():
    assert isinstance(Blob(), Collidable)


def test_collidable_false():
    class NoCollide:
        pass

    assert not isinstance(NoCollide(), Collidable)


def test_collidable_needs_both_members():

    class OnlyRadius:
        @property
        def collision_radius(self) -> float:
            return 1.0

    assert not isinstance(OnlyRadius(), Collidable)

    class OnlyMethod:
        def collides_with(self, other) -> bool:
            return False

    assert not isinstance(OnlyMethod(), Collidable)


def test_all_rounder_passes_all():
    obj = AllRounder()
    assert isinstance(obj, Movable)
    assert isinstance(obj, Drawable)
    assert isinstance(obj, Collidable)


def test_only_one_ability():
    assert not isinstance(Mover(), Drawable)
    assert not isinstance(Mover(), Collidable)
    assert not isinstance(Painter(), Movable)
    assert not isinstance(Painter(), Collidable)
    assert not isinstance(Blob(), Movable)
    assert not isinstance(Blob(), Drawable)


def test_int_is_not_drawable():
    assert not isinstance(42, Drawable)


def test_str_is_not_movable():
    assert not isinstance("hello", Movable)


def test_list_is_not_collidable():
    assert not isinstance([], Collidable)


def test_none_is_not_anything():
    assert not isinstance(None, Drawable)
    assert not isinstance(None, Movable)
    assert not isinstance(None, Collidable)
