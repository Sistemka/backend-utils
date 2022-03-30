from backend_utils.tools import Singleton


def test_singleton():
    class A(metaclass=Singleton):
        def __init__(self, a):
            self.a = a

    a1 = A(a=1)
    a2 = A(a=2)

    # test if a1 and a2 are the same objects
    assert id(a1) == id(a2)
    assert a1.a == a2.a
    assert a2.a == 1
