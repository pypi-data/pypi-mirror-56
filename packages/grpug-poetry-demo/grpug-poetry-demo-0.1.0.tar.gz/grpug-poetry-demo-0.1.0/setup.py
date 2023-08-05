# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['grpug_poetry_demo']

package_data = \
{'': ['*']}

install_requires = \
['django>=2,<3']

setup_kwargs = {
    'name': 'grpug-poetry-demo',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Jace Browning',
    'author_email': 'jacebrowning@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
