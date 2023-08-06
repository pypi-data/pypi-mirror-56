# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pelican_just_table']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.10,<3.0', 'pelican>=4.2,<5.0']

setup_kwargs = {
    'name': 'pelican-just-table',
    'version': '0.1.0',
    'description': 'Just table is a plugin for Pelican to create an easily table.',
    'long_description': None,
    'author': 'Alexandre Bonnetain',
    'author_email': 'Shir0kamii@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
