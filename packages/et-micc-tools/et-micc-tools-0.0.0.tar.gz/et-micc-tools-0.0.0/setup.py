# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['et_micc_tools']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.5.5,<0.6.0']

setup_kwargs = {
    'name': 'et-micc-tools',
    'version': '0.0.0',
    'description': 'Functionality common to et-micc and et-micc-build',
    'long_description': '=============\net-micc-tools\n=============\n\n\n\n<Enter a one-sentence description of this project here.>\n\n\n* Free software: MIT license\n* Documentation: https://et-micc-tools.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n',
    'author': 'Engelbert Tijskens',
    'author_email': 'engelbert.tijskens@uantwerpen.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etijskens/et-micc-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
