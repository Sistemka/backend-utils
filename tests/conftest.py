from fastapi import APIRouter
import pytest
from pydantic import BaseModel

from backend_utils.http import BaseRequester
from backend_utils.server import Router


@pytest.fixture()
def router() -> Router:
    return Router(router=APIRouter(), prefix='/test', tags=['Test'])


class _Requester(BaseRequester):
    URL = 'https://hello.com'
    TIMEOUT = 10


@pytest.fixture()
def requester_class() -> type(_Requester):
    return _Requester


@pytest.fixture()
def requester() -> _Requester:
    return _Requester()


@pytest.fixture()
def response_json() -> dict:
    return {
        'id': 1,
        'title': 'hello'
    }


@pytest.fixture()
def response_model() -> type(BaseModel):
    class _ValidationModel(BaseModel):
        id: int  # noqa A003
        title: str
    return _ValidationModel


@pytest.fixture()
def response_model_invalid() -> type(BaseModel):
    class _ValidationModel(BaseModel):
        name: str
    return _ValidationModel
