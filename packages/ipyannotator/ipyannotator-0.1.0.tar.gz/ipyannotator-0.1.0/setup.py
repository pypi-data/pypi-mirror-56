# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ipyannotator']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ipyannotator',
    'version': '0.1.0',
    'description': 'ipython widgets for data annotation',
    'long_description': None,
    'author': 'Palaimon OSS ',
    'author_email': 'oss@palaimon.io',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
