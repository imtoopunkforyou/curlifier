import json
import sys
from importlib import metadata
from pathlib import Path
from typing import NoReturn
from unittest import mock

import faker
import pytest
from requests.models import Response
from requests.structures import CaseInsensitiveDict
from urllib3.util.retry import Retry
from urllib3.util.timeout import Timeout


@pytest.fixture
def version_of_requests() -> str:
    return metadata.version('requests')


@pytest.fixture
def python_version_major() -> int:
    return sys.version_info.major


@pytest.fixture
def python_version_minor() -> int:
    return sys.version_info.minor


@pytest.fixture(scope='session')
def fake():
    return faker.Faker()


@pytest.fixture
def mock_response_target():
    return 'urllib3.connectionpool.HTTPConnectionPool.urlopen'


@pytest.fixture(autouse=True)
def ban_external_requests(monkeypatch, mock_response_target):
    """Ban on any external requests."""

    def _ban_external_requests(
        http_connection_pool,
        **_: str | bytes | CaseInsensitiveDict | Retry | Timeout,
    ) -> NoReturn:
        msg = 'Attempting to make a request to `{host}` without a mock'
        raise RuntimeError(
            msg.format(
                host=http_connection_pool.host,
            ),
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
    return 200


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


@pytest.fixture
def file_path_builder():
    def _file_path_builder(file_name):
        files_dir = Path('tests/files/')
        return files_dir / file_name

    return _file_path_builder


@pytest.fixture
def files(file_path_builder):
    pic = file_path_builder('f.jpg')
    voice = file_path_builder('f.mp3')
    text = file_path_builder('f.txt')

    return {
        'field_for_pic': Path.open(pic, 'rb'),
        'field_for_voice': Path.open(voice, 'rb'),
        'field_for_text': Path.open(text),
    }


@pytest.fixture
def fake_xml():
    return (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<root xmlns="http://defaultns.com/" xmlns:a="http://a.com/'
        'xmlns:b="http://b.com/"><x a:attr="val">1</x><a:y>2</a:y><b:z>3</b:z></root>'
    )


@pytest.fixture
def encoding_header(python_version_major, python_version_minor) -> str:
    if (python_version_major, python_version_minor) >= (3, 14):
        return 'gzip, deflate, zstd'

    return 'gzip, deflate'


@pytest.fixture
def curlify_hp_curl(version_of_requests, encoding_header):
    def _curlify_hp_curl(shorted, url, json):
        long = (
            'curl '
            "--request POST '{url}' "
            "--header 'User-Agent: python-requests/{version}' "
            "--header 'Accept-Encoding: {encoding_header}' "
            "--header 'Accept: */*' "
            "--header 'Connection: keep-alive' "
            "--header 'Content-Type: application/json' "
            "--data '{json}' "
            '--location'
        )
        short = (
            'curl '
            "-X POST '{url}' "
            "-H 'User-Agent: python-requests/{version}' "
            "-H 'Accept-Encoding: {encoding_header}' "
            "-H 'Accept: */*' "
            "-H 'Connection: keep-alive' "
            "-H 'Content-Type: application/json' "
            "-d '{json}' "
            '-L'
        )
        current = short if shorted else long
        return current.format(
            url=url,
            json=json,
            version=version_of_requests,
            encoding_header=encoding_header,
        )

    return _curlify_hp_curl
