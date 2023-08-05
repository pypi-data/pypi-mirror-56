# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['um', 'um.collections', 'um.crypto', 'um.statistics', 'um.visuals']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.17,<2.0', 'pandas>=0.25.3,<0.26.0']

setup_kwargs = {
    'name': 'um',
    'version': '1.5.3',
    'description': '',
    'long_description': 'um utils\n=========\n\nProject contains utility functions\n\n\nInstallation\n------------\n\nTo install via `pip` run command\n\n::\n\n    $ pip install um\n\n\nContents\n--------\n\nContents of the package\n\n* utility functions\n* visual package with color utilities\n* collections module',
    'author': 'umatbro',
    'author_email': 'umatbroo@gmail.com',
    'url': 'https://github.com/umatbro/u-utils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
