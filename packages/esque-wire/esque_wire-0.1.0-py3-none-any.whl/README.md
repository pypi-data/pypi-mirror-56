[![pypi Version](https://img.shields.io/pypi/v/esque-wire.svg)](https://pypi.org/project/esque-wire/)
[![Python Versions](https://img.shields.io/pypi/pyversions/esque-wire.svg)](https://pypi.org/project/esque-wire/)
![Build Status](https://github.com/real-digital/esque-wire/workflows/Style,%20Unit%20And%20Integration%20Tests/badge.svg)
[![Coverage Status](https://coveralls.io/repos/github/real-digital/esque-wire/badge.svg)](https://coveralls.io/github/real-digital/esque-wire)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# esque-wire
A complete and user oriented implementation of the kafka wire protocol.

# Features
## Supports all Api endpoints
Since the code for the API endpoints is automatically generated, this library supports *all* of them.
If a new one comes along, its implementation is just one code execution away. Also the field documentation is extracted
from Kafka source code if there is one.

## Type annotations
Everything is annotated! Enjoy autocomplete all the way to the last field.

```python
# run with mypy
from esque_wire import BrokerConnection, ApiVersionsRequestData

request_data = ApiVersionsRequestData()
connection = BrokerConnection("localhost:9092", "test_client")
response = connection.send(request_data)
reveal_type(response)  # Revealed type is '... AnsweredApiCall[... ApiVersionsRequestData, ... ApiVersionsResponseData]'
reveal_type(response.response_data)  # Revealed type is '... ApiVersionsResponseData*'
```