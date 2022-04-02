from fastapi import APIRouter
import pytest

from backend_utils.server import Router


@pytest.fixture()
def router() -> Router:
    return Router(router=APIRouter(), prefix='/test', tags=['Test'])
