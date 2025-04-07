# curlifier
(づ ◕‿◕ )づ
[Request](https://github.com/psf/requests) object to [curl](https://curl.se/) string.

## ⚠️ Attention
In development.  
May not work as you expect and may cause errors.



## Usage
```python
>> import requests
>> import curlifier

>> response = requests.get('https://example.com/')
>> curl = curlifier.curlify(response)
>> curl
"curl --location 'https://example.com/'"
```