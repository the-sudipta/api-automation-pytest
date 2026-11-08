"""Validates JSON bodies against the schemas in api_tests/schemas (with $ref between files)."""

import json
from functools import cache
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

SCHEMA_DIR = Path(__file__).parent / "schemas"


@cache
def _registry() -> Registry:
    resources = [
        (path.name, Resource.from_contents(json.loads(path.read_text(encoding="utf-8"))))
        for path in SCHEMA_DIR.glob("*.json")
    ]
    return Registry().with_resources(resources)


def schema_errors(body: object, schema_name: str) -> list[str]:
    """All validation errors (empty list = body follows the contract)."""
    schema = json.loads((SCHEMA_DIR / schema_name).read_text(encoding="utf-8"))
    validator = Draft202012Validator(schema, registry=_registry())
    return [f"{'/'.join(map(str, e.path)) or '<root>'}: {e.message}" for e in validator.iter_errors(body)]
