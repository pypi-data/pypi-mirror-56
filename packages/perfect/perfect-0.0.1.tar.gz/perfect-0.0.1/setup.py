# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['perfect']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'perfect',
    'version': '0.0.1',
    'description': 'The @perfect decorator - a utility library which makes it simpler to create flexible decorators',
    'long_description': '# `perfect`\n[![pypi](https://badge.fury.io/py/perfect.svg)](https://pypi.python.org/pypi/perfect/)\n[![Made with Python](https://img.shields.io/pypi/pyversions/perfect)](https://www.python.org/)\n[![Type hinted - mypy validated](https://img.shields.io/badge/typehinted-yes-teal)](https://github.com/kalaspuff/perfect)\n[![MIT License](https://img.shields.io/github/license/kalaspuff/perfect.svg)](https://github.com/kalaspuff/perfect/blob/master/LICENSE)\n[![Code coverage](https://codecov.io/gh/kalaspuff/perfect/branch/master/graph/badge.svg)](https://codecov.io/gh/kalaspuff/perfect/tree/master/perfect)\n\n*A utility library which makes it simpler to create flexible decorators by just decorating them with the `@perfect` decorator.*\n\n\n## Installation with `pip`\nLike you would install any other Python package, use `pip`, `poetry`, `pipenv` or your weapon of choice.\n```\n$ pip install perfect\n```\n\n\n## Usage and examples\n\n#### `@perfect` decorator\n',
    'author': 'Carl Oscar Aaro',
    'author_email': 'hello@carloscar.com',
    'url': 'https://github.com/kalaspuff/perfect',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
