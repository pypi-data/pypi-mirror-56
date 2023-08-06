# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['padpo', 'padpo.checkers']

package_data = \
{'': ['*']}

install_requires = \
['requests==2.22.0',
 'setuptools==42.0.2',
 'simplelogging==0.10.0',
 'wheel==0.33.6']

entry_points = \
{'console_scripts': ['padpo = padpo.padpo:main']}

setup_kwargs = {
    'name': 'padpo',
    'version': '0.4.0',
    'description': 'Linter for gettext files',
    'long_description': "# padpo\n\nLinter for gettext files (*.po)\n\nCreated to help the translation of official Python docs in French: https://github.com/python/python-docs-fr\n\nIl faut demander aux traducteurs s'ils n'ont pas de pot quand ils traduisent, maintenant ils ont `padpo`…\n:smile: :laughing: :stuck_out_tongue_winking_eye: :joy: (note\xa0: il était tard le soir quand j'ai trouvé le nom).\n\n**WORK IN PROGRESS**\n\n## License\n\nBSD 3-clause\n\nPull request are welcome.\n\n## Usage\n\nUsing the *activated virtual environment* created during the installation:\n\nFor a local input file:\n\n```bash\npadpo --input-path a_file.po\n```\n\nor for a local input directory:\n\n```bash\npadpo --input-path a_directory_containing_po_files\n```\n\nor for a pull request in python-docs-fr repository (here pull request #978)\n\n```bash\npadpo --python-docs-fr 978\n```\n\nor for a pull request in a GitHub repository (here python/python-docs-fr/pull/978)\n\n```bash\npadpo --github python/python-docs-fr/pull/978\n```\n\n![Screenshot](screenshot.png)\n\n## Installation\n\n### Automatic installation\n\n```bash\npip install padpo\n```\n\n### Manual installation\n\n1. Create a virtual environment with Python 3.7 and above\n\n   ```bash\n   python3.7 -m venv venv\n   ```\n\n2. Activate the virtual environment\n\n   ```bash\n   source venv/bin/activate\n   ```\n\n3. Install dependencies\n\n   ```bash\n   poetry install\n   ```\n\n   Note: this uses `poetry` that you can get here: https://poetry.eustace.io/docs/\n\n## Update on PyPI\n\n`./deliver.sh`\n\n## Changelog\n\n### v0.4.0\n\n* use poetry: https://poetry.eustace.io/docs/\n* add some tests with tox and pytests\n* fix some false positive issues with grammalecte\n",
    'author': 'Vincent Poulailleau',
    'author_email': 'vpoulailleau@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/vpoulailleau/padpo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
