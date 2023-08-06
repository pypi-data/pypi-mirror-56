## Develop config_yourself

`config_yourself` is tested to work with python 2.7, 3.6 and 3.7, so we should make them available before we begin hacking.

`pyenv`, `pipenv`, and `openssl` should be available before installing dependencies.

```sh
# Install the three versions of python we'll be working with
pyenv install
# Install our dev dependencies, and those of config_yourself itself
pipenv install --dev
```

## Running tests

```sh
# run unit and integration tests
pipenv run test

# run multi-python tests
pipenv run tox

# run one test suite
pipenv run pytest -vv tests/unit/ -k TestGPG
```
