# `apitest`

This repo contains the python module `apitest`.
It is publically available on the python package index as the package `evonik-apitest`.

## Repo Structure

```
apitest/           # source code of apitest
examples/          # examples for the use of apitest
notebooks/         # jupyter notebooks with examples and doc
LICENSE            # MIT license file
README.md          # this readme
setup.py           # pypi setup script
```

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install `apitest` as the package `evonik-apitest`.

```bash
pip install evonik-apitest
```

## Usage

```python
from apitest import Property, Properties, Endpoints
from apitest import Component, Instance, ComponentTest
from apitest.util import rand_str, rand_int

...
```

## Test

To test the current implementation, execute the following:

```
pytest \
    apitest/component.py \
    apitest/component_test.py \
    apitest/endpoints.py \
    apitest/instance.py \
    apitest/properties.py \
    apitest/property.py \
    apitest/util.py \
    apitest/test_basic.py
```

## Build & Upload

To build the package and upload a new version to pypi, execute the following commands:

```
rm -rf build dist evonik_apitest.egg-info
python3 setup.py sdist bdist_wheel --universal
twine upload dist/*
```

## License
[MIT](https://choosealicense.com/licenses/mit/)
