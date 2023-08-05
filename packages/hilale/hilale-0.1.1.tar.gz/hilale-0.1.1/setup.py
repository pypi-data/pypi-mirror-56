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
    'version': '0.1.1',
    'description': 'A simple python utility to keep the mouse moving on the screen',
    'long_description': '# Hilale\n\nA python utility to keep the mouse moving and keep the system from getting locked.\n',
    'author': 'rkshrksh',
    'author_email': 'aarkaygautam@gmail.com',
    'url': 'https://github.com/rkshrksh/Hilale',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
