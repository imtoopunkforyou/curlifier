# NOTE: Very dirty tests, needs significant refactoring TODO

import json

import pytest
import requests

from curlifier.builders.curl import CurlBuilder, CurlConfig


class TestCurlConfig:
    """Test CurlConfig dataclass."""

    def test_default_config(self):
        """Test default configuration values."""
        config = CurlConfig()
        assert config.location is False
        assert config.verbose is False
        assert config.silent is False
        assert config.insecure is False
        assert config.include is False
        assert config.build_short is False

    def test_custom_config(self):
        """Test custom configuration values."""
        config = CurlConfig(
            location=True,
            verbose=True,
            build_short=True,
        )
        assert config.location is True
        assert config.verbose is True
        assert config.build_short is True
        assert config.silent is False  # Still default

    def test_conflicting_options_validation(self):
        """Test that silent and verbose cannot be used together."""
        with pytest.raises(ValueError, match="Cannot use both 'silent' and 'verbose' options simultaneously"):
            CurlConfig(silent=True, verbose=True)


class TestCurlBuilder:
    """Test CurlBuilder functionality."""

    def test_basic_get_request(self, mock_response, fake_url):
        """Test basic GET request without body."""
        with mock_response:
            response = requests.get(fake_url)

        config = CurlConfig()
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        assert 'curl' in result
        assert '--request GET' in result
        assert fake_url in result

    def test_post_request_with_json(self, mock_response, fake_url, fake_json_like_dict):
        """Test POST request with JSON data."""
        with mock_response:
            response = requests.post(fake_url, json=fake_json_like_dict)

        config = CurlConfig()
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        assert 'curl' in result
        assert '--request POST' in result
        assert fake_url in result
        assert '--data' in result
        assert json.dumps(fake_json_like_dict) in result

    def test_short_form_generation(self, mock_response, fake_url):
        """Test short form curl generation."""
        with mock_response:
            response = requests.get(fake_url)

        config = CurlConfig(build_short=True)
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        assert 'curl' in result
        assert '-X GET' in result  # Short form
        assert '--request GET' not in result  # Long form should not be present

    def test_configuration_options(self, mock_response, fake_url):
        """Test various configuration options."""
        with mock_response:
            response = requests.get(fake_url)

        config = CurlConfig(
            location=True,
            verbose=True,
            insecure=True,
        )
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        assert '--location' in result
        assert '--verbose' in result
        assert '--insecure' in result

    def test_configuration_options_short_form(self, mock_response, fake_url):
        """Test configuration options in short form."""
        with mock_response:
            response = requests.get(fake_url)

        config = CurlConfig(
            location=True,
            verbose=True,
            build_short=True,
        )
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        assert '-L' in result  # Short form for location
        assert '-v' in result  # Short form for verbose

    @pytest.mark.parametrize('method', ['POST', 'PUT', 'PATCH'])
    def test_methods_with_body(self, mock_response, fake_url, fake_json_like_dict, method):
        """Test HTTP methods that typically have body."""
        with mock_response:
            response = requests.request(method, url=fake_url, json=fake_json_like_dict)

        config = CurlConfig()
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        assert f'--request {method}' in result
        assert '--data' in result

    @pytest.mark.parametrize('method', ['GET', 'HEAD', 'DELETE', 'OPTIONS'])
    def test_methods_without_body(self, mock_response, fake_url, method):
        """Test HTTP methods that typically don't have body."""
        with mock_response:
            response = requests.request(method, url=fake_url)

        config = CurlConfig()
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        assert f'--request {method}' in result
        assert '--data' not in result

    def test_file_upload(self, mock_response, fake_url, files):
        """Test file upload requests."""
        with mock_response:
            response = requests.post(fake_url, files=files)

        config = CurlConfig()
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        assert '--form' in result or '-F' in result

    def test_prepared_request_usage(self, fake_url):
        """Test using PreparedRequest instead of Response."""
        req = requests.Request('GET', fake_url)
        prepared = req.prepare()

        config = CurlConfig()
        builder = CurlBuilder(config=config, prepared_request=prepared)
        result = builder.build()

        assert 'curl' in result
        assert '--request GET' in result
        assert fake_url in result

    def test_build_short_property(self, mock_response, fake_url):
        """Test build_short property."""
        with mock_response:
            response = requests.get(fake_url)

        config = CurlConfig(build_short=True)
        builder = CurlBuilder(config=config, response=response)

        assert builder.build_short is True

    def test_xml_data_handling(self, mock_response, fake_url, fake_xml):
        """Test handling of XML data."""
        with mock_response:
            response = requests.post(fake_url, data=fake_xml)

        config = CurlConfig()
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        assert '--data' in result
        assert fake_xml.replace('\n', ' ').strip() in result  # XML is normalized


class TestCurlBuilderEdgeCases:
    """Test edge cases and error conditions."""

    def test_empty_config_works(self, mock_response, fake_url):
        """Test that empty config works correctly."""
        with mock_response:
            response = requests.get(fake_url)

        config = CurlConfig()
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        # Should contain basic curl command without extra options
        assert result.startswith('curl --request GET')
        assert '--location' not in result
        assert '--verbose' not in result

    def test_headers_are_included(self, mock_response, fake_url):
        """Test that headers are included in curl command."""
        custom_headers = {'X-Custom-Header': 'test-value'}
        with mock_response:
            response = requests.get(fake_url, headers=custom_headers)

        config = CurlConfig()
        builder = CurlBuilder(config=config, response=response)
        result = builder.build()

        assert '--header' in result
        assert 'X-Custom-Header: test-value' in result
