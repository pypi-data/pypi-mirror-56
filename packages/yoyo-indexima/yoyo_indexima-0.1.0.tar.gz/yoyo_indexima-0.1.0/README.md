# yoyo-indexima


[![Unix Build Status](https://img.shields.io/travis/geronimo-iia/yoyo-indexima/master.svg?label=unix)](https://travis-ci.org/geronimo-iia/yoyo-indexima)
[![PyPI Version](https://img.shields.io/pypi/v/yoyo-indexima.svg)](https://pypi.org/project/yoyo-indexima)
[![PyPI License](https://img.shields.io/pypi/l/yoyo-indexima.svg)](https://pypi.org/project/yoyo-indexima)

Versions following [Semantic Versioning](https://semver.org/)

## Overview

[Indexima](https://indexima.com/) migration schema based on [yoyo](https://ollycope.com/software/yoyo/latest/) and [pyhive](https://pypi.org/project/PyHive/).


> The little story
>
>In the land of database migration tool, i have tried:
>
>- flyway
>- liquidbase with hive extention
>
>Both either did not support hive (as flyway), or indexima did not fully compliant with hive (wich cause probleme with liquidbase)
>
>So I try to found a module not too complex in order to migrate our indexima schema in a safe way.
>
>In this early release, I just trying to do the job.


## Setup

### Requirements

* Python 3.7+

### Installation

Install this library directly into an activated virtual environment:

```text
$ pip install yoyo-indexima
```

or add it to your [Poetry](https://poetry.eustace.io/) project:

```text
$ poetry add yoyo-indexima
```

## Usage

### Hive connection

1. backend ui must start with ```indexima://```
2. If you have trouble to obtain an hive connection, please read http://dwgeek.com/guide-connecting-hiveserver2-using-python-pyhive.html/

Note: 
If you using python in docker, you should install :
```
apt-get update -qq
apt-get install -qqy gcc libsasl2-dev libsasl2-2 libsasl2-modules-gssapi-mit 
```

## Migration

You could see a complete sample under 'example' folder.


### using python client

```
yoyo_indexima
usage: yoyo_indexima [-h] [-s SOURCE] -u URI {show,apply}
```

example:

```
yoyo_indexima  apply  -s $(pwd)/example/migrations/ -u "indexima://admin:super_password@localhost:10000/default"
```

Commands:

- show                Show migrations
- apply               Apply migrations
- reapply             Reapply migrations
- rollback            Rollback migrations
- mark                Mark migrations as applied, without running them
- unmark              Unmark applied migrations, without rolling them back
- break-lock          Break migration locks


Help for apply:

```bash
> yoyo_indexima  apply -h
usage: yoyo_indexima apply [-h] [-s SOURCE] -u URI [-f] [-a] [-r REVISION]
                           [-d]

optional arguments:
  -h, --help            show this help message and exit
  -s SOURCE, --source SOURCE
                        source path of migration script (default ./migrations)
  -u URI, --uri URI     backend uri
  -f, --force           Force apply/rollback of steps even if previous steps
                        have failed
  -a, --all             Select all migrations, regardless of whether they have
                        been previously applied
  -r REVISION, --revision REVISION
                        Apply/rollback migration with id REVISION
  -d, --dry-run         Dry run: no modification will be applied
```

### within python code

If your migrations script are under directory ```migration``` folder

```python
import os

from yoyo_indexima import get_backend, read_migrations


if __name__ == "__main__":

    # obtain IndeximaBackend
    backend = get_backend('indexima://admin:super_password@localhost:10000/default?auth=CUSTOM')

    # Read migrations folder
    migrations = read_migrations(os.path.join(os.getcwd(), 'migrations/**/*'))
    print(f'migrations: {migrations}')
    if migrations:
        # apply migration
        with backend.lock():
            backend.apply_migrations(backend.to_apply(migrations))
```

### Management table

This tool create in your `default` schema:

- a log table: 'yoyo_log'
- a lock_table: 'yoyo_lock'
- a version table: 'yoyo_version'
- a migration table: 'yoyo_migration'

### Migration script template

```python
"""
{message}
"""

from yoyo import step

__depends__ = {{{depends}}}

steps = [
    step("create ...", "drop ...")
]
```

## License

[The MIT License (MIT)](https://geronimo-iia.github.io/yoyo-indexima/license)


## Contributing

See [Contributing](https://geronimo-iia.github.io/yoyo-indexima/contributing)

## Next step

- production usage in order to see how this tool made the job
- more documentation in code
- purpose few change in 'yoyo' like set all SQL command on Backend class
- ...
