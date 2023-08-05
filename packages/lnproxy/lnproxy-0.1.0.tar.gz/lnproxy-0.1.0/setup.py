# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lnproxy']

package_data = \
{'': ['*']}

install_requires = \
['docopt>=0.6.2,<0.7.0',
 'hkdf>=0.0.3,<0.0.4',
 'pylightning>=0.0.7.3,<0.0.8.0',
 'secp256k1>=0.13.2,<0.14.0',
 'trio>=0.13.0,<0.14.0']

setup_kwargs = {
    'name': 'lnproxy',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'willcl-ark',
    'author_email': 'will8clark@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
