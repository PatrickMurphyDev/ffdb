from typing import Any

import pyarrow as pa

Table = dict[str, list]

def sget(data: dict, *keys: str, default=None) -> Any:
    """Safely get a nested value from a dictionary."""
    val = data
    for key in keys:
        if not isinstance(val, dict) or key not in val:
            return default
        val = val.get(key)
    return val

def buffer(schema: pa.schema) -> dict[str, list]:
    """Creates {'col1': [], 'col2': []} from a pyarrow schema."""
    return {name: [] for name in schema.names}