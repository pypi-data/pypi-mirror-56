# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['getsubtitle']

package_data = \
{'': ['*']}

install_requires = \
['archi>=0.1.1,<0.2.0',
 'beautifulsoup4>=4.4.0',
 'guessit==3.1.0',
 'requests>=2.0']

entry_points = \
{'console_scripts': ['getsubtitle = getsubtitle.main: main']}

setup_kwargs = {
    'name': 'getsubtitle',
    'version': '2019.11.25',
    'description': 'download subtitles easily',
    'long_description': None,
    'author': 'Wu Haotian',
    'author_email': 'whtsky@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
