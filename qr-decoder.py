#!/usr/bin/env python3

import json
import base64
from datetime import datetime
from typing import Dict, Union

from jsonschema import validate


SCHEMA = {
    "type": "object",
    "properties": {
        "version": {"type": "string", "pattern": r"^alpha$"},
        "payment": {"type": "string", "pattern": r"^(regular|reduced)$"},
        "firstname": {"type": "string", "pattern": r".{1,30}"},
        "lastname": {"type": "string", "pattern": r".{1,30}"},
        "email": {"type": "string", "pattern": r".+@.+\..+"},
        "pgp": {"type": "string", "pattern": r"(0x[a-f0-9]{16}|)"},
        "addr1": {"type": "string", "pattern": r".{1,30}"},
        "addr2": {"type": "string", "pattern": r".{1,30}"},
        "addr3": {"type": "string", "pattern": r".{0,30}"},
        "country": {"type": "string", "pattern": r"[A-Z]{2}"},
        "date": {
            "type": "string",
            "pattern": r"[0-9]{1,2}\.[0-9]{1,2}\.[0-9]{4}"
        },
    },
    "required": [
        "version",
        "payment",
        "firstname",
        "lastname",
        "email",
        "pgp",
        "addr1",
        "addr2",
        "country",
        "date",
    ]
}


class FormDecodeError(Exception):
    pass


def _encode_form(form: Dict[str, str]) -> bytes:
    """Generate qr-code content like value for testing."""
    return base64.b64encode(json.dumps(form).encode())


def decode_form(form_b64: bytes) -> Dict[str, Union[str, datetime]]:
    """Get form data from QRCode.

    This function:
    - decodes the qr-code bytes as utf8 as we expect base64 anyway,
    - decodes the utf8 string as base64,
    - loads the result as json,
    - validates the resulting object against the modules jsonschema SCHEMA,
    - and finally tries to convert the date field into a datetime object

    If anything goes wrong a FormDecodeError is raised, otherwise the form
    data is returned as a dict.
    """
    try:
        form = json.loads(base64.b64decode(form_b64).decode())
        validate(form, SCHEMA)
        form['date_parsed'] = datetime.strptime(form['date'], "%d.%m.%Y")
    except Exception as e:
        raise FormDecodeError(
            "Loading or validation of form failed: {}".format(str(e)))

    return form


def main():
    """Demo how to use this lib"""

    test_form = {
        "version": "alpha",
        "payment": "regular",
        "firstname": "Hannah",
        "lastname": "Acker",
        "email": "h.acker@exmaple.com",
        "pgp": "0x1111111111111111",
        "addr1": "Hauptstraße 1",
        "addr2": "12345 Entenhausen",
        "addr3": "c/o Frank Nord",
        "country": "DE",
        "date": "29.3.2018",
    }

    try:
        form = decode_form(_encode_form(test_form))
        print("Valid Form: {}".format(form))

        test_form['version'] = "foobar"
        form = decode_form(_encode_form(test_form))
    except FormDecodeError as e:
        print("Invalid Form: {}".format(str(e)))


if __name__ == '__main__':
    main()
