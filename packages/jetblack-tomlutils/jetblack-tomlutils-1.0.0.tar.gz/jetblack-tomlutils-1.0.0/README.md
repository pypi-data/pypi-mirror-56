# jetblack-tomlutils

Some utilities for working with toml files.

## Usage

Install with pip:

```bash
$ pip install jetblack-tomlutils
```

### toml2json

To convert toml to JSON:

```bash
usage:
    tom2json [<input> [<output]]

    input/output: either a path or '-' for stdin/stdout

examples:
    $ toml2json < pyproject.toml > pyproject.json
    $ toml2json pyproject.toml > pyproject.json
    $ toml2json pyproject.toml - > pyproject.json
    $ toml2json pyproject.toml pyproject.json
    $ cat pyproject.toml | toml2json
    $ cat pyproject.toml | toml2json -
```

### json2toml

To convert JSON to toml:

```bash
usage:
    json2toml [<input> [<output]]

    input/output: either a path or '-' for stdin/stdout

examples:
    $ json2toml < pyproject.json
    $ json2toml pyproject.json
    $ cat pyproject.toml | json2toml
    $ cat pyproject.toml | json2toml -
```

### jsonget

To query JSON

You can query JSON using a [JSON Pointer](https://tools.ietf.org/html/rfc6901)

```bash
usage:
    jsonget <json-pointer> [<input> [<output>]]

    json-pointer: a valid JSON Pointer path
    input/output: either a path or '-' for stdin/stdout

examples:
    $ toml2json pyproject.toml | jsonget /tool/poetry/version
```

### jsonset

To update JSON

You can update JSON using a [JSON Pointer](https://tools.ietf.org/html/rfc6901)
and a value

```bash
usage:
    jsonset <json-pointer> <json-value> [<input> [<output>]]

    json-pointer: a valid JSON Pointer path
    json-value: a value that can be parsed as JSON.
    input/output: either a path or '-' for stdin/stdout


examples:
    $ toml2json pyproject.toml | jsonset /tool/poetry/version '"1.2.3"'
```

## Acknowledgements

This project is a trivial wrapper around the following projects:

* [qtoml](https://github.com/alethiophile/qtoml) - a toml parser
* [jsonpointer](https://github.com/stefankoegl/python-json-pointer) - a JSON pointer package
