#!/usr/bin/env python3
"""
Inspect and verify any source book in the Iranian History Corpus.
Usage:
    python3 Tools/inspect_source.py list
    python3 Tools/inspect_source.py show <source_id>
    python3 Tools/inspect_source.py sample <source_id> <page_number>
"""
import sys, os, sqlite3, json

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "Corpus", "Metadata", "corpus.db")

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def list_sources():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT s.source_id, s.title, s.author, s.publication_year, s.page_count, s.extraction_status,
               GROUP_CONCAT(DISTINCT p.period_name) as periods
        FROM sources s
        LEFT JOIN source_periods sp ON s.source_id = sp.source_id
        LEFT JOIN periods p ON sp.period_id = p.period_id
        GROUP BY s.source_id
        ORDER BY s.publication_year ASC
    """)
    rows = cur.fetchall()
    print(f"Total Sources: {len(rows)}\n")
    for r in rows:
        status_flag = "✓" if r["extraction_status"] == "ready" else "⚠ OCR"
        print(f"[{status_flag}] {r['source_id']}")
        print(f"    {r['author']} — {r['title']} ({r['publication_year']}) | {r['page_count']} pp")
        print(f"    Periods: {r['periods']}\n")

def show_source(source_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sources WHERE source_id = ?", (source_id,))
    row = cur.fetchone()
    if not row:
        print(f"Source not found: {source_id}")
        return
    print(f"--- SOURCE DETAILS: {source_id} ---")
    for k in row.keys():
        print(f"{k:>25}: {row[k]}")

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] == "list":
        list_sources()
    elif sys.argv[1] == "show" and len(sys.argv) >= 3:
        show_source(sys.argv[2])
    else:
        print(__doc__)
