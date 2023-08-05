# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['coordencode']

package_data = \
{'': ['*']}

install_requires = \
['numpy==1.16.1']

setup_kwargs = {
    'name': 'coordencode',
    'version': '0.0.1',
    'description': 'A library that encodes coordinates so neural networks can use them better.',
    'long_description': 'PCoords\n=======\nNeural Coordinates\n\nInstallation\n------------\nWill be pip installable on first release.',
    'author': 'SimLeek',
    'author_email': 'simulator.leek@gmail.com',
    'url': 'https://github.com/simleek/coordencode',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
