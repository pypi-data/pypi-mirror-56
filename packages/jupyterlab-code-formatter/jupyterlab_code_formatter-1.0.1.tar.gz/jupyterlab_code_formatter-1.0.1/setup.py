# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jupyterlab_code_formatter']

package_data = \
{'': ['*'], 'jupyterlab_code_formatter': ['tests/*']}

install_requires = \
['jupyterlab>=1.2,<2.0', 'notebook>=6.0,<7.0', 'packaging>=19.2,<20.0']

setup_kwargs = {
    'name': 'jupyterlab-code-formatter',
    'version': '1.0.1',
    'description': 'Server extension to power `@ryantam626/jupyterlab_code_formatter` npm package.',
    'long_description': None,
    'author': 'Ryan Tam',
    'author_email': 'ryantam626@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
