# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['et_micc_tools']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0',
 'cmake>=3.15.3,<4.0.0',
 'numpy>=1.17.4,<2.0.0',
 'pybind11>=2.4.3,<3.0.0',
 'tomlkit>=0.5.5,<0.6.0']

entry_points = \
{'console_scripts': ['build = et_micc_tools:cli_build']}

setup_kwargs = {
    'name': 'et-micc-tools',
    'version': '0.0.3',
    'description': '<Enter a one-sentence description of this project here.>',
    'long_description': '=============\net-micc-tools\n=============\n\n\n\n<Enter a one-sentence description of this project here.>\n\n\n* Free software: MIT license\n* Documentation: https://et-micc-tools.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n',
    'author': 'Engelbert Tijskens',
    'author_email': 'engelbert.tijskens@uantwerpen.be',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/etijskens/et-micc-tools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
