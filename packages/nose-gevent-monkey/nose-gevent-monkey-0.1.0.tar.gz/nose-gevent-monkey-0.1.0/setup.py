# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['nose_gevent_monkey']
install_requires = \
['nose']

entry_points = \
{'nose.plugins': ['gevent-monkey = nose_gevent_monkey:GeventMonkey']}

setup_kwargs = {
    'name': 'nose-gevent-monkey',
    'version': '0.1.0',
    'description': 'A nose plugin to monkey patch gevent as early as possible',
    'long_description': None,
    'author': 'BCD Trip Tech',
    'author_email': 'development@bcdtriptech.com',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
