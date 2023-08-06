# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['livezip']

package_data = \
{'': ['*']}

install_requires = \
['pendulum>=2.0,<3.0']

setup_kwargs = {
    'name': 'livezip',
    'version': '0.1.0',
    'description': 'Memory-bound streamable implementation of ZIP64. Aimed at streaming zips full of multimedia assets (videos, images, etc).',
    'long_description': None,
    'author': 'Rémy Sanchez',
    'author_email': 'remy.sanchez@hyperthese.net',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
