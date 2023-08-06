# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['lgw']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.10,<2.0',
 'docker>=4.1,<5.0',
 'docopt>=0.6.2,<0.7.0',
 'everett>=1.0,<2.0']

entry_points = \
{'console_scripts': ['lgw = lgw.main:main']}

setup_kwargs = {
    'name': 'lgw',
    'version': '1.0.0',
    'description': 'Lambda Gateway',
    'long_description': None,
    'author': 'Edward Q. Bridges',
    'author_email': 'ebridges@roja.cc',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
