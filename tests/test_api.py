import json

import pytest
import requests

from curlifier import curlify
from curlifier.structures.http_methods import HttpMethodsEnum


@pytest.mark.parametrize('shorted', [True, False])
def test_curlify_happy_path(fake_url, mock_response, fake_json_like_dict, shorted, curlify_hp_curl):
    with mock_response:
        response = requests.request(HttpMethodsEnum.POST.value, url=fake_url, json=fake_json_like_dict)
    curl = curlify(response, shorted=shorted, location=True)

    assert curl == curlify_hp_curl(shorted, fake_url, json.dumps(fake_json_like_dict))
