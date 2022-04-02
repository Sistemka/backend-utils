from enum import auto

from backend_utils.tools import StrEnum


def test_str_enum():
    class A(StrEnum):
        a = auto()

    a = A.a
    assert a.value == 'a'
