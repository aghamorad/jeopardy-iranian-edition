# Historical Engine Architecture: Iranian History Corpus
**Project:** Jeopardy — Iranian Edition  
**Location:** `/Users/Morad/Spark/Jeopardy - Iranian Edition/Docs/HISTORICAL_ENGINE_ARCHITECTURE.md`  
**Date:** 2026-09-09  

---

## 1. Foundational Philosophy

> **"The Language Model provides intelligence. The Local Library provides history."**

In this architecture, the LLM is never used as an ungrounded oracle of historical fact. Pre-trained general models frequently exhibit bias, conflate historical figures (e.g., confusing different Qajar treaties or prime ministers), or adopt simplistic Cold War / Orientalist tropes. 

Every single game clue, accepted alias, explanation, and distractor must be grounded in and verifiable against the **actual corpus of 49 books** residing in `/Users/Morad/Spark/Jeopardy - Iranian Edition`.

---

## 2. Ingestion Pipeline: From Raw Volume to Game Clue

```
                                  [Source Books]
                           48 PDFs + 1 EPUB (Read-Only)
                                        │
                                        ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 1: Detection & Raw Extraction                                         │
 │ • PDFKit native text extraction for 47 files (Instant, lossless)             │
 │ • Apple Vision Framework OCR (`VNRecognizeTextRequest`) for 2 scanned files │
 │ • XML/HTML chapter parser for EPUB (`Abrahamian, The Coup`)                 │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        │
                                        ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 2: Hierarchy & Page-Level Provenance Mapping                          │
 │ • Outline / TOC tree extraction via PDFDocumentOutline                      │
 │ • Running header/footer cleanup                                             │
 │ • Printed-page vs PDF-page calibration table (`page_offset_map`)            │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        │
                                        ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 3: Persian Normalization & Entity Linking                             │
 │ • Dual-text storage: `raw_text` (verbatim) vs `normalized_search_text`     │
 │ • Unicode normalization (NFC/NFKC), ZWNJ (نیم‌فاصله), ی/ي and ک/ك standard  │
 │ • Transliteration harmonizer (Mosaddeq / Mossadegh / Mosaddegh)             │
 │ • Historical title stripper for entity linking (Mirza, Seyyed, Ayatollah)   │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        │
                                        ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 4: Semantic Chunking & Storage                                        │
 │ • Chunks: 300–600 tokens adhering to natural paragraph boundaries          │
 │ • Strict Metadata Envelope:                                                 │
 │   {source_id, chapter, section, printed_page, chunk_index, passage_hash}   │
 │ • Stored in `Corpus/Derived/chunks.jsonl` & SQLite `chunks` table           │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        │
                                        ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 5: Dual-Index Search Engine                                           │
 │ • Lexical Search: SQLite FTS5 (BM25) with custom Persian/English tokenizer  │
 │ • Dense Semantic Search: Local embedded vector store                        │
 │ • Reciprocal Rank Fusion (RRF) combining keyword + semantic retrieval       │
 └──────────────────────────────────────┬──────────────────────────────────────┘
                                        │
                                        ▼
 ┌─────────────────────────────────────────────────────────────────────────────┐
 │ STAGE 6: Clue Extraction, Generation & Strict Validation                    │
 │ • Entity & Fact Extraction (Events, dates, treaties, figures, quotes)       │
 │ • Jeopardy Clue Generation (Question formulation, difficulty tiering)      │
 │ • Distractor Synthesis (Plausible, category-coherent, unambiguous wrong     │
 │   answers for Multiple Choice mode)                                         │
 │ • Fact-Check Validator: Automatic verification of generated clue against    │
 │   source passage before clue is approved                                    │
 └─────────────────────────────────────────────────────────────────────────────┘
```

---

## 3. Persian Text Normalization Protocol

Because Iranian history texts switch between English prose and Persian/Arabic terms, proper nouns, and primary citations, our pipeline maintains **two distinct representations**:

1. **`original_text`**: Untouched verbatim excerpt directly from the source book. This is preserved for user-facing supporting passages and citations.
2. **`normalized_search_text`**: Standardized for exact and fuzzy retrieval:
   - Arabic Yeh (`ي` / `\u064A`) and Persian Yeh (`ی` / `\u06CC`) normalized to standard Persian `ی`.
   - Arabic Kaf (`ك` / `\u0643`) normalized to standard Persian `ک` (`\u06A9`).
   - Zero-Width Non-Joiner (`\u200C` / نیم‌فاصله) handled uniformly.
   - Arabic vs Persian numerals (`١٢٣` vs `۱۲۳` vs `123`) indexed bi-directionally.
   - Diacritical marks (Tashdid, Tanwin, Fatha, Damma, Kasra) stripped in the search index.
   - **Transliteration Aliasing**: Standardizing historical figures across diverse academic romanizations:
     * `Mosaddeq` = `Mosaddegh` = `Mossadegh` = `Musaddiq` = `مصدق`
     * `Nader Shah` = `Nadir Shah` = `Nadir Qoli` = `نادر شاه`
     * `Nasir al-Din Shah` = `Nasser al-Din Shah` = `Nasereddin Shah` = `ناصرالدین شاه`
     * `Reza Shah` = `Riza Shah` = `Reza Khan` = `رضا شاه`
     * `Shari'ati` = `Shariati` = `Ali Shariati` = `علی شریعتی`

---

## 4. Database Schema (`Corpus/Metadata/corpus.db`)

The SQLite database structure guarantees that no clue can exist in isolation from its textual origin:

```sql
-- Sources catalog
CREATE TABLE sources (
    source_id TEXT PRIMARY KEY,
    title TEXT NOT NULL,
    author TEXT NOT NULL,
    editor TEXT,
    publication_year INTEGER,
    language TEXT NOT NULL,
    file_path TEXT NOT NULL,
    relative_path TEXT NOT NULL,
    file_format TEXT NOT NULL,
    file_size_mb REAL,
    page_count INTEGER,
    source_type TEXT,
    primary_or_secondary TEXT,
    historical_period_start INTEGER,
    historical_period_end INTEGER,
    extraction_status TEXT,
    ocr_required BOOLEAN,
    page_mapping_available BOOLEAN,
    ingestion_status TEXT,
    notes TEXT,
    historiographical_stance TEXT
);

-- Text Chunks with Exact Provenance
CREATE TABLE chunks (
    chunk_id TEXT PRIMARY KEY,
    source_id TEXT NOT NULL,
    chapter_title TEXT,
    page_number INTEGER NOT NULL,
    pdf_page_index INTEGER NOT NULL,
    chunk_text_raw TEXT NOT NULL,
    chunk_text_normalized TEXT NOT NULL,
    token_count INTEGER,
    FOREIGN KEY(source_id) REFERENCES sources(source_id)
);

-- Full-Text Search Virtual Table
CREATE VIRTUAL TABLE chunks_fts USING fts5(
    chunk_id UNINDEXED,
    source_id UNINDEXED,
    page_number UNINDEXED,
    chunk_text_normalized,
    tokenize = 'unicode61 remove_diacritics 2'
);

-- Historical Clues with Full Verification Traceability
CREATE TABLE clues (
    clue_id TEXT PRIMARY KEY,
    category TEXT NOT NULL,
    difficulty_tier INTEGER NOT NULL, -- 1: $200 (Easy), 2: $400, 3: $600, 4: $800, 5: $1000 (Very Hard)
    round TEXT NOT NULL,              -- 'jeopardy', 'double_jeopardy', 'final_jeopardy'
    clue_text_en TEXT NOT NULL,
    clue_text_fa TEXT,
    answer_en TEXT NOT NULL,
    answer_fa TEXT,
    accepted_aliases_json TEXT NOT NULL,
    distractors_json TEXT NOT NULL,   -- 3 plausible distractors for MC mode
    explanation TEXT NOT NULL,
    primary_source_id TEXT NOT NULL,
    primary_page INTEGER NOT NULL,
    primary_passage TEXT NOT NULL,
    secondary_source_id TEXT,
    secondary_page INTEGER,
    claim_type TEXT NOT NULL,          -- 'established_fact', 'scholarly_interpretation', 'primary_testimony', 'disputed'
    validation_status TEXT NOT NULL,   -- 'pending', 'verified', 'flagged'
    FOREIGN KEY(primary_source_id) REFERENCES sources(source_id)
);
```

---

## 5. Game Clue Verification State Machine

Before any clue enters the active game pool (`QuestionBank/active_clues.json`):

1. **Extraction:** Model generates candidate clue from a specific retrieved chunk.
2. **Direct Text Grounding Check:** An automated verification check compares the generated `answer` and key factual predicates in `clue_text` against `primary_passage`. If the text does not contain the explicit ground truth, the candidate is **rejected**.
3. **Historical Period & Category Consistency:** The clue's date and theme must strictly align with the source's metadata.
4. **Distractor Quality Audit:** In Multiple Choice mode, distractors must belong to the exact same semantic type (e.g. if the answer is a 19th-century prime minister, all three distractors must be actual 19th-century Iranian political figures, not 20th-century generals or foreign monarchs).
5. **Approved & Signed:** The clue is flagged `verified` with full provenance ready for rendering in the Game Engine and Editorial Inspector.
