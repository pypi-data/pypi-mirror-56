# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['yashiro']

package_data = \
{'': ['*']}

install_requires = \
['jinja2>=2.0,<3.0']

entry_points = \
{'console_scripts': ['yashiro = yashiro.main:write_output']}

setup_kwargs = {
    'name': 'yashiro',
    'version': '0.2.0',
    'description': 'A cli template tool based on jinja',
    'long_description': '<p align="center">\n<a href="https://travis-ci.org/spapanik/yashiro"><img alt="Build" src="https://travis-ci.org/spapanik/yashiro.svg?branch=master"></a>\n<a href="https://coveralls.io/github/spapanik/yashiro"><img alt="Coverage" src="https://coveralls.io/repos/github/spapanik/yashiro/badge.svg?branch=master"></a>\n<a href="https://github.com/spapanik/yashiro/blob/master/LICENSE.txt"><img alt="License" src="https://img.shields.io/github/license/spapanik/yashiro"></a>\n<a href="https://pypi.org/project/yashiro"><img alt="PyPI" src="https://img.shields.io/pypi/v/yashiro"></a>\n<a href="https://pepy.tech/project/yashiro"><img alt="Downloads" src="https://pepy.tech/badge/yashiro"></a>\n<a href="https://github.com/psf/black"><img alt="Code style" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>\n</p>\n\n# yashiro: A template CLI tool based on jinja\n\nyashiro is just a thin wrapper around jinja\n\n## Installation\n\nThe easiest way is to use pip to install yashiro.\n\n```bash\npip install --user yashiro\n```\n\n## Usage\nyashiro, once installed offers a single command, `yashiro`, that parses the templated based on a JSON file. `punch` follows the GNU recommendations for command line interfaces, and offers:\n* `-h` or `--help` to print help, and\n* `-V` or `--version` to print the version\n\nYou can use punch to parse a template.\n\n```\nusage: yashiro [-h] [-j JSON] [-t TEMPLATE] [-V]\n\noptional arguments:\n  -h, --help             Show this help message and exit\n  -j/--json JSON         The path to the json file\n  -t/--template TEMPLATE The path to the template\n  -V/--version           Print the version and exit\n```\n',
    'author': 'spapanik',
    'author_email': 'spapanik21@gmail.com',
    'url': 'https://github.com/spapanik/yashiro',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
