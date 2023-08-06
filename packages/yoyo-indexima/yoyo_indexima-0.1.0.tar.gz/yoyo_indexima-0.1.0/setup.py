# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['yoyo_indexima', 'yoyo_indexima.cli', 'yoyo_indexima.internalmigrations']

package_data = \
{'': ['*']}

install_requires = \
['PyHive==0.6.1',
 'crayons==0.3.0',
 'thrift-sasl',
 'thrift==0.13.0',
 'yoyo-migrations>=6.1.0,<6.2.0']

entry_points = \
{'console_scripts': ['yoyo_indexima = yoyo_indexima.cli:main']}

setup_kwargs = {
    'name': 'yoyo-indexima',
    'version': '0.1.0',
    'description': 'Indexima migration schema based on yoyo',
    'long_description': '# yoyo-indexima\n\n\n[![Unix Build Status](https://img.shields.io/travis/geronimo-iia/yoyo-indexima/master.svg?label=unix)](https://travis-ci.org/geronimo-iia/yoyo-indexima)\n[![PyPI Version](https://img.shields.io/pypi/v/yoyo-indexima.svg)](https://pypi.org/project/yoyo-indexima)\n[![PyPI License](https://img.shields.io/pypi/l/yoyo-indexima.svg)](https://pypi.org/project/yoyo-indexima)\n\nVersions following [Semantic Versioning](https://semver.org/)\n\n## Overview\n\n[Indexima](https://indexima.com/) migration schema based on [yoyo](https://ollycope.com/software/yoyo/latest/) and [pyhive](https://pypi.org/project/PyHive/).\n\n\n> The little story\n>\n>In the land of database migration tool, i have tried:\n>\n>- flyway\n>- liquidbase with hive extention\n>\n>Both either did not support hive (as flyway), or indexima did not fully compliant with hive (wich cause probleme with liquidbase)\n>\n>So I try to found a module not too complex in order to migrate our indexima schema in a safe way.\n>\n>In this early release, I just trying to do the job.\n\n\n## Setup\n\n### Requirements\n\n* Python 3.7+\n\n### Installation\n\nInstall this library directly into an activated virtual environment:\n\n```text\n$ pip install yoyo-indexima\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add yoyo-indexima\n```\n\n## Usage\n\n### Hive connection\n\n1. backend ui must start with ```indexima://```\n2. If you have trouble to obtain an hive connection, please read http://dwgeek.com/guide-connecting-hiveserver2-using-python-pyhive.html/\n\nNote: \nIf you using python in docker, you should install :\n```\napt-get update -qq\napt-get install -qqy gcc libsasl2-dev libsasl2-2 libsasl2-modules-gssapi-mit \n```\n\n## Migration\n\nYou could see a complete sample under \'example\' folder.\n\n\n### using python client\n\n```\nyoyo_indexima\nusage: yoyo_indexima [-h] [-s SOURCE] -u URI {show,apply}\n```\n\nexample:\n\n```\nyoyo_indexima  apply  -s $(pwd)/example/migrations/ -u "indexima://admin:super_password@localhost:10000/default"\n```\n\nCommands:\n\n- show                Show migrations\n- apply               Apply migrations\n- reapply             Reapply migrations\n- rollback            Rollback migrations\n- mark                Mark migrations as applied, without running them\n- unmark              Unmark applied migrations, without rolling them back\n- break-lock          Break migration locks\n\n\nHelp for apply:\n\n```bash\n> yoyo_indexima  apply -h\nusage: yoyo_indexima apply [-h] [-s SOURCE] -u URI [-f] [-a] [-r REVISION]\n                           [-d]\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -s SOURCE, --source SOURCE\n                        source path of migration script (default ./migrations)\n  -u URI, --uri URI     backend uri\n  -f, --force           Force apply/rollback of steps even if previous steps\n                        have failed\n  -a, --all             Select all migrations, regardless of whether they have\n                        been previously applied\n  -r REVISION, --revision REVISION\n                        Apply/rollback migration with id REVISION\n  -d, --dry-run         Dry run: no modification will be applied\n```\n\n### within python code\n\nIf your migrations script are under directory ```migration``` folder\n\n```python\nimport os\n\nfrom yoyo_indexima import get_backend, read_migrations\n\n\nif __name__ == "__main__":\n\n    # obtain IndeximaBackend\n    backend = get_backend(\'indexima://admin:super_password@localhost:10000/default?auth=CUSTOM\')\n\n    # Read migrations folder\n    migrations = read_migrations(os.path.join(os.getcwd(), \'migrations/**/*\'))\n    print(f\'migrations: {migrations}\')\n    if migrations:\n        # apply migration\n        with backend.lock():\n            backend.apply_migrations(backend.to_apply(migrations))\n```\n\n### Management table\n\nThis tool create in your `default` schema:\n\n- a log table: \'yoyo_log\'\n- a lock_table: \'yoyo_lock\'\n- a version table: \'yoyo_version\'\n- a migration table: \'yoyo_migration\'\n\n### Migration script template\n\n```python\n"""\n{message}\n"""\n\nfrom yoyo import step\n\n__depends__ = {{{depends}}}\n\nsteps = [\n    step("create ...", "drop ...")\n]\n```\n\n## License\n\n[The MIT License (MIT)](https://geronimo-iia.github.io/yoyo-indexima/license)\n\n\n## Contributing\n\nSee [Contributing](https://geronimo-iia.github.io/yoyo-indexima/contributing)\n\n## Next step\n\n- production usage in order to see how this tool made the job\n- more documentation in code\n- purpose few change in \'yoyo\' like set all SQL command on Backend class\n- ...\n',
    'author': 'Jerome Guibert',
    'author_email': 'jguibert@gmail.com',
    'url': 'https://pypi.org/project/yoyo_indexima',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
