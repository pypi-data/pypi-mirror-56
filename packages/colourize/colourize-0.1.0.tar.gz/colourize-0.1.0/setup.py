# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['colourize']

package_data = \
{'': ['*']}

install_requires = \
['colour-science==0.3.14',
 'pyyaml>=5.1,<6.0',
 'scikit-image>=0.16.2,<0.17.0',
 'torch>=1.2.0,<2.0.0',
 'torchvision>=0.4.2,<0.5.0',
 'tqdm>=4.39,<5.0']

entry_points = \
{'console_scripts': ['clz = colourize.colourize:main']}

setup_kwargs = {
    'name': 'colourize',
    'version': '0.1.0',
    'description': 'Convert image datasets to other colourspaces.',
    'long_description': '## Colourize\n\n> Convert a dataset of images into many different colourspaces.\n\nA command line tool to preprocess a dataset into many different colourspaces.\nAlso provides a PyTorch `Dataset` that will work on the output and a PyTorch\ntransform to do the conversion online during training instead.\n\n### Currently in alpha this is just a MWE\n',
    'author': 'Derek Goddeau',
    'author_email': 'derek.j.goddeau@pm.me',
    'url': 'https://gitlab.com/starshell/datadyne/colourize',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
