# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['kashmir',
 'kashmir.core',
 'kashmir.core.entities',
 'kashmir.core.protocols',
 'kashmir.core.providers',
 'kashmir.providers',
 'kashmir.repositories',
 'kashmir.usecases']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0', 'python-gitlab>=1.13,<2.0', 'typing-extensions>=3.7,<4.0']

entry_points = \
{'console_scripts': ['kashmir = kashmir.cli:cli']}

setup_kwargs = {
    'name': 'kashmir',
    'version': '2019.1.2',
    'description': "Snow's DevOps CLI Toolkit",
    'long_description': None,
    'author': 'Johnny',
    'author_email': 'johnny.w.santos@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
