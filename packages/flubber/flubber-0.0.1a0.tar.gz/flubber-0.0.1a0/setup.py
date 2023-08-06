# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flubber',
 'flubber.conf',
 'flubber.conf.project_template',
 'flubber.conf.project_template.apps',
 'flubber.console',
 'flubber.console.commands',
 'flubber.contrib',
 'flubber.contrib.settings',
 'flubber.core',
 'flubber.middleware',
 'flubber.utils']

package_data = \
{'': ['*'], 'flubber.conf.project_template': ['settings/*']}

install_requires = \
['Flask-Opentracing>=1.1,<2.0',
 'cleo>=0.7.6,<0.8.0',
 'factory_boy>=2.12,<3.0',
 'flask-sqlalchemy>=2.4,<3.0',
 'flask>=1.1,<2.0',
 'flask_restful>=0.3.7,<0.4.0',
 'flask_talisman>=0.7.0,<0.8.0',
 'gunicorn>=20.0,<21.0',
 'marshmallow-sqlalchemy>=0.19.0,<0.20.0',
 'omegaconf>=1.4,<2.0',
 'pre-commit>=1.20,<2.0',
 'structlog>=19.2,<20.0',
 'werkzeug>=0.16.0,<0.17.0']

entry_points = \
{'console_scripts': ['flubber = flubber.console:main']}

setup_kwargs = {
    'name': 'flubber',
    'version': '0.0.1a0',
    'description': '',
    'long_description': None,
    'author': 'Dharwin Perez',
    'author_email': 'dhararon@hotmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
