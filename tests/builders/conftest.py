import pytest


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
