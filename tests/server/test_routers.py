import pytest
from fastapi import APIRouter, FastAPI

from backend_utils.server import Router, compile_routers, register_routers


def test_router_validation():
    with pytest.raises(ValueError):
        Router(router=APIRouter(), prefix='test', tags=['Test'])


def test_compile_routers(router):
    root_prefix = '/test_root'
    compiled_routers = compile_routers(routers=[router, router], root_prefix=root_prefix)

    for router in compiled_routers:
        assert router.prefix.startswith(root_prefix)


def test_compile_routers_no_root_prefix(router):
    compile_routers(routers=[router, router])


def test_compile_routers_validation(router):
    with pytest.raises(ValueError):
        compile_routers(routers=[router, router], root_prefix='test_root')


def test_register_routers(router):
    app = FastAPI()
    register_routers(app=app, routers=[router, router])
