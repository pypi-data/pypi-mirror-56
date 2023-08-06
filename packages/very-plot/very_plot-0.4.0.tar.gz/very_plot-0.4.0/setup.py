# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['very_plot']

package_data = \
{'': ['*']}

install_requires = \
['matplotlib>=3.1,<4.0', 'seaborn>=0.9.0,<0.10.0']

setup_kwargs = {
    'name': 'very-plot',
    'version': '0.4.0',
    'description': 'Python plotting tools for Very',
    'long_description': '# very_plot\n\nPython plotting tools for Very\n\n**Free software:** GNU General Public License v3\n\n\n## Installation\n`pip install very_plot`\n\n## Development\n\n\n### Publishing to PyPI\n* `git tag X.X.X; git push origin X.X.X`\n* This tag must match the version in `setup.py` or CI will fail.\n* CI will automatically deploy to PyPI if the build passes.\n',
    'author': 'Jeff McGehee',
    'author_email': 'jeff@verypossible.com',
    'url': 'https://github.com/verypossible/very_plot',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
