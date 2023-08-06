# -*- coding: utf-8 -*-
from distutils.core import setup

modules = \
['luxafaret']
install_requires = \
['hidapi>=0.7.0,<0.8.0', 'webcolors>=1.10,<2.0']

entry_points = \
{'console_scripts': ['luxafaret = luxafaret:main']}

setup_kwargs = {
    'name': 'luxafaret',
    'version': '1.0.0',
    'description': '🐍🐑🖍🎨🌈 Luxafåret - colourize your Luxafor flag from Python',
    'long_description': None,
    'author': 'Simon Lundström',
    'author_email': 'github-commits@soy.se',
    'url': None,
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>3.6',
}


setup(**setup_kwargs)
