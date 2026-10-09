import logging

from core.mixins import LoggingMixin


class Foo(LoggingMixin):

    pass


class Bar(LoggingMixin):

    def __init__(self, name: str) -> None:
        self.name = name


def test_log_does_not_crash():
    Foo().log("test")


def test_log_warning_does_not_crash():
    Foo().log_warning("warn")


def test_log_error_does_not_crash():
    Foo().log_error("err")


def test_log_uses_info_level(caplog):
    with caplog.at_level(logging.INFO):
        Foo().log("hello")
    assert any(
        r.levelno == logging.INFO and "hello" in r.getMessage()
        for r in caplog.records
    )


def test_log_warning_uses_warning_level(caplog):
    with caplog.at_level(logging.WARNING):
        Foo().log_warning("careful")
    assert any(
        r.levelno == logging.WARNING and "careful" in r.getMessage()
        for r in caplog.records
    )


def test_log_error_uses_error_level(caplog):
    with caplog.at_level(logging.ERROR):
        Foo().log_error("broken")
    assert any(
        r.levelno == logging.ERROR and "broken" in r.getMessage()
        for r in caplog.records
    )


def test_message_format(caplog):
    with caplog.at_level(logging.INFO):
        Foo().log("msg")
    text = caplog.records[-1].getMessage()
    assert text.startswith("[Foo] INFO: ")
    assert "msg" in text


def test_format_uses_class_name_not_base():

    class Sub(LoggingMixin):
        pass

    logger = Sub()._get_logger()
    assert logger.name == "Sub"


def test_slots_is_empty_tuple():
    assert LoggingMixin.__slots__ == ()


def test_mixin_has_no_dict():
    assert not hasattr(LoggingMixin, "__dict__") or \
        "log" in LoggingMixin.__dict__


def test_mixin_has_no_init():
    assert "__init__" not in LoggingMixin.__dict__


def test_mixin_works_with_init():
    b = Bar("test")
    assert b.name == "test"
    b.log("ok")


def test_handler_added_once():
    f = Foo()
    f.log("first")
    logger = logging.getLogger("Foo")
    count_after_first = len(logger.handlers)
    f.log("second")
    f.log("third")
    assert len(logger.handlers) == count_after_first


def test_no_duplicate_output(caplog):
    with caplog.at_level(logging.INFO):
        Foo().log("unique-message")
    matches = [
        r for r in caplog.records if "unique-message" in r.getMessage()
    ]
    assert len(matches) == 1


def test_each_class_has_own_logger():
    class A(LoggingMixin):
        pass

    class B(LoggingMixin):
        pass

    assert A()._get_logger().name == "A"
    assert B()._get_logger().name == "B"
    assert A()._get_logger().name != B()._get_logger().name
