#!/usr/bin/env python3

import json
import base64
from jsonschema import validate
from typing import Dict

SCHEMA = {
    "type": "object",
    "properties": {
        "version": {"type": "string"},
        "payment": {"type": "string"},
        "firstname": {"type": "string"},
        "lastname": {"type": "string"},
        "email": {"type": "string"},
        "pgp": {"type": "string"},
        "addr1": {"type": "string"},
        "addr2": {"type": "string"},
        "addr3": {"type": "string"},
        "c/o": {"type": "string"},
        "country": {"type": "string"},
        "date": {"type": "string"},
    }
}


class FormDecodeError(Exception):
    pass


def encode_form(form: Dict[str, str]) -> bytes:
    return base64.b64encode(json.dumps(form).encode())


def decode_form(form_b64: bytes) -> Dict[str, str]:
    try:
        form = json.loads(base64.b64decode(form_b64).decode())
        validate(form, SCHEMA)
    except Exception as e:
        raise FormDecodeError(
            "Loading or validation of form failed: {}".format(str(e)))

    return form


def main():

    form = {
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

    form = decode_form(encode_form(form))
    print("Valid Form: {}".format(form))

    try:
        form['payment'] = 1
        form = decode_form(encode_form(form))
    except FormDecodeError as e:
        print("Invalid Form: {}".format(str(e)))


if __name__ == '__main__':
    main()
