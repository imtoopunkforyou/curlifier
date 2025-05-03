# curlifier
[![coverage](https://raw.githubusercontent.com/imtoopunkforyou/curlifier/main/.github/badge/coverage.svg)](https://github.com/pytest-dev/pytest-cov)
[![tests](https://github.com/imtoopunkforyou/curlifier/actions/workflows/tests.yaml/badge.svg)](https://github.com/imtoopunkforyou/curlifier/actions/workflows/tests.yaml)
[![pypi package version](https://img.shields.io/pypi/v/curlifier.svg)](https://pypi.org/project/curlifier)
[![pypi downloads](https://img.shields.io/pypi/dm/curlifier.svg)](https://pypi.org/project/curlifier)
[![supported python versions](https://img.shields.io/pypi/pyversions/curlifier.svg)](https://pypi.org/project/curlifier)
[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![license](https://img.shields.io/pypi/l/curlifier.svg)](https://github.com/imtoopunkforyou/curlifier/blob/main/LICENSE)


```
░█████╗░██╗░░░██╗██████╗░██╗░░░░░██╗███████╗██╗███████╗██████╗░
██╔══██╗██║░░░██║██╔══██╗██║░░░░░██║██╔════╝██║██╔════╝██╔══██╗
██║░░╚═╝██║░░░██║██████╔╝██║░░░░░██║█████╗░░██║█████╗░░██████╔╝
██║░░██╗██║░░░██║██╔══██╗██║░░░░░██║██╔══╝░░██║██╔══╝░░██╔══██╗
╚█████╔╝╚██████╔╝██║░░██║███████╗██║██║░░░░░██║███████╗██║░░██║
░╚════╝░░╚═════╝░╚═╝░░╚═╝╚══════╝╚═╝╚═╝░░░░░╚═╝╚══════╝╚═╝░░╚═╝
```

Converts the [Request](https://requests.readthedocs.io/en/latest/api/#requests.Response) and [PreparedRequest](https://requests.readthedocs.io/en/latest/api/#requests.PreparedRequest) objects of the [Requests](https://pypi.org/project/requests/) library into an executable [curl](https://curl.se/) command.

## Installation
```bash
pip install curlifier
```

### Dependencies
- `python (>=3.10, <4.0)`
- `requests (>=2.0, <3.0.0)`

## Usage
All you need is to import `curlify`.  
For example:
```python
>>> import requests
>>> from curlifier import curlify
>>> body = {'id': 1, 'name': 'Tima', 'age': 28}
>>> r = requests.post('https://httpbin.org/', json=body)
>>> curlify(r)
curl --request POST 'https://httpbin.org/' <...> --header 'Content-Type: application/json' --data '{"id": 1, "name": "Tima", "age": 28}'
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
curl -X POST 'https://httpbin.org/' <...> -H 'Content-Type: application/json' -d '{"id": 1, "name": "Tima", "age": 28}'
```
You can also specify the configuration when forming the curl command:
```python
>>> curlify(r, location=True, insecure=True)
curl --request POST 'https://httpbin.org/' <...> --header 'Content-Type: application/json' --data '{"id": 1, "name": "Tima", "age": 28}' --location --insecure
```
- **location** (bool) - Follow redirects (default: False)
- **verbose** (bool) - Verbose output (default: False)
- **silent** (bool) - Silent mode (default: False)
- **insecure** (bool) - Allow insecure connections (default: False)
- **include** (bool) - Include protocol headers (default: False)

## License
Curlifier is released under the MIT License. See the bundled [LICENSE](https://github.com/imtoopunkforyou/curlifier/blob/main/LICENSE) file for details.
