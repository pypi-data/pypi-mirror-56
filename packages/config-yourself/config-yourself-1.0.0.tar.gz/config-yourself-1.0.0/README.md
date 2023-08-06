# config-yourself-python

[![CircleCI](https://circleci.com/gh/blinkhealth/config-yourself-python.svg?style=svg)](https://circleci.com/gh/blinkhealth/config-yourself-python)

`config-yourself` is a python 2.7+ package to help your application read [go-config-yourself files](https://github.com/blinkhealth/go-config-yourself#config-files).

---

## Installation

```sh
# choose if you'd like to use `kms`, `gpg` or the `password` provider
pip install 'config_yourself[kms]'

# or go crazy with all of them
pip install 'config_yourself[all]'
```

## Usage

```py
import config_yourself as cy

# Load one config file
encrypted_config = cy.load.file("config/test.yml")
config = cy.Config(encrypted_config)
# now use it like a dict, all secrets have been decrypted
print(config["database"])


# Let's get a little more creative
# `config_yourself` can take a number of config files, merge them,
# and decrypt them

# we start with a defaults file, that defines the valid keys for all subsequent files
# then, we take a file path provided from the environment
files = ['config/defaults.yml', os.environ['CONFIG_FILE']]

# During development, we might choose to have a SCM-ignored personal file, to apply overrides to our personal taste
if os.path.exists(personal_config_path):
  files.append('config/personal.yml')

# we take every file, deserialize it from YAML
configs = [cy.load.file(path) for path in files]
# we can append regular dicts to this list
configs.append({
  'MODE': os.environ.get('BACKEND_MODE', 'tripolar')
})

# we can also decide to override values from the environment...
if os.environ['SHOOT_MYSELF_IN_THE_FOOT']:
  # config_yourself will parse env values as JSON, so this will turn to False
  os.environ['BLINKCONFIG.someService.enabled'] = 'false'
  configs.append(cy.load.env('BLINKCONFIG'))


# Take our list of configs, and pass secrets to the decryption provider
config = cy.Config(*configs, secrets={'password': os.environ['SUPER_SECRET_PASSWORD']})
# The resulting merged config is finally decrypted

print(config['someService']['endpoint']) # => "https://super-secure-service.example.com"
print(config['someService']['enabled']) # => False
```

### From a Django or Flask application

When using in Flask or Django and you'd like to follow the same pattern above,
use the :py:meth:`~config_yourself.AppConfig` method instead:

```py
import config_yourself as bc

config = cy.AppConfig()
# functionally equal to:

# assuming CONFIG_FILE=./config/production.yml
cy.Config(**[
  "./config/defaults.yml",
  "./config/production.yml",
])

# assuming CONFIG_FILE="" and an existing "personal.yml" file
cy.Config(**[
  "./config/defaults.yml",
  "./config/local.yml",
  "./config/personal.yml",
])
```
