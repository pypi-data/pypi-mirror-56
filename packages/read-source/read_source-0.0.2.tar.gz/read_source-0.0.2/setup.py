# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['read_source']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'read-source',
    'version': '0.0.2',
    'description': '',
    'long_description': "# Read Python3 Source File With Correct Encoding\n\naccording to <https://www.python.org/dev/peps/pep-0263/>,\npython3 source file encoding are default to be `utf-8`.\n\nBut `open()`'s encoding will be `gbk` on windows,\nSo don't use `open` without encoding to read a python3 source file. \n\n\nexample:\n\n```python\nfrom read_source import get_encoding, read\nprint(get_encoding('tests/source/gb18030/dash-star-dash.py')) # gb18030\nwith read('tests/source/gb18030/dash-star-dash.py') as f:\n    print(f.read()) \n    # -*- coding: gb18030 -*-\n```",
    'author': 'Trim21',
    'author_email': 'i@trim21.me',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
