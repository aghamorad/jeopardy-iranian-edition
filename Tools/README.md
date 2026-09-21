# Active MAIN-bank tools

Use only these commands for MAIN-bank changes:

```bash
python3 Tools/append_batch.py <stem> --dry-run
python3 Tools/append_batch.py <stem>
python3 Tools/render_bank.py
python3 Tools/render_persian_dicts.py
python3 Tools/check_parts.py
./verify_all.sh
```

`append_batch.py` is the only supported archive writer. It validates a new
English/Persian pair against the current bank, writes it atomically, retains a
backup, and records the immutable part. `render_bank.py` and
`render_persian_dicts.py` are the only supported writers for derived files.

The other Python files are retained historical generators, repairs, and release
notes. They are not part of the current workflow and must not be used to write
`QuestionBank/verified_clues*.json` or `Web/data/clues*.js`.
