# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pybandit']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pybandit',
    'version': '0.0.1',
    'description': 'Imlementation of Multiarmed Bandit Algorithms',
    'long_description': None,
    'author': 'Tuhin Sharma',
    'author_email': 'tuhinsharma121@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
