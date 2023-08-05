# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['seedyquay']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'seedy-quay',
    'version': '0.1.0',
    'description': 'Placeholder',
    'long_description': "# seedy-quay\nSeedy Quay. Python extensions for working with Amazon Web Services' Cloud Development Kit\n",
    'author': 'Gary Donovan',
    'author_email': 'gary.donovan@oovvuu.com',
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
