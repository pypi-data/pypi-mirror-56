# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['semver', 'tests']

package_data = \
{'': ['*']}

extras_require = \
{':python_version >= "2.7" and python_version < "2.8" or python_version >= "3.4" and python_version < "3.5"': ['typing>=3.6,<4.0']}

setup_kwargs = {
    'name': 'poetry-semver',
    'version': '0.1.0',
    'description': 'A semantic versioning library for Python',
    'long_description': '# Poetry SemVer\n\nA semantic versioning library for Python. Initially part of the [Poetry](https://github.com/python-poetry/poetry) codebase.\n',
    'author': 'Sébastien Eustace',
    'author_email': 'sebastien@eustace.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/python-poetry/semver',
    'packages': packages,
    'package_data': package_data,
    'extras_require': extras_require,
    'python_requires': '>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
}


setup(**setup_kwargs)
