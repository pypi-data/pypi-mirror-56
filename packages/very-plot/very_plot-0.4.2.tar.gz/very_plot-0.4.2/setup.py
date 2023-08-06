# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['very_plot']

package_data = \
{'': ['*']}

install_requires = \
['coveralls>=1.8,<2.0',
 'flake8>=3.7,<4.0',
 'matplotlib>=3.1,<4.0',
 'seaborn>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'very-plot',
    'version': '0.4.2',
    'description': 'Python plotting tools for Very',
    'long_description': '# very_plot\n\nPython plotting tools for Very.  The main functionality is styling graphs with a black and white theme.\n\n**Free software:** GNU General Public License v3\n\n## Installation\n`pip install very_plot`\n\n## Usage\n```\nfrom very_plot import themes\nthemes.blog_mpl()\n```\n\nAll plots after this import will follow this theme.\n\n',
    'author': 'Jeff McGehee',
    'author_email': 'jeff@verypossible.com',
    'url': 'https://github.com/verypossible/very_plot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
