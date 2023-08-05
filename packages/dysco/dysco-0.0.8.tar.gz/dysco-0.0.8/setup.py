# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dysco']

package_data = \
{'': ['*']}

install_requires = \
['python-slugify>=4.0,<5.0']

setup_kwargs = {
    'name': 'dysco',
    'version': '0.0.8',
    'description': 'Dysco provides configurable dynamic scoping behavior in Python.',
    'long_description': '![Dysco](https://github.com/intoli/dysco/raw/master/media/dysco.png)\n\n<h1 vertical-align="middle">Dysco - Dynamic Scoping in Python\n    <a targe="_blank" href="https://twitter.com/share?url=https%3A%2F%2Fgithub.com%2Fintoli%2Fdysco%2F&text=Dysco%20-%20Configurable%20dynamic%20scoping%20for%20Python">\n        <img height="26px" src="https://simplesharebuttons.com/images/somacro/twitter.png"\n +          alt="Tweet"></a>\n    <a target="_blank" href="https://www.facebook.com/sharer/sharer.php?u=https%3A//github.com/intoli/dysco">\n        <img height="26px" src="https://simplesharebuttons.com/images/somacro/facebook.png"\n            alt="Share on Facebook"></a>\n    <a target="_blank" href="http://reddit.com/submit?url=https%3A%2F%2Fgithub.com%2Fintoli%2Fdysco%2F&title=Dysco%20%E2%80%94%20Configurable%20dynamic%20scoping%20for%20Python">\n        <img height="26px" src="https://simplesharebuttons.com/images/somacro/reddit.png"\n            alt="Share on Reddit"></a>\n    <a target="_blank" href="https://news.ycombinator.com/submitlink?u=https://github.com/intoli/dysco&t=Dysco%20%E2%80%94%20Configurable%20dynamic%20scoping%20for%20Python">\n        <img height="26px" src="https://github.com/intoli/dysco/raw/master/media/ycombinator.png"\n            alt="Share on Hacker News"></a>\n</h1>\n\n<p align="left">\n    <a href="https://circleci.com/gh/intoli/dysco/tree/master">\n        <img src="https://img.shields.io/circleci/project/github/intoli/dysco/master.svg"\n            alt="Build Status"></a>\n    <a href="https://circleci.intoli.com/artifacts/intoli/dysco/coverage-report/index.html">\n        <img src="https://img.shields.io/badge/dynamic/json.svg?label=coverage&colorB=ff69b4&query=$.coverage&uri=https://circleci.intoli.com/artifacts/intoli/dysco/coverage-report/total-coverage.json"\n          alt="Coverage"></a>\n    <a href="https://github.com/intoli/dysco/blob/master/LICENSE.md">\n        <img src="https://img.shields.io/pypi/l/dysco.svg"\n            alt="License"></a>\n    <a href="https://pypi.python.org/pypi/dysco/">\n        <img src="https://img.shields.io/pypi/v/dysco.svg"\n            alt="PyPI Version"></a>\n</p>\n\n###### [Installation](#installation) | [Development](#development) | [Contributing](#contributing)\n\n> Dysco is a lightweight Python library that brings [dynamic scoping](https://en.wikipedia.org/wiki/Scope_(computer_science)#Dynamic_scoping) capabilities to Python in a highly configurable way.\n\n\n## Installation\n\nDysco can be installed from [pypy](https://pypi.org/project/dysco/) using `pip` or any compatible Python package manager.\n\n```bash\n# Installation with pip.\npip install dysco\n\n# Or, installation with poetry.\npoetry add dysco\n```\n\n## Development\n\nTo install the dependencies locally, you need [poetry](https://poetry.eustace.io/docs/#installation) to be installed.\nYou can then run\n\n```bash\n# This is only required if you\'re not using poetry v1.0.0 or greater.\n# It tells poetry to place the virtual environment in `.venv`.\npoetry config settings.virtualenvs.in-project true\n\n# Install all of the dependencies.\npoetry install\n```\n\nto install the project dependencies.\n\nThe library is tested against Python versions 3.7 and 3.8.\nThese are most easily installed using [pyenv](https://github.com/pyenv/pyenv#installation) with the following command.\n\n```bash\n# Install the supported Python versions.\npyenv install --skip-existing 3.7.5\npyenv install --skip-existing 3.8.0\n```\n\nTesting, linting, and document generation can then be run via [tox](https://tox.readthedocs.io/en/latest/).\nThe bare `tox` command will run everything in all environments, or you can break it down by Python version and task.\nFor example, you could run the individual Python 3.8 tasks manually by running the following.\n\n```bash\n# Install the project dependencies in `.tox/py38/`.\ntox -e py38-init\n\n# Run black, flake8, isort, and mypy.\ntox -e py38-lint\n\n# Run the tests and generate a coverage report.\ntox -e py38-test --coverage\n\n## Build the project documentation.\ntox -e py38-docs\n```\n\n## Deployment\n\nYou first need to configure your credentials with poetry.\n\n```bash\npoetry config http-basic.pypi intoli <pypi-password>\n```\n\nYou can then use invoke to bump the version number, commit the changes, tag the version, and deploy to pypi.\n\n```bash\n# Bumps the patch version and deploys the package.\n# Valid options are major, minor, and patch.\ninvoke bump patch\n```\n\n## Contributing\n\nContributions are welcome, but please follow these contributor guidelines outlined in [CONTRIBUTING.md](CONTRIBUTING.md).\n\n\n## License\n\nExodus is licensed under a [BSD 2-Clause License](LICENSE.md) and is copyright [Intoli, LLC](https://intoli.com).\n',
    'author': 'Evan Sangaline',
    'author_email': 'evan@intoli.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/intoli/dysco/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
