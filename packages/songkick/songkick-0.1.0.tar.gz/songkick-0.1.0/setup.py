# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['songkick']

package_data = \
{'': ['*']}

install_requires = \
['python-dateutil>=2.8,<3.0', 'requests>=2,<3']

setup_kwargs = {
    'name': 'songkick',
    'version': '0.1.0',
    'description': 'A Python SDK for the Songkick API.',
    'long_description': '# Songkick API Python SDK\n\nThis is a Python SDK for the [Songkick API](https://www.songkick.com/developer/).\n',
    'author': 'Craig Anderson',
    'author_email': 'craiga@craiga.id.au',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
