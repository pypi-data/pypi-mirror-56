# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['jetblack_tomlutils']

package_data = \
{'': ['*']}

install_requires = \
['jsonpointer>=2.0,<3.0', 'qtoml>=0.2.4,<0.3.0']

entry_points = \
{'console_scripts': ['json2toml = jetblack_tomlutils.toml_json:json2toml',
                     'jsonget = jetblack_tomlutils.toml_json:jsonget',
                     'jsonset = jetblack_tomlutils.toml_json:jsonset',
                     'toml2json = jetblack_tomlutils.toml_json:toml2json']}

setup_kwargs = {
    'name': 'jetblack-tomlutils',
    'version': '1.0.0',
    'description': 'Utilities for working with toml files',
    'long_description': '# jetblack-tomlutils\n\nSome utilities for working with toml files.\n\n## Usage\n\nInstall with pip:\n\n```bash\n$ pip install jetblack-tomlutils\n```\n\n### toml2json\n\nTo convert toml to JSON:\n\n```bash\nusage:\n    tom2json [<input> [<output]]\n\n    input/output: either a path or \'-\' for stdin/stdout\n\nexamples:\n    $ toml2json < pyproject.toml > pyproject.json\n    $ toml2json pyproject.toml > pyproject.json\n    $ toml2json pyproject.toml - > pyproject.json\n    $ toml2json pyproject.toml pyproject.json\n    $ cat pyproject.toml | toml2json\n    $ cat pyproject.toml | toml2json -\n```\n\n### json2toml\n\nTo convert JSON to toml:\n\n```bash\nusage:\n    json2toml [<input> [<output]]\n\n    input/output: either a path or \'-\' for stdin/stdout\n\nexamples:\n    $ json2toml < pyproject.json\n    $ json2toml pyproject.json\n    $ cat pyproject.toml | json2toml\n    $ cat pyproject.toml | json2toml -\n```\n\n### jsonget\n\nTo query JSON\n\nYou can query JSON using a [JSON Pointer](https://tools.ietf.org/html/rfc6901)\n\n```bash\nusage:\n    jsonget <json-pointer> [<input> [<output>]]\n\n    json-pointer: a valid JSON Pointer path\n    input/output: either a path or \'-\' for stdin/stdout\n\nexamples:\n    $ toml2json pyproject.toml | jsonget /tool/poetry/version\n```\n\n### jsonset\n\nTo update JSON\n\nYou can update JSON using a [JSON Pointer](https://tools.ietf.org/html/rfc6901)\nand a value\n\n```bash\nusage:\n    jsonset <json-pointer> <json-value> [<input> [<output>]]\n\n    json-pointer: a valid JSON Pointer path\n    json-value: a value that can be parsed as JSON.\n    input/output: either a path or \'-\' for stdin/stdout\n\n\nexamples:\n    $ toml2json pyproject.toml | jsonset /tool/poetry/version \'"1.2.3"\'\n```\n\n## Acknowledgements\n\nThis project is a trivial wrapper around the following projects:\n\n* [qtoml](https://github.com/alethiophile/qtoml) - a toml parser\n* [jsonpointer](https://github.com/stefankoegl/python-json-pointer) - a JSON pointer package\n',
    'author': 'Rob Blackbourn',
    'author_email': 'rblackbourn@gmail.com',
    'url': 'https://github.com/rob-blackbourn/jetblack-tomlutils',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
