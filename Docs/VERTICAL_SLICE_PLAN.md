# Playable Vertical Slice Plan: First Milestone
**Project:** Jeopardy — Iranian Edition  
**Location:** `/Users/Morad/Spark/Jeopardy - Iranian Edition/Docs/VERTICAL_SLICE_PLAN.md`  
**Date:** 2026-09-09  

---

## 1. Vertical Slice Philosophy

Per project instructions:
> *"Do not spend days cataloguing books while neglecting the game. Corpus engineering and game development should proceed in parallel. The first playable milestone should use a SMALL SUBSET of the real corpus."*

Rather than stalling gameplay development on bulk-ingesting all 19,783 pages across 49 books, we select **six representative volumes** that together span the entire historical and cultural arc of the project. We ingest these six books with 100% provenance integrity, generate **120 to 180 verified clues**, and deploy them immediately into a fully functional, playable game engine with buzzer controllers, speech recognition, host voice, and scoring.

---

## 2. Selected Vertical Slice Corpus (The "Core Six")

These six books represent diverse historical periods, source types (primary vs secondary), and document formats:

| # | Selected Book | Historical Period | Source Type & Role | Format |
| :- | :--- | :--- | :--- | :--- |
| **1** | **Amanat, *Iran: A Modern History* (2017)** | Safavid to 2000s | **Comprehensive Survey Anchor**: Provides baseline chronology, dynastic transitions, and cultural background. | PDF (Digital text) |
| **2** | **Browne, *The Persian Revolution of 1905–1909* (1910)** | Constitutional Era | **Primary Source Chronicle**: Contemporary eyewitness accounts, telegrams, Sattar Khan, anjomanha, and Majles debates. | PDF (Clean OCR) |
| **3** | **Abrahamian, *The Coup: 1953, the CIA, and the Roots of Modern US-Iranian Relations* (2013)** | Mosaddegh & 1953 | **Specialist Revisionist Monograph**: Clean EPUB structure with embedded print page tags; deep forensic oil data. | EPUB (Semantic) |
| **4** | **Alam, *The Shah and I: Confidential Court Diaries* (1991)** | Late Pahlavi (1969–77) | **Primary Source Court Diary**: Uncensored daily court life, the Shah's private thoughts, OPEC politics, Persepolis gala. | PDF (Clean text) |
| **5** | **Khomeini, *Islam and Revolution* (1981)** | 1963–1980 | **Primary Source Treatise**: Foundational ideological texts: *Velayat-e Faqih*, 1964 Capitulations speech, revolutionary proclamations. | PDF (Clean text) |
| **6** | **Naficy, *A Social History of Iranian Cinema, Vol. 1* (2011)** | Artisanal Era (1897–1941) | **Specialist Cultural History**: Akkas-bashi, royal cinematographers, first cinemas, *Dokhtar-e Lor* (1933), visual culture. | PDF (Clean text) |

---

## 3. Playable Board Category Blueprint (Single & Double Jeopardy)

From these six sources, we construct two standard 30-clue boards (Single Jeopardy and Double Jeopardy) plus Final Jeopardy:

### Single Jeopardy Board ($200 to $1,000)
1. **The Qajar Court**: Nasir al-Din Shah, Amir Kabir, Dar al-Fonun, royal tours (Source: Amanat)
2. **Constitutional Voices**: Anjomanha, the Tabriz resistance, Sattar Khan, the 1907 partition (Source: Browne)
3. **Black Gold & Mosaddegh**: Nationalization, Abadan refinery, National Front, Kermit Roosevelt (Source: Abrahamian)
4. **Court Confidential**: Royal diaries, Asadollah Alam, OPEC price hikes, Persepolis 1971 (Source: Alam)
5. **Cinema Pioneers**: Akkas-bashi, Grand Cinema, *The Lor Girl*, Sepanta, early censorship (Source: Naficy)
6. **Ideology & Resistance**: *Velayat-e Faqih*, 1964 anti-capitulations speech, Qom protests (Source: Khomeini)

### Double Jeopardy Board ($400 to $2,000)
1. **Safavid Splendor**: Shah Abbas I, Isfahan urban plan, Armenian New Julfa silk traders (Source: Amanat)
2. **Mashruteh Press & Satire**: *Sur-e Esrafil*, Dehkhoda’s *Charand-o Parand*, Majles debates (Source: Browne)
3. **Operation Ajax**: Operation Boot, General Zahedi, Tehran radio broadcast, August 19 coup (Source: Abrahamian)
4. **Diplomatic High Wire**: Nixon-Kissinger visits, White Revolution tensions, SAVAK reporting (Source: Alam)
5. **The First Talkies**: Abdolhossein Sepanta, Ardeshir Irani, Imperial Cinema of Tehran (Source: Naficy)
6. **The Crucible of Qom**: Ayatollah Boroujerdi, Hawza theology, Fayziyeh madrasa raid (Source: Khomeini / Mottahedeh)

---

## 4. Vertical Slice Deliverables & Milestones

```
Phase 1: Ingestion of Core Six [CURRENT STEP]
  ├── Programmatic extraction into Corpus/Derived/vertical_slice/
  ├── Verification of page-offset calibration for all 6 sources
  └── Chunking and SQLite FTS5 index build

Phase 2: QuestionBank Generation (120 Sourced Clues)
  ├── 60 Single Jeopardy clues ($200, $400, $600, $800, $1000)
  ├── 60 Double Jeopardy clues ($400, $800, $1200, $1600, $2000)
  ├── 4 Final Jeopardy clues
  └── Validation check ensuring 100% citation completeness

Phase 3: Game Engine Core (Swift / macOS)
  ├── State machine (Board, Buzzers, Clue reveal, Timer, Scoreboard)
  ├── Dual Game Modes:
  │   ├── Classic Jeopardy: Speech recognition buzzer + open voice answer
  │   └── Multiple Choice: 4 options with sourced distractors (keyboard/gamepad)
  ├── Answer Adjudication: Persian & English alias matching with fuzzy scoring
  └── Host Audio: Local text-to-speech synthesis
```
