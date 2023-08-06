# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pointscan']

package_data = \
{'': ['*']}

install_requires = \
['BAC0>=19.9,<20.0',
 'Flask>=1.1,<2.0',
 'click>=7.0,<8.0',
 'pandas>=0.25.3,<0.26.0',
 'requests>=2.22,<3.0']

entry_points = \
{'console_scripts': ['pointscan = pointscan:scan.main']}

setup_kwargs = {
    'name': 'pointscan',
    'version': '0.1.1',
    'description': 'Library for scanning BACnet points',
    'long_description': None,
    'author': 'Gabe Fierro',
    'author_email': 'gtfierro@cs.berkeley.edu',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
