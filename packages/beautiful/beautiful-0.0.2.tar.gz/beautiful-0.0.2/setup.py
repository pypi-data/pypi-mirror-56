# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['beautiful']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'beautiful',
    'version': '0.0.2',
    'description': 'A collection of functions and classes to aid developers into building better code faster',
    'long_description': '# `beautiful`\n[![pypi](https://badge.fury.io/py/beautiful.svg)](https://pypi.python.org/pypi/beautiful/)\n[![Made with Python](https://img.shields.io/pypi/pyversions/beautiful)](https://www.python.org/)\n[![Type hinted - mypy validated](https://img.shields.io/badge/typehinted-yes-teal)](https://github.com/kalaspuff/beautiful)\n[![MIT License](https://img.shields.io/github/license/kalaspuff/beautiful.svg)](https://github.com/kalaspuff/beautiful/blob/master/LICENSE)\n[![Code coverage](https://codecov.io/gh/kalaspuff/beautiful/branch/master/graph/badge.svg)](https://codecov.io/gh/kalaspuff/beautiful/tree/master/beautiful)\n\n*A collection of functions and classes to aid developers into building better code faster.*\n\n\n## Installation with `pip`\nLike you would install any other Python package, use `pip`, `poetry`, `pipenv` or your weapon of choice.\n```\n$ pip install beautiful\n```\n\n\n## Usage and examples\n\n#### Use-case\n```\nimport beautiful\n\n```\n',
    'author': 'Carl Oscar Aaro',
    'author_email': 'hello@carloscar.com',
    'url': 'https://github.com/kalaspuff/beautiful',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
