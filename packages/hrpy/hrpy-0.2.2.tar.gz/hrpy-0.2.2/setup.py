# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['hrpy']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['hr = hrpy.hr:main']}

setup_kwargs = {
    'name': 'hrpy',
    'version': '0.2.2',
    'description': 'hr but written in python',
    'long_description': 'hrpy\n====\n\n*hr* but in python\n\n--------------\n\nUSAGE\n-----\n\n::\n\n       ~$ hr [STRING]...\n\nEvery argument passed to the program gets multiplied across the length\nof the terminal window\n\n--------------\n\nExample\n-------\n\n::\n\n       ~$ hr - + -\n       ------------------------------------- ...\n       +++++++++++++++++++++++++++++++++++++ ...\n       ------------------------------------- ...\n\n--------------\n\nThe current use I have for this is to make log files less of a mess\n',
    'author': 'John Naylor',
    'author_email': 'jonaylor89@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.0,<4.0',
}


setup(**setup_kwargs)
