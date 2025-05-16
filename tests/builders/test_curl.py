# NOTE: Very dirty tests, needs significant refactoring TODO

import json

import pytest
import requests

from curlifier.builders.curl import CurlBuilder
from curlifier.structures.commands import CommandsConfigureEnum
from curlifier.structures.http_methods import HttpMethodsEnum


@pytest.mark.parametrize('location', (True, False))
@pytest.mark.parametrize('verbose', (True, False))
@pytest.mark.parametrize('silent', (True, False))
@pytest.mark.parametrize('insecure', (True, False))
@pytest.mark.parametrize('include', (True, False))
@pytest.mark.parametrize('http_method_w_body', [method for method in HttpMethodsEnum.get_methods_with_body()])
@pytest.mark.parametrize('build_short', (True, False))
class TestCurlWithBody:  # noqa: WPS216
    def test_request_w_files(  # noqa: WPS211, WPS218
        self,
        http_method_w_body,
        mock_response,
        fake_url,
        files,
        build_short,
        transmitter_builder_w_files_payload,
        location,
        verbose,
        silent,
        insecure,
        include,
    ):
        with mock_response:
            response = requests.request(http_method_w_body, url=fake_url, files=files)
        curl = CurlBuilder(
            response=response,
            build_short=build_short,
            location=location,
            verbose=verbose,
            silent=silent,
            insecure=insecure,
            include=include,
        )
        builded = curl.build()
        assert transmitter_builder_w_files_payload(build_short, http_method_w_body, fake_url) in builded
        if location:
            assert CommandsConfigureEnum.LOCATION.get(shorted=build_short) in builded
        if verbose:
            assert CommandsConfigureEnum.VERBOSE.get(shorted=build_short) in builded
        if silent:
            assert CommandsConfigureEnum.SILENT.get(shorted=build_short) in builded
        if insecure:
            assert CommandsConfigureEnum.INSECURE.get(shorted=build_short) in builded
        if include:
            assert CommandsConfigureEnum.INCLUDE.get(shorted=build_short) in builded

    def test_request_w_json(  # noqa: WPS211, WPS218
        self,
        http_method_w_body,
        mock_response,
        fake_url,
        build_short,
        fake_json_like_dict,
        transmitter_builder_w_json_payload,
        location,
        verbose,
        silent,
        insecure,
        include,
    ):
        with mock_response:
            response = requests.request(http_method_w_body, url=fake_url, json=fake_json_like_dict)
        curl = CurlBuilder(
            response=response,
            build_short=build_short,
            location=location,
            verbose=verbose,
            silent=silent,
            insecure=insecure,
            include=include,
        )
        assert build_short == curl.build_short
        builded = curl.build()
        assert transmitter_builder_w_json_payload(
            build_short,
            http_method_w_body,
            fake_url,
            json.dumps(fake_json_like_dict),
        ) in builded

        if location:
            assert CommandsConfigureEnum.LOCATION.get(shorted=build_short) in builded
        if verbose:
            assert CommandsConfigureEnum.VERBOSE.get(shorted=build_short) in builded
        if silent:
            assert CommandsConfigureEnum.SILENT.get(shorted=build_short) in builded
        if insecure:
            assert CommandsConfigureEnum.INSECURE.get(shorted=build_short) in builded
        if include:
            assert CommandsConfigureEnum.INCLUDE.get(shorted=build_short) in builded

    def test_request_w_data(  # noqa: WPS211, WPS218
        self,
        http_method_w_body,
        mock_response,
        fake_url,
        build_short,
        fake_xml,
        transmitter_builder_w_xml_payload,
        location,
        verbose,
        silent,
        insecure,
        include,
    ):
        with mock_response:
            response = requests.request(http_method_w_body, url=fake_url, data=fake_xml)
        curl = CurlBuilder(
            response=response,
            build_short=build_short,
            location=location,
            verbose=verbose,
            silent=silent,
            insecure=insecure,
            include=include,
        )
        builded = curl.build()
        assert transmitter_builder_w_xml_payload(
            build_short,
            http_method_w_body,
            fake_url,
            fake_xml,
        ) in builded

        if location:
            assert CommandsConfigureEnum.LOCATION.get(shorted=build_short) in builded
        if verbose:
            assert CommandsConfigureEnum.VERBOSE.get(shorted=build_short) in builded
        if silent:
            assert CommandsConfigureEnum.SILENT.get(shorted=build_short) in builded
        if insecure:
            assert CommandsConfigureEnum.INSECURE.get(shorted=build_short) in builded
        if include:
            assert CommandsConfigureEnum.INCLUDE.get(shorted=build_short) in builded


@pytest.mark.parametrize('location', (True, False))
@pytest.mark.parametrize('verbose', (True, False))
@pytest.mark.parametrize('silent', (True, False))
@pytest.mark.parametrize('insecure', (True, False))
@pytest.mark.parametrize('include', (True, False))
@pytest.mark.parametrize('build_short', (True, False))
@pytest.mark.parametrize(
    'http_method_without_body',
    [method for method in HttpMethodsEnum.get_methods_without_body()],
)
class TestCurlWithOutBody:  # noqa: WPS216
    def test_request_without_body(  # noqa: WPS211, WPS218
        self,
        mock_response,
        fake_url,
        build_short,
        http_method_without_body,
        transmitter_builder_without_body_payload,
        location,
        verbose,
        silent,
        insecure,
        include,
    ):
        with mock_response:
            response = requests.request(http_method_without_body, url=fake_url)
        curl = CurlBuilder(
            response=response,
            build_short=build_short,
            location=location,
            verbose=verbose,
            silent=silent,
            insecure=insecure,
            include=include,
        )
        builded = curl.build()
        assert transmitter_builder_without_body_payload(
            build_short,
            http_method_without_body,
            fake_url,
        ) in builded

        if location:
            assert CommandsConfigureEnum.LOCATION.get(shorted=build_short) in builded
        if verbose:
            assert CommandsConfigureEnum.VERBOSE.get(shorted=build_short) in builded
        if silent:
            assert CommandsConfigureEnum.SILENT.get(shorted=build_short) in builded
        if insecure:
            assert CommandsConfigureEnum.INSECURE.get(shorted=build_short) in builded
        if include:
            assert CommandsConfigureEnum.INCLUDE.get(shorted=build_short) in builded
