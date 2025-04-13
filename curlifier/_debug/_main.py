import re

import requests
from requests.models import PreparedRequest

base_usl = 'http://localhost:8000'

user = {
    'id': 10,
    'name': 'Bob',
    'age': 22
}

F1 = '/home/imtoopunkforyou/curlifier/curlifier/_debug/test0.png'
F2 = '/home/imtoopunkforyou/curlifier/curlifier/_debug/test1.txt'
F3 = '/home/imtoopunkforyou/curlifier/curlifier/_debug/test2'

xml_data = """<?xml version="1.0" ?>
<wfs:DescribeFeatureType
   service="WFS"
   version="1.0.0"
   xmlns:wfs="http://www.opengis.net/wfs"
   xmlns:myns="http://www.example.com/myns"
   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
   xmlns:xsd="http://www.w3.org/2001/XMLSchema"
   xsi:schemaLocation="http://www.opengis.net/wfs ../wfs/1.0.0/WFS-basic.xsd">
   <wfs:TypeName>myns:COLA</wfs:TypeName>
</wfs:DescribeFeatureType>"""

files = {
    'field_name_one': open(F1, 'rb'),
    'field_name_two': open(F3, 'r'),
}
response = requests.post(base_usl + '/users/add', json=user)
# response = requests.get(base_usl + '/test')

req = response.request.copy()
body = req.body

from curlifier import curlify



result = curlify(
    response,
    build_short=True,
)
print('*'*10)
print(result)
print('*'*10)
...
