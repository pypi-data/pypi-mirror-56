# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['esque_wire',
 'esque_wire.protocol',
 'esque_wire.protocol.serializers',
 'esque_wire.protocol.serializers.api',
 'esque_wire.protocol.structs',
 'esque_wire.protocol.structs.api']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'esque-wire',
    'version': '0.1.0',
    'description': 'A complete implementation of the Kafka API',
    'long_description': '[![pypi Version](https://img.shields.io/pypi/v/esque-wire.svg)](https://pypi.org/project/esque-wire/)\n[![Python Versions](https://img.shields.io/pypi/pyversions/esque-wire.svg)](https://pypi.org/project/esque-wire/)\n![Build Status](https://github.com/real-digital/esque-wire/workflows/Style,%20Unit%20And%20Integration%20Tests/badge.svg)\n[![Coverage Status](https://coveralls.io/repos/github/real-digital/esque-wire/badge.svg)](https://coveralls.io/github/real-digital/esque-wire)\n[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)\n\n# esque-wire\nA complete and user oriented implementation of the kafka wire protocol.\n\n# Features\n## Supports all Api endpoints\nSince the code for the API endpoints is automatically generated, this library supports *all* of them.\nIf a new one comes along, its implementation is just one code execution away. Also the field documentation is extracted\nfrom Kafka source code if there is one.\n\n## Type annotations\nEverything is annotated! Enjoy autocomplete all the way to the last field.\n\n```python\n# run with mypy\nfrom esque_wire import BrokerConnection, ApiVersionsRequestData\n\nrequest_data = ApiVersionsRequestData()\nconnection = BrokerConnection("localhost:9092", "test_client")\nresponse = connection.send(request_data)\nreveal_type(response)  # Revealed type is \'... AnsweredApiCall[... ApiVersionsRequestData, ... ApiVersionsResponseData]\'\nreveal_type(response.response_data)  # Revealed type is \'... ApiVersionsResponseData*\'\n```',
    'author': 'real-digital',
    'author_email': 'opensource@real-digital.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/real.digital/esque-wire',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
