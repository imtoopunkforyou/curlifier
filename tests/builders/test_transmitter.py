import json

import pytest
import requests

from curlifier.builders.transmitter import (
    Decoder,
    PreparedTransmitter,
    TransmitterBuilder,
)
from curlifier.structures.http_methods import HttpMethodsEnum


class PreparedTransmitterTest:
    trash_headers = (
        'Content-Length',
    )


@pytest.mark.parametrize('http_method_w_body', [method for method in HttpMethodsEnum.get_methods_with_body()])
class TestPreparedTransmitterWithBody(PreparedTransmitterTest):
    def test_w_files(self, http_method_w_body, mock_response, fake_url, files):
        with mock_response:
            response = requests.request(http_method_w_body, url=fake_url, files=files)
        prepared_transmitter = PreparedTransmitter(response)
        assert prepared_transmitter.url
        assert prepared_transmitter.method
        assert prepared_transmitter.body
        assert prepared_transmitter.has_body
        assert prepared_transmitter.headers.get('Content-Type') == 'multipart/form-data'

    def test_w_json(self, http_method_w_body, mock_response, fake_url, fake_json_like_dict):
        with mock_response:
            response = requests.request(http_method_w_body, url=fake_url, json=fake_json_like_dict)
        prepared_transmitter = PreparedTransmitter(response)

        assert prepared_transmitter.url
        assert prepared_transmitter.method
        assert prepared_transmitter.body
        assert prepared_transmitter.has_body
        for header in self.trash_headers:
            assert prepared_transmitter.headers.get(header) is None

    def test_w_data(self, http_method_w_body, mock_response, fake_url, fake_xml):
        with mock_response:
            response = requests.request(http_method_w_body, url=fake_url, data=fake_xml)
        prepared_transmitter = PreparedTransmitter(response)

        assert prepared_transmitter.url
        assert prepared_transmitter.method
        assert prepared_transmitter.body
        assert prepared_transmitter.has_body
        for header in self.trash_headers:
            assert prepared_transmitter.headers.get(header) is None


@pytest.mark.parametrize(
    'http_method_without_body',
    [method for method in HttpMethodsEnum.get_methods_without_body()],
)
class TestPreparedTransmitterWithOutBody(PreparedTransmitterTest):

    def test_without_body(self, http_method_without_body, mock_response, fake_url):
        with mock_response:
            response = requests.request(http_method_without_body, url=fake_url)
        prepared_transmitter = PreparedTransmitter(response)

        assert prepared_transmitter.url
        assert prepared_transmitter.method
        assert prepared_transmitter.body is None
        assert prepared_transmitter.has_body is False
        for header in self.trash_headers:
            assert prepared_transmitter.headers.get(header) is None


@pytest.mark.parametrize('http_method_w_body', [method for method in HttpMethodsEnum.get_methods_with_body()])
@pytest.mark.parametrize('build_short', (True, False))
class TestTransmitterBuilderWithBody:
    def test_request_w_files(
        self,
        http_method_w_body,
        mock_response,
        fake_url,
        files,
        build_short,
        transmitter_builder_w_files_payload,
    ):
        with mock_response:
            response = requests.request(http_method_w_body, url=fake_url, files=files)
        transmitter_builder = TransmitterBuilder(response=response, build_short=build_short)
        builded = transmitter_builder.build()
        assert builded == transmitter_builder_w_files_payload(build_short, http_method_w_body, fake_url)

    def test_request_w_json(
        self,
        http_method_w_body,
        mock_response,
        fake_url,
        build_short,
        fake_json_like_dict,
        transmitter_builder_w_json_payload,
    ):
        with mock_response:
            response = requests.request(http_method_w_body, url=fake_url, json=fake_json_like_dict)
        transmitter_builder = TransmitterBuilder(response=response, build_short=build_short)
        builded = transmitter_builder.build()
        assert builded == transmitter_builder_w_json_payload(
            build_short,
            http_method_w_body,
            fake_url,
            json.dumps(fake_json_like_dict),
        )

    def test_request_w_data(
        self,
        http_method_w_body,
        mock_response,
        fake_url,
        build_short,
        fake_xml,
        transmitter_builder_w_xml_payload,
    ):
        with mock_response:
            response = requests.request(http_method_w_body, url=fake_url, data=fake_xml)
        transmitter_builder = TransmitterBuilder(response=response, build_short=build_short)
        builded = transmitter_builder.build()
        assert builded == transmitter_builder_w_xml_payload(
            build_short,
            http_method_w_body,
            fake_url,
            fake_xml,
        )


@pytest.mark.parametrize(
    'http_method_without_body',
    [method for method in HttpMethodsEnum.get_methods_without_body()],
)
@pytest.mark.parametrize('build_short', (True, False))
class TestTransmitterBuilderWithOutBody:
    def test_request_without_body(
        self,
        mock_response,
        fake_url,
        build_short,
        http_method_without_body,
        transmitter_builder_without_body_payload,
    ):
        with mock_response:
            response = requests.request(http_method_without_body, url=fake_url)
        transmitter_builder = TransmitterBuilder(response=response, build_short=build_short)
        builded = transmitter_builder.build()
        assert builded == transmitter_builder_without_body_payload(
            build_short,
            http_method_without_body,
            fake_url,
        )


def test_prepared_transmitter_w_exception(mock_response, fake_url, fake_json_like_dict):
    with mock_response:
        response = requests.request(
            HttpMethodsEnum.POST.value,
            url=fake_url,
            json=fake_json_like_dict,
        )
    with pytest.raises(ValueError):
        PreparedTransmitter(response, prepared_request='prepared_req_obj')


def test_decoder_w_exception():
    undecoded_obj = False
    decoder = Decoder()

    with pytest.raises(TypeError):
        decoder.decode(undecoded_obj)
