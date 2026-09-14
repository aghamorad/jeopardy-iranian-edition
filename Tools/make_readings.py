#!/usr/bin/env python3
"""Write MAIN's shelf out of the corpus manifest, for the Reading List panel.

Every clue in the bank already carries a `book`, an `author` and a `page`, and the
verdict card prints them under the answer. What the shelf itself *is* — all
forty-nine sources sitting in `Sources/MAIN CORPUS/`, not only the handful a given
board happens to cite — has never been visible anywhere. This is that list.

`Corpus/Metadata/corpus_manifest.json` is the source, and it is the right one: each
entry already knows its title, its author, its year, which shelf folder it lives on,
and a one-line annotation written for exactly this purpose. Nothing here is invented.
The only hand-typed data in this file is the seven bilingual shelf headings, because
the manifest names folders (`3 - Qajar & Constitutional Era (1796-1925)`) and a
reader wants a heading.

Three traps, all answered from the manifest rather than papered over:

**`source_type` is a scholarly classification, not a shelf category.** Forty-five
distinct strings, from `Comprehensive Survey` to `Specialist Monograph / Subaltern
History`, and the panel wants a one-word chip. Pulling the head noun out of them
with a regex is the obvious move and the wrong one — it files
`Primary Source / Court Diaries` and `Specialist Monograph / Political History` under
the same label often enough to be a lie. So the table below is spelled out in full,
and the tool **aborts naming the offender** if the manifest ever carries a
`source_type` it has not been taught. A quiet fallback would mislabel a real book in
front of a real reader, and the manifest will grow.

**Four entries name an editor inside `author`** — `'Stephanie Cronin (editor) and
various contributors'`. That is provenance, not a citation. The parenthetical is
stripped; where the cleaned name turns out to be the editor, `(ed.)` goes back on,
because an edited volume is cited by its editor. Where the recorded "editor" is
really a translator — Khomeini's Algar, Alam's Alikhani — the author stands alone,
since promoting Algar to editor would misstate the book.

**Order is the manifest's, and stays that way.** Within a shelf folder the manifest
is already surname-alphabetical, which is how a bibliography sorts, and it is the
shelf's own order besides. Sorting by the raw author string in here would undo it —
`Abbas Amanat` sorts before `Ervand Abrahamian`, which is the wrong way round.

    python3 Tools/make_readings.py

Writes Web/data/readings.js (window.READINGS_GENERAL). The course shelf has no
manifest at all, so its file is authored rather than generated; see the header in
Web/courses/iran-in-world-politics/data/readings.js.

Deterministic: no randomness, no network, so a rebuild is byte-identical.
"""

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MANIFEST = os.path.join(ROOT, 'Corpus', 'Metadata', 'corpus_manifest.json')
OUT = os.path.join(ROOT, 'Web', 'data', 'readings.js')

GLOBAL = 'READINGS_GENERAL'

# Shelf folder -> (heading en, heading fa), in the order the panel prints them.
# The Persian headings are authored, not derived, and are Morad's to correct.
GROUPS = (
    ('1 - General History (Multi-Era)',
     'General History', 'تاریخ عمومی'),
    ('2 - Safavid, Afsharid & Zand (1501-1796)',
     'Safavid, Afsharid & Zand · 1501–1796', 'صفویه، افشاریه و زندیه · ۱۵۰۱–۱۷۹۶'),
    ('3 - Qajar & Constitutional Era (1796-1925)',
     'Qajar & Constitutional Era · 1796–1925', 'قاجار و عصر مشروطه · ۱۷۹۶–۱۹۲۵'),
    ('4 - Pahlavi Era & Mosaddegh (1925-1979)',
     'Pahlavi Era & Mosaddegh · 1925–1979', 'دوران پهلوی و مصدق · ۱۹۲۵–۱۹۷۹'),
    ('5 - Revolution & Islamic Republic (1979-Present)',
     'Revolution & Islamic Republic · 1979–present',
     'انقلاب و جمهوری اسلامی · ۱۹۷۹–اکنون'),
    ('6 - Biographies & Memoirs',
     'Biographies & Memoirs', 'زندگینامه‌ها و خاطرات'),
    ('7 - Society, Culture & Ideas (Thematic)',
     'Society, Culture & Ideas', 'جامعه، فرهنگ و اندیشه'),
)

# source_type -> the one-word chip the row wears. Total by construction: the tool
# aborts on a source_type that is not a key here, so a manifest addition is a loud
# failure rather than a wrong label.
KIND = {
    'Comprehensive Survey': 'Survey',
    'Comprehensive Survey of Republic': 'Survey',
    'Historical Sociology / Monograph': 'Monograph',
    'Interpretive Survey / Geopolitics of Religion': 'Survey',
    'Longue-durée Survey / Interpretive': 'Survey',
    'Narrative Intellectual & Cultural History': 'Monograph',
    'Political Sociology / Structural Analysis': 'Monograph',
    'Primary Source / Contemporary Chronicle': 'Primary source',
    'Primary Source / Court Diaries': 'Primary source',
    'Primary Source / Memoir': 'Primary source',
    'Primary Source / Memoir in Exile': 'Primary source',
    'Primary Source Collection': 'Primary source',
    'Specialist Biography': 'Biography',
    'Specialist Biography / Administrative History': 'Biography',
    'Specialist Biography / Military History': 'Biography',
    'Specialist Biography / Political History': 'Biography',
    'Specialist Biography / Royal History': 'Biography',
    'Specialist Cultural & Film History': 'Monograph',
    'Specialist Cultural Monograph / Ethnomusicology': 'Monograph',
    'Specialist Cultural Monograph / Gender Theory': 'Monograph',
    'Specialist Edited Volume': 'Edited volume',
    'Specialist Edited Volume / Diplomatic & Intelligence': 'Edited volume',
    'Specialist Ethnography / Media Studies': 'Monograph',
    'Specialist Intellectual Biography': 'Biography',
    'Specialist Intellectual History': 'Monograph',
    'Specialist Monograph': 'Monograph',
    'Specialist Monograph / Architectural History': 'Monograph',
    'Specialist Monograph / Contemporary History': 'Monograph',
    'Specialist Monograph / Diplomatic History': 'Monograph',
    'Specialist Monograph / Gender & State Policy': 'Monograph',
    'Specialist Monograph / Historical Geography': 'Monograph',
    'Specialist Monograph / Historical Sociology': 'Monograph',
    'Specialist Monograph / Institutional Economy': 'Monograph',
    'Specialist Monograph / Intellectual & Religious': 'Monograph',
    'Specialist Monograph / Political Economy': 'Monograph',
    'Specialist Monograph / Political History': 'Monograph',
    'Specialist Monograph / Revisionist Economic': 'Monograph',
    'Specialist Monograph / Revisionist Geopolitical': 'Monograph',
    'Specialist Monograph / Social History': 'Monograph',
    'Specialist Monograph / Subaltern History': 'Monograph',
    'Specialist Monograph / Survey': 'Monograph',
    'Specialist Thematic / Gender & Social': 'Monograph',
    'Specialist Urban Sociology': 'Monograph',
    'Survey / Interpretive': 'Survey',
    'Survey / Interpretive Monograph': 'Survey',
}

CONTRIBUTOR_CRUFT = (' (editor)', ' (editors)',
                     ' and various contributors', ' and contributors')


def clean_author(entry):
    """The name a bibliographic row prints, with the apparatus taken off."""
    author = (entry.get('author') or '').strip()
    for cruft in CONTRIBUTOR_CRUFT:
        author = author.replace(cruft, '')
    author = ' '.join(author.split())

    editor = (entry.get('editor') or '').strip()
    if editor and editor == author:                 # an edited volume
        plural = ',' in editor or '&' in editor
        author = '%s (eds.)' % author if plural else '%s (ed.)' % author
    return author


def kind_of(entry):
    st = entry.get('source_type')
    if st not in KIND:
        sys.exit('source_type not in the table: %r\n'
                 'teach Tools/make_readings.py what chip it wears, then re-run'
                 % st)
    return KIND[st]


def js(value):
    """A JS literal for one value. json.dumps does the escaping, so a title with an
    apostrophe in it -- and four of them have one -- cannot break the file."""
    return json.dumps(value, ensure_ascii=False)


def row(entry):
    parts = ['title: %s' % js(entry['title']),
             'author: %s' % js(clean_author(entry)),
             'year: %s' % (entry['publication_year']
                           if entry.get('publication_year') else 'null'),
             'kind: %s' % js(kind_of(entry))]
    note = ' '.join((entry.get('notes') or '').split())
    if note:
        parts.append('note: %s' % js(note))
    return '    { %s },' % ', '.join(parts)


def main():
    with open(MANIFEST, encoding='utf-8') as fh:
        entries = json.load(fh)

    on_shelf = {e['relative_path'].split('/')[0] for e in entries}
    named = {g[0] for g in GROUPS}
    if on_shelf != named:
        sys.exit('the manifest and the headings disagree: %r'
                 % sorted(on_shelf ^ named))

    out = ['/* MAIN\'s shelf, generated by Tools/make_readings.py from the corpus',
           '   manifest -- do not edit by hand; re-run the tool. */',
           'window.%s = [' % GLOBAL]

    total = 0
    for folder, en, fa in GROUPS:
        items = [e for e in entries if e['relative_path'].startswith(folder + '/')]
        out.append('  { group: { en: %s, fa: %s }, items: [' % (js(en), js(fa)))
        for e in items:
            out.append(row(e))
        out.append('  ] },')
        total += len(items)

    out.append('];')
    out.append('')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out))

    for folder, en, _ in GROUPS:
        n = sum(1 for e in entries if e['relative_path'].startswith(folder + '/'))
        print('%-6s %-46s %2d' % ('', en, n))
    print('%-6s %-46s %2d  ->  %s'
          % ('', 'MAIN', total, os.path.relpath(OUT, ROOT)))
    if total != len(entries):
        sys.exit('wrote %d of %d manifest entries' % (total, len(entries)))


if __name__ == '__main__':
    main()
