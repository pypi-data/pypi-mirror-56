# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['tablearn']

package_data = \
{'': ['*']}

install_requires = \
['catboost>=0.20.0,<0.21.0',
 'lightgbm>=2.3,<3.0',
 'numpy>=1.17,<2.0',
 'pandas>=0.25.3,<0.26.0',
 'pendulum>=2.0,<3.0',
 'scikit-learn>=0.21.3,<0.22.0',
 'seaborn>=0.9.0,<0.10.0',
 'torch>=1.3,<2.0',
 'torchvision>=0.4.2,<0.5.0',
 'xgboost>=0.90.0,<0.91.0']

setup_kwargs = {
    'name': 'tablearn',
    'version': '0.1.0',
    'description': 'tablearn: Learner for Tabular Data',
    'long_description': None,
    'author': 'yajiez',
    'author_email': 'yajiez.me@gmail.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
