# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['geometry', 'geometry.curve', 'geometry.mesh', 'geometry.shape']

package_data = \
{'': ['*']}

install_requires = \
['attrs>=19.1,<20.0',
 'numpy>=1.16,<2.0',
 'scipy>=1.1,<2.0',
 'triangle>=20190115.3,<20190116.0']

setup_kwargs = {
    'name': 'python-geometry',
    'version': '0.5.0',
    'description': 'Geometry in Python.',
    'long_description': 'python-geometry\n===============\n\nGeometry in Python.\n',
    'author': 'Dominik Steinberger',
    'author_email': 'dominik.steinberger@imfd.tu-freiberg.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
