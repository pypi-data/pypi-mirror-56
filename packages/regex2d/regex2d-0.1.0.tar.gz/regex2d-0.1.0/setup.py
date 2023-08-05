# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['regex2d']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'regex2d',
    'version': '0.1.0',
    'description': '2 dimensional regex engine for describing image languages',
    'long_description': None,
    'author': 'Arjoonn Sharma',
    'author_email': 'arjoonn.94@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
