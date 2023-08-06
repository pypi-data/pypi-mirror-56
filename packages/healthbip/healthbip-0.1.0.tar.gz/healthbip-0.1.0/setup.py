# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['healthbip']

package_data = \
{'': ['*']}

install_requires = \
['Django>2']

setup_kwargs = {
    'name': 'healthbip',
    'version': '0.1.0',
    'description': 'Django Application Healthchecks',
    'long_description': None,
    'author': 'Anders Innovations Oy',
    'author_email': 'admin@anders.fi',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
