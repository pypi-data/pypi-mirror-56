# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['aeternity']

package_data = \
{'': ['*']}

install_requires = \
['Deprecated>=1.2,<2.0',
 'PyNaCl>=1.3,<2.0',
 'base58>=1.0,<2.0',
 'click>=7.0,<8.0',
 'namedtupled>=0.3.3,<0.4.0',
 'requests>=2.20,<3.0',
 'rlp>=1.1,<2.0',
 'semver>=2.8,<3.0',
 'simplejson>=3.16.0,<4.0.0',
 'validators>=0.13,<0.14',
 'websockets>=7.0,<8.0']

entry_points = \
{'console_scripts': ['aecli = aeternity.__main__:run']}

setup_kwargs = {
    'name': 'aepp-sdk',
    'version': '6.1.0',
    'description': 'Python SDK to interact with the Æternity blockchain',
    'long_description': '# aepp-sdk-python\n\n[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)\n[![Build Status](https://ci.aepps.com/buildStatus/icon?job=aepp-sdk-python/develop)](https://ci.aepps.com/job/aepp-sdk-python/job/develop/)\n[![PyPI version](https://badge.fury.io/py/aepp-sdk.svg)](https://badge.fury.io/py/aepp-sdk)\n[![Language grade: Python](https://img.shields.io/lgtm/grade/python/g/aeternity/aepp-sdk-python.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/aeternity/aepp-sdk-python/context:python)\n[![Documentation Status](https://readthedocs.org/projects/aepp-sdk-python/badge/?version=latest)](https://aepp-sdk-python.readthedocs.io/en/latest/?badge=latest)\n\nWelcome to the [Aeternity](https://aeternity.com) SDK for Python\n\nFor support visit the [forum](https://forum.aeternity.com), for bug reports or feature requests visit open an [issue](https://github.com/aeternity/aepp-sdk-python/issues).\n\n\n### Documentation \n- [Stable](https://aepp-sdk-python.readthedocs.io/en/stable/) for the `master` branch (current release).\n- [Latest](https://aepp-sdk-python.readthedocs.io/en/latest/) for the `develop` branch\n\n### Relevant repositories\n- [Aeternity node](https://github.com/aeternity/aeternity)\n- [Protocol documentation](https://github.com/aeternity/protocol)\n\n### Useful links\n- [Mainnet API Gateway](https://mainnet.aeternity.io/v2/status)\n- [Mainnet frontend and middleware](https://mainnet.aeternal.io) (Aeternal)\n- [Testnet API Gateway](https://mainnet.aeternity.io/v2/status)\n- [Testnet frontend and middleware](https://testnet.aeternal.io) (Aeternal)\n- [Testnet faucet](https://testnet.faucet.aepps.com)\n\n\n\n\n\n',
    'author': 'Andrea Giacobino',
    'author_email': 'no.andrea@gmail.com',
    'url': 'https://github.com/aeternity/aepp-sdk-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
