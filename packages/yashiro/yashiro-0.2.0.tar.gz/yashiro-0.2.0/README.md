<p align="center">
<a href="https://travis-ci.org/spapanik/yashiro"><img alt="Build" src="https://travis-ci.org/spapanik/yashiro.svg?branch=master"></a>
<a href="https://coveralls.io/github/spapanik/yashiro"><img alt="Coverage" src="https://coveralls.io/repos/github/spapanik/yashiro/badge.svg?branch=master"></a>
<a href="https://github.com/spapanik/yashiro/blob/master/LICENSE.txt"><img alt="License" src="https://img.shields.io/github/license/spapanik/yashiro"></a>
<a href="https://pypi.org/project/yashiro"><img alt="PyPI" src="https://img.shields.io/pypi/v/yashiro"></a>
<a href="https://pepy.tech/project/yashiro"><img alt="Downloads" src="https://pepy.tech/badge/yashiro"></a>
<a href="https://github.com/psf/black"><img alt="Code style" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

# yashiro: A template CLI tool based on jinja

yashiro is just a thin wrapper around jinja

## Installation

The easiest way is to use pip to install yashiro.

```bash
pip install --user yashiro
```

## Usage
yashiro, once installed offers a single command, `yashiro`, that parses the templated based on a JSON file. `punch` follows the GNU recommendations for command line interfaces, and offers:
* `-h` or `--help` to print help, and
* `-V` or `--version` to print the version

You can use punch to parse a template.

```
usage: yashiro [-h] [-j JSON] [-t TEMPLATE] [-V]

optional arguments:
  -h, --help             Show this help message and exit
  -j/--json JSON         The path to the json file
  -t/--template TEMPLATE The path to the template
  -V/--version           Print the version and exit
```
