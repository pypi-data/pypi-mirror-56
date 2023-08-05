# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['yoyo_indexima']

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
    'version': '0.0.1',
    'description': 'Indexima migration schema based on yoyo',
    'long_description': '# yoyo-indexima\n\n\n[![Unix Build Status](https://img.shields.io/travis/geronimo-iia/yoyo-indexima/master.svg?label=unix)](https://travis-ci.org/geronimo-iia/yoyo-indexima)\n[![PyPI Version](https://img.shields.io/pypi/v/yoyo-indexima.svg)](https://pypi.org/project/yoyo-indexima)\n[![PyPI License](https://img.shields.io/pypi/l/yoyo-indexima.svg)](https://pypi.org/project/yoyo-indexima)\n\nVersions following [Semantic Versioning](https://semver.org/)\n\n## Overview\n\nIndexima migration schema based on yoyo and pyhive.\n\n\n## Setup\n\n### Requirements\n\n* Python 3.7+\n\n### Installation\n\nInstall this library directly into an activated virtual environment:\n\n```text\n$ pip install yoyo-indexima\n```\n\nor add it to your [Poetry](https://poetry.eustace.io/) project:\n\n```text\n$ poetry add yoyo-indexima\n```\n\n## Usage\n\nYou could see a complete sample under \'example\' folder.\n\nIf your migrations script are under directory ```migration folder```:\n\nNote:\n- If you have trouble to obtain an hive connection, please read http://dwgeek.com/guide-connecting-hiveserver2-using-python-pyhive.html/\n- backend ui must start with ```indexima://```\n\n\n### using python client\n\n```\nusage: yoyo_indexima [-h] [-s SOURCE] -u URI {show,apply}\n```\n\nexample:\n\n```\nyoyo_indexima  apply  -s $(pwd)/example/migrations/ -u "indexima://admin:super_password@localhost:10000/default"\n```\n\n\n### within python code\n\n```python\nimport os\n\nfrom yoyo_indexima import get_backend, read_migrations\n\n\nif __name__ == "__main__":\n\n    # obtain IndeximaBackend\n    backend = get_backend(\'indexima://admin:super_password@localhost:10000/default\')\n\n    # Read migrations folder\n    migrations = read_migrations(os.path.join(os.getcwd(), \'migrations\'))\n    print(f\'migrations: {migrations}\')\n    if migrations:\n        # apply migration\n        with backend.lock():\n            backend.apply_migrations(backend.to_apply(migrations))\n```\n\n\n\n## License\n\n[The MIT License (MIT)](https://geronimo-iia.github.io/yoyo-indexima/license)\n\n\n## Contributing\n\nSee [Contributing](https://geronimo-iia.github.io/yoyo-indexima/contributing)\n\n\n',
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
