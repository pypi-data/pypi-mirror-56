# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['stockholm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stockholm',
    'version': '0.0.0',
    'description': 'An up to date human friendly and flexible approach for development with any kind of monetary amounts',
    'long_description': '# `stockholm`\nLibrary for formatting and performing arithmetic and comparison operations on monetary amounts. Also with support for currency handling, exchange and network transport generation + parsing.\n\nAn up to date human friendly and flexible approach for development with any kind of monetary amounts.\n\nAt its bone a `Money` class for Python 3. A library for merchant developers, fintech companies and subscription services. A simple, yet powerful way of working with money in development.\n\n### Acknowledgements\nBuilt with inspiration from https://github.com/carlospalol/money and https://github.com/vimeo/py-money',
    'author': 'Carl Oscar Aaro',
    'author_email': 'hello@carloscar.com',
    'url': 'https://github.com/kalaspuff/stockholm',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
