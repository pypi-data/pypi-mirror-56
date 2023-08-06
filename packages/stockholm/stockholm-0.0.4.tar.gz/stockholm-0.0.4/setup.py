# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['stockholm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stockholm',
    'version': '0.0.4',
    'description': 'An up to date human friendly and flexible approach for development with any kind of monetary amounts',
    'long_description': '# `stockholm` — `Money` for Python 3\n[![pypi](https://badge.fury.io/py/stockholm.svg)](https://pypi.python.org/pypi/stockholm/)\n[![MIT License](https://img.shields.io/github/license/kalaspuff/stockholm.svg)](https://github.com/kalaspuff/stockholm/blob/master/LICENSE)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n\nLibrary for formatting and performing arithmetic and comparison operations on monetary amounts. Also with support for currency handling, exchange and network transport structure generation as well as parsing.\n\nAn up to date human friendly and flexible approach for development with any kind of monetary amounts.\n\nAt its bone a `Money` class for Python 3.x. This is a library to be used by backend and frontend API coders of fintech companies, web merchants and subscription services. A simple, yet powerful way of coding with money.\n\n### Installation with `pip`\n``` \n$ pip install stockholm\n```\n\n### Examples\n```python\nfrom stockholm import Money\n\n# Example code in development\n```\n    \n\n### Acknowledgements\nBuilt with inspiration from https://github.com/carlospalol/money and https://github.com/vimeo/py-money\n',
    'author': 'Carl Oscar Aaro',
    'author_email': 'hello@carloscar.com',
    'url': 'https://github.com/kalaspuff/stockholm',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
