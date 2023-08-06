# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['repyl']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'repyl',
    'version': '0.2.0',
    'description': '',
    'long_description': None,
    'author': 'Ben G',
    'author_email': 'ben.gordon@toasttab.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
