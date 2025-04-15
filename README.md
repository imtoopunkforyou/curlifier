# curlifier
(づ ◕‿◕ )づ
[Request](https://github.com/psf/requests) object to [curl](https://curl.se/) string.

# ⚠️ Attention
- In development.  
- May not work as you expect and may cause errors.
- Currently not published on PyPI.


## Usage
```python
>> import requests
>> from curlifier import curlify

>> response = requests.get('https://example.com/')
>> curl = curlify(response)
>> curl
"curl --request GET 'https://example.com/' --header 'User-Agent: python-requests/2.32.3' --header 'Accept-Encoding: gzip, deflate' --header 'Accept: */*' --header 'Connection: keep-alive'  --location"
```

## TODO
- [ ] readme.md
- [ ] tests
- [ ] docs
- [ ] publish on pypi
- [ ] delete `./_debug`
- [ ] `__version__.py`