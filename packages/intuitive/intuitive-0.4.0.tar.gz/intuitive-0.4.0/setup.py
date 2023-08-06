# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['intuitive']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'intuitive',
    'version': '0.4.0',
    'description': '',
    'long_description': None,
    'author': 'John Smith',
    'author_email': 'John.Smith@example.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
