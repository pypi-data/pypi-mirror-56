# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['dwys']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'dwys',
    'version': '0.0.3',
    'description': 'A language agnostic doctesting library',
    'long_description': None,
    'author': 'Vince Knight',
    'author_email': 'vincent.knight@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
