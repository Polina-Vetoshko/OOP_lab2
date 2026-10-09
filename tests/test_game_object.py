import pytest

from core.game_object import GameObject


class Complete(GameObject):

    def update(self, dt: float) -> None:
        pass

    def draw(self) -> str:
        return "ok"


class Partial(GameObject):

    def update(self, dt: float) -> None:
        pass


def test_cannot_instantiate_abstract():
    with pytest.raises(TypeError):
        GameObject("x")


def test_subclass_must_implement_methods():
    with pytest.raises(TypeError):
        Partial("y")


def test_subclass_without_update_fails():
    class NoUpdate(GameObject):
        def draw(self) -> str:
            return "ok"

    with pytest.raises(TypeError):
        NoUpdate("z")


def test_subclass_without_draw_fails():
    class NoDraw(GameObject):
        def update(self, dt: float) -> None:
            pass

    with pytest.raises(TypeError):
        NoDraw("w")


def test_concrete_subclass_works():
    obj = Complete("alpha")
    assert obj.name == "alpha"
    assert obj.active is True
    assert obj.id > 0


def test_draw_returns_string():
    obj = Complete("alpha")
    assert obj.draw() == "ok"
    assert isinstance(obj.draw(), str)


def test_update_callable():
    obj = Complete("alpha")
    # update не должен падать
    obj.update(0.016)


def test_unique_ids():
    a = Complete("a")
    b = Complete("b")
    assert a.id != b.id


def test_ids_increase():
    a = Complete("a")
    b = Complete("b")
    assert b.id > a.id


def test_id_counter_shared_across_subclasses():

    class Other(GameObject):
        def update(self, dt: float) -> None:
            pass

        def draw(self) -> str:
            return "other"

    a = Complete("a")
    b = Other("b")
    c = Complete("c")
    assert len({a.id, b.id, c.id}) == 3


def test_deactivate():
    obj = Complete("z")
    assert obj.active is True
    obj.deactivate()
    assert obj.active is False


def test_deactivate_is_idempotent():
    obj = Complete("z")
    obj.deactivate()
    obj.deactivate()
    assert obj.active is False


def test_repr_contains_class_id_name():
    obj = Complete("hero")
    r = repr(obj)
    assert "Complete" in r
    assert "hero" in r
    assert str(obj.id) in r


def test_id_is_read_only():
    obj = Complete("x")
    with pytest.raises(AttributeError):
        obj.id = 999


def test_name_is_read_only():
    obj = Complete("x")
    with pytest.raises(AttributeError):
        obj.name = "other"


def test_active_is_read_only():
    obj = Complete("x")
    with pytest.raises(AttributeError):
        obj.active = False
