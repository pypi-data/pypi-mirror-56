# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['read_source']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'read-source',
    'version': '0.0.1',
    'description': '',
    'long_description': None,
    'author': 'Trim21',
    'author_email': 'i@trim21.me',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.5,<4.0',
}


setup(**setup_kwargs)
