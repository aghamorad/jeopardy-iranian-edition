#!/usr/bin/env python3
"""Write MAIN's shelf out of the corpus manifest, for the Reading List panel.

Every clue in the bank already carries a `book`, an `author` and a `page`, and the
verdict card prints them under the answer. What the shelf itself *is* — all
fifty sources sitting in `Sources/MAIN CORPUS/`, not only the handful a given
board happens to cite — has never been visible anywhere. This is that list.

`Corpus/Metadata/corpus_manifest.json` is the source, and it is the right one: each
entry already knows its title, its author, its year, which shelf folder it lives on,
and a one-line annotation written for exactly this purpose. Nothing here is invented.
The only hand-typed data in this file is the eight bilingual shelf headings, because
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

Writes Web/data/readings.js (window.READINGS_GENERAL).

A course shelf has no manifest at all, so its file is authored rather than
generated; see the header in Web/courses/iran-in-world-politics/data/readings.js.
But when a course's bank is absorbed into MAIN (Tools/promote_course_bank.py) its
clues start citing readings that live under `Sources/COURSES/`, and a citation the
player cannot look up defeats the source line — so **the course's readings join
MAIN's shelf**, and this file is what has to learn to read it. `COURSE_SHELVES`
below is the registry; adding a course adds a line to it and nothing else.

They join it **filed under MAIN's own headings**, not under the course's. A week
number is a seminar's clock, and nobody reading MAIN's shelf is sitting in that
seminar: the course's `Week 3 · Factions and elections` is MAIN's `Revolution &
Islamic Republic · 1979–present`, and that is the heading its four articles print
under, after the corpus's own rows. The filing table in `COURSE_SHELVES` is spelled
out week by week — MAIN's eight headings are broad enough that most of a syllabus
lands in one or two of them, and guessing that is worse than reading it — and it
**aborts naming the offender** if the course ever grows a week the table has not
been taught, or if a filed week stops existing. The course's own shelf keeps its
week headings; nothing here writes to it.

Each copied row keeps every key it was authored with — including `src`, the PDF it
came from, which the panel does not read and which is kept anyway because copying a
row means copying all of it. The rows are therefore *not* run through `row()`
below: that function is the corpus's shape, and the course's is its own (`kind`
there is `article`/`chapter`, a seminar's vocabulary, not the corpus's scholarship
chips).

Deterministic: no randomness, no network, so a rebuild is byte-identical.
"""

import json
import os
import subprocess
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
    ('8 - New Additions (2026-09)',
     'New Additions · 2026', 'افزوده‌های تازه · ۲۰۲۶'),
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
    'Primary Source / Political Essay': 'Primary source',
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
    'Specialist Monograph / Media Studies': 'Monograph',
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

# The MAIN headings a course's weeks are allowed to be filed under, named rather
# than spelled out so the table below reads as the decision it is. Each is a folder
# in GROUPS above, and `main()` refuses a filing that names one that is not.
REVOLUTION = '5 - Revolution & Islamic Republic (1979-Present)'
SOCIETY = '7 - Society, Culture & Ideas (Thematic)'
# The Qajar seminar's whole term is the one era, so all eight weeks file here
# rather than spreading week 7 (the Great Game) or week 8 (women) over headings
# MAIN does not have. MAIN's headings are eras, and every row is a Qajar work.
QAJAR = '3 - Qajar & Constitutional Era (1796-1925)'

# Courses whose bank MAIN has absorbed, and whose readings therefore ride along:
# (file, how many readings it must hold, {its group heading: the MAIN folder it is
# filed under}). The count is asserted rather than trusted so a course shelf that
# loses a row is a loud failure here, not a short shelf there, and the filing table
# is asserted in both directions by `main()` — a new week with no filing, or a
# filing with no week, stops the run.
COURSE_SHELVES = (
    ('Web/courses/iran-in-world-politics/data/readings.js', 42, {
        'Week 1 · Revolution and theocracy': REVOLUTION,
        'Week 2 · The Iran–Iraq War': REVOLUTION,
        'Week 3 · Factions and elections': REVOLUTION,
        'Week 4 · The Revolutionary Guards': REVOLUTION,
        'Week 5 · Foreign policy: ideology and pragmatism': REVOLUTION,
        'Week 7 · The Axis of Resistance': REVOLUTION,
        'Week 8 · Sanctions and the domestic economy': REVOLUTION,
        'Week 9 · Gender, the body and the state': SOCIETY,
        'Week 10 · Ethnicity and national identity': SOCIETY,
        'Week 11 · Iran at war since 2023': REVOLUTION,
    }),
    ('Web/courses/qajars/data/readings.js', 85, {
        'Week 1 · The Russo-Persian wars': QAJAR,
        'Week 2 · The ulama & authority': QAJAR,
        'Week 3 · Army reform': QAJAR,
        'Week 4 · Reformist thought': QAJAR,
        'Week 5 · The Tobacco Protest': QAJAR,
        'Week 6 · The Constitutional Revolution': QAJAR,
        'Week 7 · Britain, Russia & the Great Game': QAJAR,
        'Week 8 · Women in political life': QAJAR,
    }),
)

# A course shelf is JS, authored by hand: single-quoted strings, escaped
# apostrophes, bare `null` years. Reading it with a regex would mean writing a
# second and worse implementation of JS string literals, so it is evaluated by
# `node` -- the same reader, for the same reason, as Tools/check_readings.py.
# `window` is the only global these files touch. Exactly one key may land on it.
READER = (
    "const fs=require('fs'),vm=require('vm');"
    "const ctx={window:{}};"
    "vm.createContext(ctx);"
    "vm.runInContext(fs.readFileSync(process.argv[1],'utf8'),ctx,"
    "{filename:process.argv[1]});"
    "const k=Object.keys(ctx.window);"
    "if(k.length!==1){process.stderr.write('expected exactly one window.<GLOBAL> "
    "assignment, saw '+JSON.stringify(k));process.exit(3);}"
    "process.stdout.write(JSON.stringify({name:k[0],value:ctx.window[k[0]]}));"
)


def load_course_shelf(rel):
    """Evaluate one course shelf with `node`: (its global name, its groups)."""
    try:
        out = subprocess.run(['node', '-e', READER, os.path.join(ROOT, rel)],
                             capture_output=True, text=True)
    except FileNotFoundError:
        sys.exit('`node` is not on PATH -- it is what reads %s, which is JS '
                 'rather than data' % rel)
    if out.returncode != 0:
        sys.exit('node could not evaluate %s: %s'
                 % (rel, (out.stderr or out.stdout).strip()))
    try:
        got = json.loads(out.stdout)
    except ValueError:
        sys.exit('node printed something that is not JSON for %s: %r'
                 % (rel, out.stdout[:200]))
    return got['name'], got['value']


def js_value(value):
    """One JS literal. `null` and numbers unquoted, everything else as a string."""
    if value is None:
        return 'null'
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, int):
        return str(value)
    return js(value)


def course_row(item):
    """A course row, copied with every key it was authored with, in its own order.

    Not `row()`: that is the corpus's shape (`kind` is a scholarship chip there and
    a seminar's `article`/`chapter` here), and a copied row keeps its own.
    """
    return '    { %s },' % ', '.join('%s: %s' % (k, js_value(v))
                                     for k, v in item.items())


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


def file_courses():
    """Read each absorbed course shelf, filing its rows under MAIN's headings.

    Returns `(filed, carried)`: `filed` maps a GROUPS folder to a list of
    `(file, its global name, its row lines)` blocks -- one block per course that
    put readings there -- and `carried` is what the run prints. Both directions of
    the filing table are asserted: a course week the table has not been taught, or
    a filing for a week the shelf no longer has, stops the run rather than letting
    a week's readings fall off MAIN's shelf unremarked.
    """
    filed = {folder: [] for folder, _, _ in GROUPS}
    carried = []
    for rel, expected, filing in COURSE_SHELVES:
        name, groups = load_course_shelf(rel)
        n = sum(len(g.get('items') or []) for g in groups)
        if n != expected:
            sys.exit('%s: %d readings under window.%s, expected %d -- the course '
                     'shelf and this registry disagree'
                     % (rel, n, name, expected))

        seen = set()
        blocks = {}
        for gi, g in enumerate(groups):
            head = (g.get('group') or {}).get('en')
            where = '%s group %d' % (rel, gi + 1)
            if head not in filing:
                sys.exit('%s (%r) is filed under no MAIN heading -- teach '
                         'COURSE_SHELVES in Tools/make_readings.py where that '
                         'week belongs' % (where, head))
            folder = filing[head]
            if folder not in filed:
                sys.exit('%s (%r) is filed under %r, which is not one of the '
                         'headings above' % (where, head, folder))
            seen.add(head)
            block = blocks.setdefault(folder, [])
            block.extend(course_row(it) for it in (g.get('items') or []))

        stale = sorted(set(filing) - seen)
        if stale:
            sys.exit('%s: COURSE_SHELVES files %r, which that shelf no longer has '
                     '-- re-read it and drop the stale line'
                     % (rel, stale))

        for folder, lines in blocks.items():
            filed[folder].append((rel, name, lines))
        carried.append((rel, name, n))
    return filed, carried


def main():
    with open(MANIFEST, encoding='utf-8') as fh:
        entries = json.load(fh)

    on_shelf = {e['relative_path'].split('/')[0] for e in entries}
    named = {g[0] for g in GROUPS}
    if on_shelf != named:
        sys.exit('the manifest and the headings disagree: %r'
                 % sorted(on_shelf ^ named))

    filed, carried = file_courses()

    out = ['/* MAIN\'s shelf, generated by Tools/make_readings.py from the corpus',
           '   manifest -- do not edit by hand; re-run the tool. Readings from an',
           "   absorbed course sit under MAIN's own headings, not the course's. */",
           'window.%s = [' % GLOBAL]

    total = 0
    for folder, en, fa in GROUPS:
        items = [e for e in entries if e['relative_path'].startswith(folder + '/')]
        out.append('  { group: { en: %s, fa: %s }, items: [' % (js(en), js(fa)))
        for e in items:
            out.append(row(e))
        for rel, name, lines in filed[folder]:
            out.append('')
            out.append('    /* %d readings from window.%s, the absorbed course '
                       'shelf at' % (len(lines), name))
            out.append('       %s -- filed here by week; the course keeps its own '
                       'week headings. */' % rel)
            out.extend(lines)
        out.append('  ] },')
        total += len(items)

    if total != len(entries):
        sys.exit('wrote %d of %d manifest entries' % (total, len(entries)))

    out.append('];')
    out.append('')

    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as fh:
        fh.write('\n'.join(out))

    folded = 0
    for folder, en, _ in GROUPS:
        n = sum(1 for e in entries if e['relative_path'].startswith(folder + '/'))
        f = sum(len(lines) for _, _, lines in filed[folder])
        folded += f
        print('%-6s %-46s %3d  %s' % ('', en, n, '+ %d filed' % f if f else ''))
    print('%-6s %-46s %3d  MAIN corpus' % ('', '', total))
    for rel, name, n in carried:
        print('%-6s %-46s %3d  filed into those headings -- %s'
              % ('', '', n, rel))
    print('%-6s %-46s %3d  ->  %s'
          % ('', '', total + folded, os.path.relpath(OUT, ROOT)))


if __name__ == '__main__':
    main()
