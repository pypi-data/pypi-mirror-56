# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hilale']

package_data = \
{'': ['*']}

install_requires = \
['pyautogui>=0.9.48,<0.10.0']

setup_kwargs = {
    'name': 'hilale',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'rkshrksh',
    'author_email': 'aarkaygautam@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
