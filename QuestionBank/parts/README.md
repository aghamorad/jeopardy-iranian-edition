# MAIN bank parts

Each landed MAIN batch is an immutable part recorded in `manifest.json`. The
verified archives are still the materialized bank consumed by the renderers and
the game, but no future batch requires authors to alter or re-review old rows.

The active workflow is:

```bash
python3 Tools/append_batch.py <stem> --dry-run
python3 Tools/append_batch.py <stem>
python3 Tools/render_bank.py
python3 Tools/render_persian_dicts.py
python3 Tools/check_parts.py
```

`append_batch.py` validates only the proposed part directly, while checking it
against the current bank for ID, question-repeat, category-source, citation,
and Persian-calendar conflicts. On a real append it records the two source
files and their SHA-256 digests here. `check_parts.py` proves that each recorded
part is unchanged and still represented exactly in both archives.

Do not edit a recorded incoming pair. A correction is a new, reviewed repair
batch; the old part remains evidence of what was landed. The archive and every
derived play file remain generated artifacts, never hand-edited.
