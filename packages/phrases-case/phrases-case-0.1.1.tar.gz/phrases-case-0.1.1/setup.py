# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['phrases_case']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'phrases-case',
    'version': '0.1.1',
    'description': 'Convert phrases between different cases.',
    'long_description': "# phrases case\n\n[![build status](https://github.com/NateScarlet/phrases-case/workflows/Python%20package/badge.svg)](https://github.com/NateScarlet/phrases-case/actions)\n[![version](https://img.shields.io/pypi/v/phrases-case)](https://pypi.org/project/phrases-case/)\n![python version](https://img.shields.io/pypi/pyversions/phrases-case)\n![wheel](https://img.shields.io/pypi/wheel/phrases-case)\n\nConvert phrases between different cases.\n\nNot using `re` module.\n\n```python\n>>> import phrases_case\n>>> phrases_case.snake('camelCase')\n'camel_case'\n>>> phrases_case.snake('camelCase', separator='-')\n'camel-case'\n>>> phrases_case.hyphen('camelCase')\n'camel-case'\n>>> phrases_case.space('camelCase')\n'camel case'\n>>> phrases_case.camel('snake_case')\n'snakeCase'\n>>> phrases_case.pascal('snake_case')\n'SnakeCase'\n```\n",
    'author': 'NateScarlet',
    'author_email': 'NateScarlet@Gmail.com',
    'url': 'https://github.com/NateScarlet/phrases-case',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
