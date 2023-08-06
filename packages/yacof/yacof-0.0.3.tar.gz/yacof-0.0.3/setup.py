# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['yacof']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.1,<2.0', 'ruamel.yaml>=0.16.5,<0.17.0']

entry_points = \
{'console_scripts': ['yacof = yacof.cli:main']}

setup_kwargs = {
    'name': 'yacof',
    'version': '0.0.3',
    'description': 'Yet another YAML config library',
    'long_description': None,
    'author': 'fbjorn',
    'author_email': 'kopfabschneider@yandex.ru',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
