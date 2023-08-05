# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ask_academic_dates']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'ask-academic-dates',
    'version': '0.2.3',
    'description': 'Ask Scholars Portal Academic Date finder',
    'long_description': "# Ask Schools\n\n[\n![PyPI](https://img.shields.io/pypi/v/ask_schools.svg)\n![PyPI](https://img.shields.io/pypi/pyversions/ask_schools.svg)\n![PyPI](https://img.shields.io/github/license/guinslym/ask_schools.svg)\n](https://pypi.org/project/ask_schools/)\n[![TravisCI](https://travis-ci.org/guinslym/ask_schools.svg?branch=master)](https://travis-ci.org/guinslym/ask_schools)\n\n\nThis package helps convert Ask School suffixes to the school full name.\n\n\n## Installation\n\n**Ask Academic Date** can be installed from PyPI using `pip` or your package manager of choice:\n\n```\npip install ask_academic_dates\n```\n\n## Usage\n\n\nExample:\n\n```python\n\nfrom ask_academic_dates import find_academic_year\nfrom datetime import date\n\ndef check_find_academic_year():\n  given_date = date(2019,5,3)\n  result = find_academic_year(given_date)\n  assert result == '2018-2019'\n```\n\n## Code of Conduct\n\nEveryone interacting in the project's codebases, issue trackers, chat rooms, and mailing lists is expected to follow the [PyPA Code of Conduct](https://www.pypa.io/en/latest/code-of-conduct/).",
    'author': 'Guinsly Mondesir',
    'author_email': 'guinslym@gmail.com',
    'url': 'https://github.com/guinslym/ask_academic_dates',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
