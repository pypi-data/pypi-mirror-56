# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'python'}

packages = \
['jaeger',
 'jaeger.actor',
 'jaeger.actor.commands',
 'jaeger.commands',
 'jaeger.core',
 'jaeger.interfaces',
 'jaeger.utils',
 'jaeger.wago']

package_data = \
{'': ['*'], 'jaeger': ['etc/*']}

install_requires = \
['Click>=7.0,<8.0',
 'astropy>=3.0.4,<4.0.0',
 'numpy>=1.15.1,<2.0.0',
 'peewee>=3.11.2,<4.0.0',
 'progressbar2>=3.39.3,<4.0.0',
 'pygments>=2.2.0,<3.0.0',
 'pymodbus>=2.3.0,<3.0.0',
 'pyserial>=3.4,<4.0',
 'python-can>=3.1.1,<4.0.0',
 'ruamel.yaml>=0.15.61,<0.16.0',
 'sdss-clu>=0.1.5,<0.2.0']

extras_require = \
{'docs': ['Sphinx>=1.0,<2.0',
          'releases>=1.6.1,<2.0.0',
          'sphinxcontrib-trio==1.1.0',
          'sphinx-click==2.3.0',
          'semantic-version==2.6.0']}

entry_points = \
{'console_scripts': ['jaeger = jaeger.cli:jaeger']}

setup_kwargs = {
    'name': 'jaeger',
    'version': '0.4.0',
    'description': 'Controllers for the SDSS-V FPS',
    'long_description': 'jaeger\n======\n\n![Versions](https://img.shields.io/badge/python-3.7-blue)\n[![Documentation Status](https://readthedocs.org/projects/jaeger/badge/?version=latest)](https://sdss-jaeger.readthedocs.io/en/latest/?badge=latest)\n[![Travis (.org)](https://img.shields.io/travis/sdss/jaeger)](https://travis-ci.org/sdss/jaeger)\n[![Coverage Status](https://coveralls.io/repos/github/sdss/jaeger/badge.svg?branch=master)](https://coveralls.io/github/sdss/jaeger?branch=master)\n\nPython controller for CAN-based SDSS fibre positioners\n',
    'author': 'José Sánchez-Gallego',
    'author_email': 'gallegoj@uw.edu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sdss/jaeger',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
