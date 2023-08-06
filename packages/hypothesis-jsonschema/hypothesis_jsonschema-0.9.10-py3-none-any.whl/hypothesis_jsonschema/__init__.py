"""A Hypothesis extension for JSON schemata.

The only public API is `from_schema`; check the docstring for details.
"""

__version__ = "0.9.10"
__all__ = ["from_schema"]

from ._impl import from_schema
