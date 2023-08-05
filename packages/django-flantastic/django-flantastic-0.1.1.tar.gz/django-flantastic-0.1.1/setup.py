# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['flantastic',
 'flantastic.data',
 'flantastic.management',
 'flantastic.migrations',
 'flantastic.tests']

package_data = \
{'': ['*'],
 'flantastic': ['static/flantastic/css/*',
                'static/flantastic/icons/*',
                'static/flantastic/js/*',
                'templates/flantastic/*'],
 'flantastic.management': ['commands/*']}

install_requires = \
['Django>=2.2,<3.0',
 'pandas>=0.25.1,<0.26.0',
 'psycopg2>=2.8,<3.0',
 'requests>=2.22,<3.0',
 'tqdm>=4.36.1,<5.0.0']

setup_kwargs = {
    'name': 'django-flantastic',
    'version': '0.1.1',
    'description': 'GeoDjango app flantastic wich helps to find the best puddings.',
    'long_description': '# flantastic\n\n[![Build Status](https://travis-ci.org/Simarra/django-flantastic.svg?branch=develop)](https://travis-ci.org/Simarra/django-flantastic)\n\nAn app to found the best blank of France!\n',
    'author': 'Loic MARTEL',
    'author_email': None,
    'url': 'https://github.com/Simarra/flantastic',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
