# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['use_dir']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'use-dir',
    'version': '0.1.4',
    'description': '',
    'long_description': "```python\nfrom use_dir import use_dir\n\nwith use_dir('./bin'):\n    # Do stuff here in the bin directory\n    pass\n\n# We are now back in our starting directory, even if an exception was thrown\n```\n",
    'author': 'Mark Rawls',
    'author_email': 'markrawls96@gmail.com',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
