# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['hypermodern_python']

package_data = \
{'': ['*']}

install_requires = \
['click>=7.0,<8.0']

extras_require = \
{'docs': ['sphinx>=2.2.1,<3.0.0',
          'sphinx-rtd-theme>=0.4.3,<0.5.0',
          'sphinx-autodoc-typehints>=1.10.3,<2.0.0']}

entry_points = \
{'console_scripts': ['hypermodern-python = hypermodern_python.console:main']}

setup_kwargs = {
    'name': 'hypermodern-python',
    'version': '0.1.0',
    'description': 'The hypermodern Python project',
    'long_description': '[![tests](https://github.com/cjolowicz/hypermodern-python/workflows/tests/badge.svg)](https://github.com/cjolowicz/hypermodern-python/actions?workflow=tests)\n[![Codecov](https://codecov.io/gh/cjolowicz/hypermodern-python/branch/master/graph/badge.svg)](https://codecov.io/gh/cjolowicz/hypermodern-python)\n[![PyPI](https://img.shields.io/pypi/v/hypermodern-python.svg)](https://pypi.org/project/hypermodern-python/)\n[![Read the Docs](https://readthedocs.org/projects/hypermodern-python/badge/)](https://hypermodern-python.readthedocs.io/)\n\n# hypermodern-python\n',
    'author': 'Claudio Jolowicz',
    'author_email': 'mail@claudiojolowicz.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/cjolowicz/hypermodern-python',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
