import json
import os
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


@pytest.fixture
def file_path_builder():
    def _file_path_builder(file_name):
        files_dir = 'tests/files/'
        return os.path.join(files_dir, file_name)

    return _file_path_builder


@pytest.fixture
def files(file_path_builder):
    pic = file_path_builder('f.jpg')
    voice = file_path_builder('f.mp3')
    text = file_path_builder('f.txt')

    return {
        'field_for_pic': open(pic, 'rb'),
        'field_for_voice': open(voice, 'rb'),
        'field_for_text': open(text, 'r'),
    }


@pytest.fixture
def fake_xml():
    xml = (
        '<?xml version="1.0" encoding="utf-8"?>'
        '<root xmlns="http://defaultns.com/" xmlns:a="http://a.com/'
        'xmlns:b="http://b.com/"><x a:attr="val">1</x><a:y>2</a:y><b:z>3</b:z></root>'
    )

    return xml


@pytest.fixture
def transmitter_builder_w_files_payload():
    def _transmitter_builder_w_files_payload(shorted, method, url):
        long = (
            "--request {method} '{url}' "
            "--header 'User-Agent: python-requests/2.32.3' "
            "--header 'Accept-Encoding: gzip, deflate' "
            "--header 'Accept: */*' "
            "--header 'Connection: keep-alive' "
            "--header 'Content-Type: multipart/form-data' "
            "--form 'field_for_pic=@f.jpg' "
            "--form 'field_for_voice=@f.mp3' "
            "--form 'field_for_text=@f.txt'"
        )
        short = (
            "-X {method} '{url}' "
            "-H 'User-Agent: python-requests/2.32.3' "
            "-H 'Accept-Encoding: gzip, deflate' "
            "-H 'Accept: */*' "
            "-H 'Connection: keep-alive' "
            "-H 'Content-Type: multipart/form-data' "
            "-F 'field_for_pic=@f.jpg' "
            "-F 'field_for_voice=@f.mp3' "
            "-F 'field_for_text=@f.txt'"
        )
        current = short if shorted else long
        return current.format(
            method=method,
            url=url,
        )

    return _transmitter_builder_w_files_payload


@pytest.fixture
def transmitter_builder_w_json_payload():
    def _transmitter_builder_w_json_payload(shorted, method, url, json):
        long = (
            "--request {method} '{url}' "
            "--header 'User-Agent: python-requests/2.32.3' "
            "--header 'Accept-Encoding: gzip, deflate' "
            "--header 'Accept: */*' "
            "--header 'Connection: keep-alive' "
            "--header 'Content-Type: application/json' "
            "--data '{json}'"
        )
        short = (
            "-X {method} '{url}' "
            "-H 'User-Agent: python-requests/2.32.3' "
            "-H 'Accept-Encoding: gzip, deflate' "
            "-H 'Accept: */*' "
            "-H 'Connection: keep-alive' "
            "-H 'Content-Type: application/json' "
            "-d '{json}'"
        )
        current = short if shorted else long
        return current.format(
            method=method,
            url=url,
            json=json,
        )

    return _transmitter_builder_w_json_payload


@pytest.fixture
def transmitter_builder_w_xml_payload():
    def _transmitter_builder_w_xml_payload(shorted, method, url, xml):
        long = (
            "--request {method} '{url}' "
            "--header 'User-Agent: python-requests/2.32.3' "
            "--header 'Accept-Encoding: gzip, deflate' "
            "--header 'Accept: */*' "
            "--header 'Connection: keep-alive' "
            "--data '{xml}'"
        )
        short = (
            "-X {method} '{url}' "
            "-H 'User-Agent: python-requests/2.32.3' "
            "-H 'Accept-Encoding: gzip, deflate' "
            "-H 'Accept: */*' "
            "-H 'Connection: keep-alive' "
            "-d '{xml}'"
        )
        current = short if shorted else long
        return current.format(
            method=method,
            url=url,
            xml=xml,
        )

    return _transmitter_builder_w_xml_payload


@pytest.fixture
def transmitter_builder_without_body_payload():
    def _transmitter_builder_without_body_payload(shorted, method, url):
        long = (
            "--request {method} '{url}' "
            "--header 'User-Agent: python-requests/2.32.3' "
            "--header 'Accept-Encoding: gzip, deflate' "
            "--header 'Accept: */*' "
            "--header 'Connection: keep-alive' "
        )
        short = (
            "-X {method} '{url}' "
            "-H 'User-Agent: python-requests/2.32.3' "
            "-H 'Accept-Encoding: gzip, deflate' "
            "-H 'Accept: */*' "
            "-H 'Connection: keep-alive' "
        )
        current = short if shorted else long
        return current.format(
            method=method,
            url=url,
        )

    return _transmitter_builder_without_body_payload
