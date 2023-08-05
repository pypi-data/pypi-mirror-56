# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['astboom', 'astboom.visualizers']

package_data = \
{'': ['*']}

install_requires = \
['asciitree>=0.3.3,<0.4.0', 'click>=7.0,<8.0']

entry_points = \
{'console_scripts': ['astboom = astboom.main:cli']}

setup_kwargs = {
    'name': 'astboom',
    'version': '0.2.1',
    'description': 'Visualize Python AST in console.',
    'long_description': "# astboom\n![PyPI](https://img.shields.io/pypi/v/astboom) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/astboom) ![PyPI - Format](https://img.shields.io/pypi/format/astboom) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n\nVisualize Python AST/CST in console using ASCII graphics.\n\nAST is displayed as provided by standard `ast` module, CST is displayed as provided by `lib2to3`.\n\n## Example\n\n![Example usage](https://raw.githubusercontent.com/lensvol/astboom/master/docs/example.png)\n\n## Usage\n\nSimply provide a valid Python source code string as an argument\nand a corresponding AST/CST will be displayed.\n\n```\n# astboom --help\nUsage: astboom [OPTIONS] [SOURCE]\n\nOptions:\n  --ast / --cst  Display source code as AST or CST (default: AST).\n  --no-pos  Hide 'col_offset' and 'lineno' fields.\n  --help    Show this message and exit.\n```\n\nIf no source provided as an argument, then tool will attempt to read it\nfrom *STDIN*.\n\n## Installation\n\n```shell script\n# pip install astboom\n```\n\n## Getting started with development\n\n```shell script\n# git clone https://github.com/lensvol/astboom\n# poetry install --develop\n```\n\n## License\n\nThis project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details\n\n## Authors\n\n* **Kirill Borisov** ([lensvol@gmail.com](mailto:lensvol@gmail.com))\n",
    'author': 'Kirill Borisov',
    'author_email': 'lensvol@gmail.com',
    'url': 'https://github.com/lensvol/astboom',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
