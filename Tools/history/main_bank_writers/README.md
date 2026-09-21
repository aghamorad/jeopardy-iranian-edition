# Retired direct writers

These scripts are retained as historical evidence only. They can write the
MAIN archive directly and therefore bypass the supported batch gate, immutable
parts ledger, and derived-file checks. They must never be run in normal work.

The supported replacement is `../../append_batch.py`, followed by the renderers
and `../../check_parts.py` documented in `../../README.md`.
