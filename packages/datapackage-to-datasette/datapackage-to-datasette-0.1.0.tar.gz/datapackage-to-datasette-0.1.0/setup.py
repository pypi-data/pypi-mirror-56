# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['datapackage_to_datasette']

package_data = \
{'': ['*']}

install_requires = \
['datapackage>=1.10.0,<2.0.0',
 'deepmerge==0.1.0',
 'sqlalchemy>=1.3.0,<2.0.0',
 'tableschema-sql>=1.3.0,<2.0.0']

entry_points = \
{'console_scripts': ['datapackage-to-datasette = '
                     'datapackage_to_datasette.cli:main']}

setup_kwargs = {
    'name': 'datapackage-to-datasette',
    'version': '0.1.0',
    'description': 'Import Frictionless Data Datapackages into SQLite and generate Datasette metadata',
    'long_description': "# datapackage-to-datasette\n\n[![Build Status](https://travis-ci.org/chris48s/datapackage-to-datasette.svg?branch=master)](https://travis-ci.org/chris48s/datapackage-to-datasette)\n[![Coverage Status](https://coveralls.io/repos/github/chris48s/datapackage-to-datasette/badge.svg?branch=master)](https://coveralls.io/github/chris48s/datapackage-to-datasette?branch=master)\n[![PyPI Version](https://img.shields.io/pypi/v/datapackage-to-datasette.svg)](https://pypi.org/project/datapackage-to-datasette/)\n![License](https://img.shields.io/pypi/l/datapackage-to-datasette.svg)\n![Python Support](https://img.shields.io/pypi/pyversions/datapackage-to-datasette.svg)\n![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)\n\nImport Frictionless Data\n[Datapackage](https://frictionlessdata.io/docs/data-package/)s\ninto SQLite and generate\n[Datasette metadata](https://datasette.readthedocs.io/en/stable/metadata.html).\n\n## Setup\n\n```sh\npip install datapackage-to-datasette\n```\n\n## Usage\n\n### On the console\n\nImport a datapackage from a local file\n\n```sh\ndatapackage-to-datasette mydatabase.db /path/to/datapackage.json metadata.json\n```\n\nor from a URL\n\n```sh\ndatapackage-to-datasette mydatabase.db https://pkgstore.datahub.io/core/co2-ppm/10/datapackage.json metadata.json\n```\n\nIf the datasette metadata file already exists, you can pass\n`--write-mode replace` or `--write-mode merge` to overwrite\nor merge with the existing datasette metadata file.\n\n### As a library\n\n```py\nfrom datapackage_to_datasette import datapackage_to_datasette, DataImportError\n\ntry:\n    datapackage_to_datasette(\n        'mydatabase.db',\n        '/path/to/datapackage.json',\n        'metadata.json',\n        write_mode='replace'\n    )\nexcept DataImportError:\n    raise\n```\n",
    'author': 'chris48s',
    'author_email': None,
    'url': 'https://github.com/chris48s/datapackage-to-datasette',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
