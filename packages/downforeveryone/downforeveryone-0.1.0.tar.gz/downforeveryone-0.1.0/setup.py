# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['downforeveryone']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['isup = downforeveryone.isup:main']}

setup_kwargs = {
    'name': 'downforeveryone',
    'version': '0.1.0',
    'description': 'checks if a website is really down via isup.me',
    'long_description': "downforeveryone\n======================\n|CIRCLECI| |LICENSE|\n\n.. |CIRCLECI| image:: https://circleci.com/gh/rpdelaney/downforeveryone/tree/master.svg?style=svg\n   :target: https://circleci.com/gh/rpdelaney/downforeveryone/tree/master\n.. |LICENSE| image:: https://img.shields.io/badge/license-Apache%202.0-informational\n   :target: https://www.apache.org/licenses/LICENSE-2.0.txt\n\nChecks if a website is down for everyone or just you, via isup.me.\n\nInstallation\n------------\n\n::\n\n    pip3 install downforeveryone\n\n============\nDevelopment\n============\n\nTo install development dependencies, you will need `poetry <https://docs.pipenv.org/en/latest/>`_\nand `pre-commit <https://pre-commit.com/>`_.\n\n::\n\n    poetry install\n    pre-commit install --install-hooks\n\nUsage\n-----\n\n::\n\n    $ isup -h\n    usage: isup [-h] url\n\n    checks if a site is down for everyone or just you\n\n    positional arguments:\n    url         url to test\n\n    optional arguments:\n    -h, --help  show this help message and exit\n    $ isup google.com ; echo $?\n    just you.\n    1\n    $ isup thingthatsdown.com ; echo $?\n    it's down.\n    0\n",
    'author': 'Ryan Delaney',
    'author_email': 'ryan.delaney@gmail.com',
    'url': 'https://github.com/rpdelaney/isup',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
