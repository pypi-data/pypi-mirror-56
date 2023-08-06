# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['stockholm']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'stockholm',
    'version': '0.0.6',
    'description': 'An up to date human friendly and flexible approach for development with any kind of monetary amounts',
    'long_description': '# `stockholm` — `Money` for Python 3\n[![pypi](https://badge.fury.io/py/stockholm.svg)](https://pypi.python.org/pypi/stockholm/)\n[![MIT License](https://img.shields.io/github/license/kalaspuff/stockholm.svg)](https://github.com/kalaspuff/stockholm/blob/master/LICENSE)\n[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)\n\nLibrary for formatting and performing arithmetic and comparison operations on monetary amounts. Also with support for currency handling, exchange and network transport structure generation as well as parsing.\n\nAn up to date human friendly and flexible approach for development with any kind of monetary amounts.\n\nAt its bone a `Money` class for Python 3.x. This is a library to be used by backend and frontend API coders of fintech companies, web merchants and subscription services. A simple, yet powerful way of coding with money.\n\nThe `stockholm.Money` object has full arithmetic support together with `int`, `float`, `Decimal`, other `Money` objects as well as `string`. `stockholm.Money` object also supports complex string formatting functionality for easy debugging and a clean coding pattern.\n\n### Installation with `pip`\n```\n$ pip install stockholm\n```\n\n### Examples\nFull arithmetic support with different types, backed by `Decimal` for dealing with rounding errors, while also keeping the monetary amount fully currency aware.\n```python\nfrom stockholm import Money\n\nmoney = Money("4711.50", currency="SEK")\nprint(money)\n# 4711.50 SEK\n\noutput = (money + 100) * 3 + Money(50)\nprint(output)\n# 14484.50 SEK\n\nprint(output / 5)\n# 2896.90 SEK\n\nprint(round(output / 3, 4))\n# 4828.1667 SEK\n\nprint(round(output / 3, 1))\n# 4828.20 SEK\n```\n\nAdvanced string formatting functionality\n```python\nfrom stockholm import Money\n\njpy_money = Money(1352953, "JPY")\nexchange_rate = Money("0.08861326")\nsek_money = Money(jpy_money * exchange_rate, "SEK")\n\nprint(f"I have {jpy_money:,.0m} which equals around {sek_money:,.2m}")\nprint(f"The exchange rate is {exchange_rate} ({jpy_money:c} -> {sek_money:c})")\n# I have 1,352,953 JPY which equals around 119,889.58 SEK\n# The exchange rate is 0.08861326 (JPY -> SEK)\n\nprint(f"{jpy_money:.0f}")\n# 1352953\n\nprint(f"{sek_money:.2f}")\n# 119889.58\n\nprint(f"{sek_money:.1f}")\n# 119889.6\n\nprint(f"{sek_money:.0f}")\n# 119890\n```\n\nFlexible ways for assigning values to a monetary amount\n```python\nfrom decimal import Decimal\nfrom stockholm import Money\n\nMoney(100, currency="EUR")\n# <stockholm.Money: "100.00 EUR">\n\nMoney("1338 USD")\n# <stockholm.Money: "1338.00 USD">\n\nMoney("0.5")\n# <stockholm.Money: "0.50">\n\namount = Decimal(5000) / 3\nMoney(amount, currency="XDR")\n# <stockholm.Money: "1666.666666667">\n\nmoney = Money("0.30285471")\nMoney(money, currency="BTC")\n# <stockholm.Money: "0.30285471 BTC">\n\ncents_as_str = "471100"\nMoney(cents_as_str, currency="USD", is_cents=True)\n# <stockholm.Money: "4711.00 USD">\n```\n\nAdding several monetary amounts from a list\n```python\nfrom stockholm import Money\n\namounts = [\n    Money(1),\n    Money("1.50"),\n    Money("1000"),\n]\n\n# Use Money.sum to deal with complex values of different data types\nMoney.sum(amounts)\n# <stockholm.Money: "1002.50">\n\n# Built-in sum may also be used (if only working with monetary amounts)\nsum(amounts)\n# <stockholm.Money: "1002.50">\n```\n\n### Acknowledgements\nBuilt with inspiration from https://github.com/carlospalol/money and https://github.com/vimeo/py-money\n',
    'author': 'Carl Oscar Aaro',
    'author_email': 'hello@carloscar.com',
    'url': 'https://github.com/kalaspuff/stockholm',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
