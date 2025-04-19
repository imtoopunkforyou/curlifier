# curlifier
```
░█████╗░██╗░░░██╗██████╗░██╗░░░░░██╗███████╗██╗███████╗██████╗░
██╔══██╗██║░░░██║██╔══██╗██║░░░░░██║██╔════╝██║██╔════╝██╔══██╗
██║░░╚═╝██║░░░██║██████╔╝██║░░░░░██║█████╗░░██║█████╗░░██████╔╝
██║░░██╗██║░░░██║██╔══██╗██║░░░░░██║██╔══╝░░██║██╔══╝░░██╔══██╗
╚█████╔╝╚██████╔╝██║░░██║███████╗██║██║░░░░░██║███████╗██║░░██║
░╚════╝░░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝
```

Curlifier converts the [Request](https://requests.readthedocs.io/en/latest/api/#requests.Response) and [PreparedRequest](https://requests.readthedocs.io/en/latest/api/#requests.PreparedRequest) objects of the [Requests](https://pypi.org/project/requests/) library into an executable [curl](https://curl.se/) command.

## Installation
Curlifier is available on [PyPI](https://pypi.org/project/curlifier/):
```bash
pip install curlifier
```

### Dependencies
- `python (>=3.12, <4.0)`
- `requests (>=2.30.3, <3.0.0)`

## Usage
All you need is to import `curlify`.  
For example:
```python
>>> import requests
>>> from curlifier import curlify
>>> body = {'id': 1, 'name': 'Tima', 'age': 28}
>>> r = requests.post('https://httpbin.org/', json=body)
>>> curlify(r)
curl --request POST 'https://httpbin.org/' --header 'User-Agent: python-requests/2.32.3' --header 'Accept-Encoding: gzip, deflate' --header 'Accept: */*' --header 'Connection: keep-alive' --header 'Content-Type: application/json' --data '{"id": 1, "name": "Tima", "age": 28}'
```
If you use `PraparedRequest`, you can also specify it instead of the `Response` object:
```python
>>> req = requests.Request('POST', 'https://httpbin.org/')
>>> r = req.prepare()
>>> curlify(prepared_request=r)
curl --request POST 'https://httpbin.org/'
```
If you want a short version of the curl command, you can specify it:
```python
>>> body = {'id': 1, 'name': 'Tima', 'age': 28}
>>> r = requests.post('https://httpbin.org/', json=body)
>>> curlify(r, shorted=True)
curl -X POST 'https://httpbin.org/' -H 'User-Agent: python-requests/2.32.3' -H 'Accept-Encoding: gzip, deflate' -H 'Accept: */*' -H 'Connection: keep-alive' -H 'Content-Type: application/json' -d '{"id": 1, "name": "Tima", "age": 28}'
```
You can also specify the configuration when forming the curl command:
```python
>>> curlify(r, location=True, verbose=True, silent=True, insecure=True, include=True)
curl --request POST 'https://httpbin.org/' --header 'User-Agent: python-requests/2.32.3' --header 'Accept-Encoding: gzip, deflate' --header 'Accept: */*' --header 'Connection: keep-alive' --header 'Content-Type: application/json' --data '{"id": 1, "name": "Tima", "age": 28}' --location --verbose --silent --insecure --include
```
- **location** (bool) - Follow redirects (default: False)
- **verbose** (bool) - Verbose output (default: False)
- **silent** (bool) - Silent mode (default: False)
- **insecure** (bool) - Allow insecure connections (default: False)
- **include** (bool) - Include protocol headers (default: False)

## License
Curlifier is released under the MIT License. See the bundled [LICENSE](LICENSE) file for details.
