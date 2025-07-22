import json

import pytest
import requests

from curlifier import CurlConfig, curlify
from curlifier.builders.exceptions import MutuallyExclusiveArgsError
from curlifier.structures.http_methods import HttpMethodsEnum


class TestCurlifyAPI:
    """Test curlify function API."""

    @pytest.mark.parametrize('build_short', [True, False])
    def test_curlify_happy_path(self, fake_url, mock_response, fake_json_like_dict, build_short, curlify_hp_curl):
        """Test basic curlify functionality."""
        with mock_response:
            response = requests.request(HttpMethodsEnum.POST.value, url=fake_url, json=fake_json_like_dict)
        curl = curlify(response, shorted=build_short, location=True)

        assert curl == curlify_hp_curl(build_short, fake_url, json.dumps(fake_json_like_dict))

    def test_curlify_with_prepared_request(self, fake_url):
        """Test curlify with PreparedRequest."""
        req = requests.Request('GET', fake_url)
        prepared = req.prepare()

        curl = curlify(prepared_request=prepared)

        assert 'curl' in curl
        assert '--request GET' in curl
        assert fake_url in curl

    def test_curlify_with_config_options(self, fake_url, mock_response):
        """Test curlify with various configuration options."""
        with mock_response:
            response = requests.get(fake_url)

        curl = curlify(
            response,
            location=True,
            verbose=True,
            insecure=True,
        )

        assert '--location' in curl
        assert '--verbose' in curl
        assert '--insecure' in curl

    def test_curlify_short_form(self, fake_url, mock_response):
        """Test curlify short form generation."""
        with mock_response:
            response = requests.get(fake_url)

        curl = curlify(response, shorted=True, location=True)

        assert '-X GET' in curl
        assert '-L' in curl


class TestCurlifyValidation:
    """Test curlify input validation."""

    def test_no_request_provided(self):
        """Test error when no request is provided."""
        with pytest.raises(ValueError, match="Either 'response' or 'prepared_request' must be provided"):
            curlify()

    def test_both_requests_provided(self, fake_url, mock_response):
        """Test error when both response and prepared_request are provided."""
        with mock_response:
            response = requests.get(fake_url)

        req = requests.Request('GET', fake_url)
        prepared = req.prepare()

        with pytest.raises(MutuallyExclusiveArgsError):
            curlify(response=response, prepared_request=prepared)

    def test_invalid_config_option(self, fake_url, mock_response):
        """Test error for invalid configuration option."""
        with mock_response:
            response = requests.get(fake_url)

        with pytest.raises(ValueError, match='Invalid configuration options'):
            curlify(response, invalid_option=True)

    def test_non_boolean_config_value(self, fake_url, mock_response):
        """Test error for non-boolean configuration value."""
        with mock_response:
            response = requests.get(fake_url)

        with pytest.raises(TypeError, match='must be a boolean'):
            curlify(response, location='yes')

    def test_non_boolean_shorted_parameter(self, fake_url, mock_response):
        """Test error for non-boolean shorted parameter."""
        with mock_response:
            response = requests.get(fake_url)

        with pytest.raises(TypeError, match="Parameter 'shorted' must be a boolean"):
            curlify(response, shorted='yes')

    def test_conflicting_silent_verbose_options(self, fake_url, mock_response):
        """Test error for conflicting silent and verbose options."""
        with mock_response:
            response = requests.get(fake_url)

        with pytest.raises(ValueError, match="Cannot use both 'silent' and 'verbose' options simultaneously"):
            curlify(response, silent=True, verbose=True)


class TestCurlConfigAPI:
    """Test CurlConfig when used independently."""

    def test_curlconfig_exported(self):
        """Test that CurlConfig is properly exported."""
        config = CurlConfig(location=True, build_short=True)

        assert config.location is True
        assert config.build_short is True

    def test_curlconfig_validation(self):
        """Test CurlConfig validation."""
        with pytest.raises(ValueError, match="Cannot use both 'silent' and 'verbose' options simultaneously"):
            CurlConfig(silent=True, verbose=True)
