# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['demo_project']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.0,<3.0']

setup_kwargs = {
    'name': 'demo-project',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Daniel Eitan',
    'author_email': 'daniel.eitan@whitesourcesoftware.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
