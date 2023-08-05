# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['swarm_controller']

package_data = \
{'': ['*']}

install_requires = \
['boto3>=1.10.12,<2.0.0',
 'click>=7.0,<8.0',
 'docker>=4.1.0,<5.0.0',
 'paramiko>=2.6,<3.0',
 'requests>=2.22.0,<3.0.0']

entry_points = \
{'console_scripts': ['swarm-ctl = swarm_controller.core:swarm_ctl']}

setup_kwargs = {
    'name': 'swarm-controller',
    'version': '1.0.4',
    'description': 'Cluster bootstrapping for Docker Swarm on AWS',
    'long_description': '# Swarm Controller\n\n![](https://github.com/jaredvacanti/swarm-controller/workflows/Publish%20to%20PyPI/badge.svg)\n![PyPI](https://img.shields.io/pypi/v/swarm-controller?style=flat-square)\n![PyPI - License](https://img.shields.io/pypi/l/swarm-controller?style=flat-square)\n\nThis is a simple command line program to manage the bootstrapping \nand maintenance of a Docker Swarm Cluster.\n\nCurrently only AWS is supported (requiring access to the \nmetadata service). Eventually we will allow other metadata\nstores like etcd or Consul.\n\n## Installation\n\n```\npip install swarm-controller\n```\n\n## Usage\n\nBootstrap a node:\n```\nswarm-ctl bootstrap\n```\n\nCleanup & Maintenance\n```\nswarm-ctl cleanup\nswarm-ctl relabel\n```\n\n## Tests\n\n```\npoetry run tox\n```\n\n## License\n \nMIT License\n\nCopyright (c) 2019\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.\n',
    'author': 'Jared Vacanti',
    'author_email': 'jaredvacanti@gmail.com',
    'url': 'https://github.com/jaredvacanti/swarm-controller',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
