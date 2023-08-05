# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pinnwand']

package_data = \
{'': ['*'], 'pinnwand': ['static/*', 'template/*']}

install_requires = \
['click>=7.0,<8.0',
 'pygments>=2.4,<3.0',
 'sqlalchemy>=1.3,<2.0',
 'tornado>=6.0,<7.0']

setup_kwargs = {
    'name': 'pinnwand',
    'version': '0.1.1',
    'description': 'Straightforward pastebin software.',
    'long_description': '.. image:: https://travis-ci.org/supakeen/pinnwand.svg?branch=master\n    :target: https://travis-ci.org/supakeen/pinnwand\n\n.. image:: https://readthedocs.org/projects/pinnwand/badge/?version=latest\n    :target: https://pinnwand.readthedocs.io/en/latest/\n\n.. image:: https://pinnwand.readthedocs.io/en/latest/_static/license.svg\n    :target: https://github.com/supakeen/pinnwand/blob/master/LICENSE\n\n.. image:: https://img.shields.io/badge/code%20style-black-000000.svg\n    :target: https://github.com/ambv/black\n\n\npinnwand\n########\n\n``pinnwand`` is Python pastebin software.\n\nPrerequisites\n=============\n* Python >= 3.6\n* Tornado\n* sqlalchemy\n* click\n* a database driver\n\nUsage\n=====\n\nEnter text, click "Paste". Easy enough.\n\nUsing API is slightly more difficult but certainly recommended for programmatic usage.\n``pinnwand`` accepts HTTP POST requests to ``/json/new`` with following body:\n\n::\n\n    {\n        "code": "text to send",\n        "lexer": "text",\n        "expiry": "1day",\n        "filename": "source.txt"\n    }\n\n``filename`` is optional here.\n\nAPI will return JSON response with full URL for convenience and ``paste_id, removal_id`` keys.\nUse first one to query existing records by GET request to ``/json/show/paste_id``.\n\nTo remove existing paste send POST request to ``/json/remove`` with data\n\n::\n\n    {"removal_id": <removal_id>}\n\n\nReporting bugs\n==============\nBugs are reported best at ``pinnwand``\'s `project page`_ on github.\n\nLicense\n=======\n``pinnwand`` is distributed under a 3-clause BSD-style license. See `LICENSE`\nfor details.\n\n.. _project page: https://github.com/supakeen/pinnwand\n',
    'author': 'supakeen',
    'author_email': 'cmdr@supakeen.com',
    'url': 'https://github.com/supakeen/pinnwand',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4',
}


setup(**setup_kwargs)
