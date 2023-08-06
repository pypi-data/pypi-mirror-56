# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aws_assume']

package_data = \
{'': ['*']}

install_requires = \
['aws_credential_process>=0.1.0,<0.2.0', 'click==7.0']

entry_points = \
{'console_scripts': ['_assume = aws_assume._assume:main']}

setup_kwargs = {
    'name': 'aws-assume',
    'version': '0.2.1',
    'description': 'AWS session token refreshing daemon',
    'long_description': None,
    'author': 'Dick Marinus',
    'author_email': 'dick@mrns.nl',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
