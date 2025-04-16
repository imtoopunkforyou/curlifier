import json
from typing import NoReturn
from unittest import mock

import faker
import pytest
from requests.models import Response
from requests.structures import CaseInsensitiveDict


@pytest.fixture(scope='session')
def fake():
    return faker.Faker()


@pytest.fixture
def mock_response_target():
    return 'urllib3.connectionpool.HTTPConnectionPool.urlopen'


@pytest.fixture(autouse=True)
def ban_external_requests(monkeypatch, mock_response_target):
    """Ban on any external requests."""
    def _ban_external_requests(http_connection_pool, **_) -> NoReturn:
        msg = 'Attempting to make a request to `{host}` without a mock'
        raise RuntimeError(
            msg.format(
                host=http_connection_pool.host,
            )
        )

    monkeypatch.setattr(
        mock_response_target,
        _ban_external_requests,
    )


@pytest.fixture
def fake_url(fake):
    url = fake.url(schemes=['https', 'http'])
    path = fake.uri_path(deep=2)

    return url + path


@pytest.fixture
def fake_json_like_dict(fake):
    return json.loads(fake.json(num_rows=1))


@pytest.fixture
def fake_json(fake):
    return fake.json(num_rows=1)


@pytest.fixture
def fake_json_bytes(fake):
    return fake.json_bytes(num_rows=1)


@pytest.fixture
def http_status_ok():
    status_code = 200

    return status_code


@pytest.fixture
def fake_response_headers(fake):
    cid = CaseInsensitiveDict()
    cid['Date'] = fake.iso8601()
    cid['Server'] = 'uvicorn'
    cid['Content-Length'] = str(fake.pyint())
    cid['Content-Type'] = 'application/json'

    return cid


@pytest.fixture
def mock_response(
    fake_url,
    mock_response_target,
    fake_response_headers,
    fake_json_bytes,
    http_status_ok,
):
    response = Response()
    response.status_code = http_status_ok
    response._content = fake_json_bytes
    response.headers = fake_response_headers
    response.url = fake_url
    response.reason = 'OK'
    response.read = lambda *_: False

    return mock.patch(
        target=mock_response_target,
        return_value=response,
    )
