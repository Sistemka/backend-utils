import httpx
import respx
import pytest

from backend_utils.http import RequestMethods


def _mock_request_200(requester, response_json):
    respx.get(requester.url + '/hello').mock(
        side_effect=lambda request: httpx.Response(json=response_json, status_code=200) # noqa U100
    )


def _mock_request_404(requester):
    respx.get(requester.url + '/hello').mock(
        side_effect=lambda request: httpx.Response(status_code=404) # noqa U100
    )


def _mock_request_timeout(requester):
    respx.get(requester.url + '/hello').mock(side_effect=httpx.ConnectTimeout)


def test_is_singleton(requester_class):
    r1 = requester_class()
    r2 = requester_class()
    assert id(r1) == id(r2)


def test_name(requester):
    assert requester.name == '_Requester'


@pytest.mark.asyncio
@respx.mock
async def test_make_request_with_uri(requester, response_json):
    _mock_request_200(requester, response_json)
    r = await requester.make_request(
        method=RequestMethods.GET,
        uri='hello'
    )
    assert r.status_code == 200
    assert r.json() == response_json


@pytest.mark.asyncio
@respx.mock
async def test_make_request_with_url(requester, response_json):
    _mock_request_200(requester, response_json)
    r = await requester.make_request(
        method=RequestMethods.GET,
        url=f'{requester.url}/hello'
    )
    assert r.status_code == 200
    assert r.json() == response_json


@pytest.mark.asyncio
@respx.mock
async def test_make_request_with_validation(requester, response_json, response_model):
    _mock_request_200(requester, response_json)
    r = await requester.make_request(
        method=RequestMethods.GET,
        url=f'{requester.url}/hello',
        response_model=response_model
    )
    assert r is not None
    assert r.id == response_json['id']
    assert r.title == response_json['title']


@pytest.mark.asyncio
@respx.mock
async def test_make_request_validation_error(requester, response_json, response_model_invalid):
    _mock_request_200(requester, response_json)
    r = await requester.make_request(
        method=RequestMethods.GET,
        url=f'{requester.url}/hello',
        response_model=response_model_invalid
    )
    assert r is None


@pytest.mark.asyncio
@respx.mock
async def test_make_request_timeout(requester):
    _mock_request_timeout(requester)
    r = await requester.make_request(
        method=RequestMethods.GET,
        url=f'{requester.url}/hello',
        timeout=0.01
    )
    assert r is None


@pytest.mark.asyncio
@respx.mock
async def test_make_request_not_found(requester):
    _mock_request_404(requester)
    r = await requester.make_request(
        method=RequestMethods.GET,
        url=f'{requester.url}/hello',
    )
    assert r is None
