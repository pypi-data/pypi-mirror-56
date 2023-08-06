# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['clickshot']

package_data = \
{'': ['*']}

install_requires = \
['mss>=4.0,<5.0',
 'numpy>=1.17,<2.0',
 'opencv-python>=4.1,<5.0',
 'pynput>=1.4,<2.0']

setup_kwargs = {
    'name': 'clickshot',
    'version': '0.4.0',
    'description': 'A framework for easier cross-platform GUI testing.',
    'long_description': '# Clickshot\n\n[![PyPI](https://img.shields.io/pypi/v/clickshot.svg)](https://pypi.python.org/pypi/clickshot)\n[![Build Status](https://travis-ci.com/sneakypete81/clickshot.svg?branch=master)](https://travis-ci.com/sneakypete81/clickshot)\n[![Coverage](https://codecov.io/gh/sneakypete81/clickshot/graph/badge.svg)](https://codecov.io/gh/sneakypete81/clickshot)\n\nA framework for easier cross-platform GUI testing.\n\n## Installation\n\n```sh\npip install clickshot\n```\n\n## Usage\n\nTODO\n\n## Development\n\nRequires [Poetry](https://poetry.eustace.io/).\n\n```sh\ngit clone https://github.com/sneakypete81/clickshot.git\npoetry install\n```\n\nThen you can use the following:\n\n```sh\n  poetry run pytest  # Run all unit tests\n  poetry run flake8  # Run the linter\n  poetry run black . # Run the code autoformatter\n  poetry run tox     # Run all checks across all supported Python versions\n  poetry shell       # Open a venv shell with your local clone installed\n```\n',
    'author': 'sneakypete81',
    'author_email': 'sneakypete81@gmail.com',
    'url': 'https://github.com/sneakypete81/clickshot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
