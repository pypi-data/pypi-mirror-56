# `crudl`

This repo contains the python module `crudl `.
It is publically available on the python package index as the package `evonik-crudl `.

## Repo Structure

```
crudl/             # source code of crudl
LICENSE            # MIT license file
README.md          # this readme
setup.py           # pypi setup script
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `crudl` as the package `evonik-crudl `.

```bash
pip install evonik-crudl
```

## Usage

```python
from apitest import SqliteDB, MysqlDB

...
```

An example for the use of SqliteDB can be found in [crudl/tet.py](crudl/test.py).

## Test

To test the current implementation, execute the following:

```
pytest crudl/test.py
```

Note that this only tests the SqliteDB wrapper.

## Build & Upload

To build the package and upload a new version to pypi, execute the following commands:

```
rm -rf build dist evonik_crudl.egg-info
python3 setup.py sdist bdist_wheel --universal
twine upload dist/*
```

## Open / Known Issues

- generalization of filter comparators
- add filter operators (and/or/...)

## License
[MIT](https://choosealicense.com/licenses/mit/)
