# Jeopardy — Iranian Edition (`HANDOFF.md`)

**Repo / Working Directory:** `/Volumes/San-C3PO/C3PO/Apps & Games/Jeopardy - Iranian Edition` (`origin/main`)  
**Last Updated:** 2026-11-21 (Gemini)

## Current Verified State
- **AI Studio Export Merged & Audited** (from `/Users/Morad/Downloads/jeopardy-iranian-edition-nov-20-2026-4-56-06-pm`):
  - **Merged:**
    - `Android/app/src/main/java/com/morad/jeopardy/MainActivity.java`: responsive viewport (`setUseWideViewPort(true)`, `setLoadWithOverviewMode(true)`), external `http`/`https` links routed via `ACTION_VIEW`, display cutout `LAYOUT_IN_DISPLAY_CUTOUT_MODE_SHORT_EDGES`.
    - `Web/index.html`, `Web/styles.css`, `Web/i18n.js`, `Web/editions.js`, `Web/host-layer.js`, `Web/app.js`: `Tannaz Rosva` host rename, `HostLayer.say()` / `HostLayer.isActive()`, click-to-skip on both host sprite and bubble (`×`), `smartTitleCase()` for English options/answers, podium live/early-lockout/out states, readable clue text floor (`16px`/`18px`), wager slider arrow keys, `Esc`/`X` commentary skip, `webkit.messageHandlers.links` routing, and styled `.more-apps` grid.
    - `Web/sw.js`: merged `SW_REV` (`20261120-live-6`), `SW_UPDATED` client notification, and Network-First HTML/JS/CSS (`isCodeOrDocumentRequest`) while **preserving** `precache()` on `install` for offline first-visit support.
    - `Web/courses/iran-in-world-politics/course.css`, `course.js`, `Web/courses/pahlavis/course.js`, `Web/courses/qajars/course.js`: non-blocking course commentary (`PAHLAVI_WEEKS`, `QAJAR_WEEKS`, `SEMINAR_NOTES`) and `isClueActiveWithoutVerdict()` guard.
  - **Rejected / Preserved from Working Repo:**
    - Kept working repo's `Web/data/clues.js` & `Web/data/clues_fa.js` (AI Studio's copy stripped `period` and `passage` from all 4,167 clues).
    - Kept working repo's `Web/courses/qajars/data/bank-en.js` & `bank-fa.js` (AI Studio's copy reverted 472 alias updates).
    - Excluded AI Studio's wrapper (`server.js`, `server.test.js`, `package.json`, `bun.lock`, `metadata.json`, `public/`, `.aistudio/`) and unreferenced duplicate audio/image assets.
- **22 New Cloned Course Voice Clips (`mlx-speech` `fish-s2-pro`, 48 kHz mono AAC `.m4a`):**
  - **Pahlavis (Dr. Stephanie Cronin):** `stephanie_pahlavis_week1_1921_coup.m4a` .. `stephanie_pahlavis_week8_cold_war.m4a` in `Web/courses/pahlavis/assets/audio/`.
  - **Qajars (Dr. Stephanie Cronin):** `stephanie_qajars_week1_russo_iranian_wars.m4a` .. `stephanie_qajars_week8_women_political_life.m4a` in `Web/courses/qajars/assets/audio/`.
  - **Iran in World Politics (Dr. Eskandar Sadeghi-Boroujerdi):** `eskandar_28_note_right_1.m4a` .. `eskandar_33_note_wrong_3.m4a` in `Web/courses/iran-in-world-politics/assets/audio/`.
  - Wired into `TEXT`, `SOUND`, and `verdict` handlers (plays cloned English voice + transcript in English mode; keeps `HostLayer.say()` caption in Persian mode).
- **Verification:**
  - `Web/data/boot_assets.js` rebuilt (`329` assets, `--check` PASS).
  - `Tools/check_bank.py` PASS (0 errors) on all 3 courses (`iran-in-world-politics`, `qajars`, `pahlavis`).
  - `./verify_all.sh`: **ALL 12 STEPS PASSED** (including 27/27 Swift & engine tests).
  - JavaScriptCore (`jsc`) syntax check PASS on all 8 modified JS files.

## Notes
- `Sources` and `Versions` in this repo are symlinks to `/Volumes/SanDisk-AI/C3PO-Offload/Jeopardy/...`; when `SanDisk-AI` is not mounted, `git status` shows `D Versions/...` — do not stage those deletions.
