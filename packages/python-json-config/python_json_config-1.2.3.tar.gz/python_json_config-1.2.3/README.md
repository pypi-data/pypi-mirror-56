[![Build Status](https://travis-ci.com/janehmueller/python-json-config.svg?token=tGKCTy4zTZfGNfjpEgEX&branch=master)](https://travis-ci.com/janehmueller/python-json-config)
![License](https://img.shields.io/pypi/l/python-json-config.svg)
[![Version](https://img.shields.io/pypi/v/python-json-config.svg)](https://pypi.python.org/pypi/python-json-config/)

# Overview
This library allows to load json configs and access the values like members (i.e., `config.server.port`
instead of `config['server']['port']`), validate the data types of fields and transform the values of fields.

# Installing
```
pip install python-json-config
```
# Usage
```
from python_json_config import ConfigBuilder

# create config parser
builder = ConfigBuilder()

# parse config
config = builder.parse_config('path/to/config.json')

# access elements
host = config.server.host
port = config.server.port
myfield = config.myfield
```

## Validate field types
```
builder.validate_field_type('server.ip', str)
builder.validate_field_type('server.port', int)
builder.validate_field_type('jwt.access_token_expires', str)
```

## Validate field values
```
from python_json_config.validators import is_unreserved_port, is_ipv4_address, is_timedelta

# use provided methods
builder.validate_field_value('server.ip', is_ipv4_address)
builder.validate_field_value('server.port', is_unreserved_port)
builder.validate_field_value('jwt.access_token_expires', is_timedelta)

# use custom validation function
builder.validate_field_value('server.ip', lambda ip: ip != '0.0.0.0')

# return custom error messages in your lambda
builder.validate_field_value('server.ip', lambda ip: (ip != '0.0.0.0', 'IP is unroutable.'))

# chain validation functions
builder.validate_field_value('server.ip', [lambda ip: ip != 'localhost', lambda ip: ip != '127.0.0.1'])
```

## Transform field values
```
from python_json_config.transformers import to_timedelta

# use provided methods
builder.transform_field_value('jwt.access_token_expires', to_timedelta)


from datetime import datetime

# parse a timedelta (e.g., Jun 1 2005) into a datetime object
builder.transform_field_value('important_date', lambda date: datetime.strptime(date, '%b %d %Y'))
```

## Define field access settings
```
# required means an error is thrown if a non-existing field is accessed 
builder.set_field_access_required()
# return None for the following fields instead of throwing an error
builder.add_optional_field('server.host')
builder.add_optional_fields(['cache.ttl', 'server.path'])

# optional means None is returned if a non-existing field is accessed 
builder.set_field_access_optional()
# throw an error for the following fields instead of returning None
builder.add_required_field('server.user')
builder.add_required_fields(['cache.backend', 'server.password'])
```

## Access config values
```
port = config.server.port
assert port > 1023

ip = config.server.ip
assert ip not in ['0.0.0.0', 'localhost', '127.0.0.1']

important_date = config.important_date
assert isinstance(important_date, datetime)

jwt_access_token_expires = config.jwt.access_token_expires
assert isinstance(jwt_access_token_expires, timedelta)
```

## Change config values
```
config = ConfigBuilder().parse_config({"server.port": 1024})

config.add("server.host", "localhost")
assert config.server.host == "localhost"

config.add("cache", "redis")
assert config.cache == "redis"

config.update("server.port", 1025)
assert config.server.port == 1025

config.update("server.user", "user", upsert=True)
assert config.server.user == "user"
```

## Overwrite fields with environment variables
First, set environment variables (e.g., via bash):
```
$ MYPROJECT_SERVER_HOST="localhost"
$ MYPROJECT_CACHE="redis"
$ MYPYTHONPROJECTS_USER="user"
```
Escape underscores in names of variables with another underscore:
```
$ MYPYTHONPROJECTS_LOG__FILE="project.log"
```
Then just tell the builder, which prefixes should be merged:
```
builder = ConfigBuilder()
# you can also just pass a single prefix (builder.merge_with_env_variables("MYPROJECT")
builder.merge_with_env_variables(["MYPROJECT", "MYPYTHONPROJECTS"])
config = builder.parse_config({"server.host": "0.0.0.0"})

assert config.server.host == "localhost"
assert config.cache == "redis"
assert config.user == "user"
assert config.log_file == "project.log"
```
Alternatively you can also do the merging after creating the config object:
```
builder = ConfigBuilder()
config = builder.parse_config({"server.host": "0.0.0.0"})
config.merge_with_env_variables(["MYPROJECT", "MYPYTHONPROJECTS"])

assert config.server.host == "localhost"
assert config.cache == "redis"
assert config.user == "user"
```

## Serialization
The config can be serialized to a dictionary, json or binary (via pickle or msgpack).
```
builder = ConfigBuilder()
config = builder.parse_config({"server.host": "0.0.0.0"})

import pickle
pickle_config = pickle.loads(pickle.dumps(config))

dict_config = builder.parse_config(config.to_dict())

import json
json_config = builder.parse_config(config.to_json())

import msgpack
msgpack_config = Config.from_msgpack(config.to_msgpack())
```

**Important note:** serializing via json or msgpack will stringify any non-serializable value (e.g., datetime objects).
