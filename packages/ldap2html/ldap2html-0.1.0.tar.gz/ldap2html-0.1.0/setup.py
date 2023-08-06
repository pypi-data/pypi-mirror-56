# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['ldap2html']

package_data = \
{'': ['*'], 'ldap2html': ['html/*', 'ldap/*']}

install_requires = \
['ldap3>=2.6,<3.0']

entry_points = \
{'console_scripts': ['ldap2html = ldap2html:entrypoint']}

setup_kwargs = {
    'name': 'ldap2html',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'nonylene',
    'author_email': 'nonylene@gmail.com',
    'url': 'https://github.com/nonylene/ldap2html',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
