# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['neeraj_poetry_demo']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.0,<3.0']

setup_kwargs = {
    'name': 'neeraj-poetry-demo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Neeraj Chaudhary',
    'author_email': 'neeraj_chaudhary@mcafee.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=2.7,<3.0',
}


setup(**setup_kwargs)
