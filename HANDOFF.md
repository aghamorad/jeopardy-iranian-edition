# Genius! — Iranian Edition / نابغه! — نسخهٔ ایرانی (`HANDOFF.md`)

**Repo / Working Directory:** `/Volumes/HDD-C3PO/Projects/Jeopardy - Iranian Edition` (`origin/main`)  
**Last Updated:** 2026-11-27 (Gemini)

## Current Verified State
- **MAIN Bank Frontier Mega-Expansion (`main-2026-11-frontier`, `4,277` → `6,051` EN+FA rows; +1,884 total new clues with `main-2026-11-popculture`, 2026-11-28):**
  - Landed **1,774 brand-new, source-verified EN+FA mirrored clues (3,548 bilingual entries)** in `QuestionBank/incoming/main-2026-11-frontier-{en,fa}.json` (recorded in `QuestionBank/parts/manifest.json`), mined across **54+ previously unmined frontier books** in `Sources/MAIN CORPUS/` across 9 thematic shards:
    - Music, Pop Culture & Broadcasting (`s01`, 200), Cinema & Visual Arts (`s02`, 200), Gender, Family & Qajar Satire (`s04`, 200), *Shahnameh*, Literature, Translation & Literacy (`s05`, 200), Saljuq/Mongol/Timurid/Safavid & Monetary History (`s06`, 200), Qajar State & Constitutional Revolution (`s07`, 200), Pahlavi Biographies, 1953 Coup & Army (`s08`, 175), 20th-Century Intellectuals & Global 1979 (`s09`, 200), and 1979 Social Origins, Street Politics & Welfare State (`s10`, 200) — minus 1 duplicate final (`s04_final_family_law_revolution`).
  - Combined with `main-2026-11-popculture` (`110` clues), MAIN jumped from **4,167 → 6,051 rows** (`1,298` unique categories in EN and FA) with **0 repeats**, **0 Persian calendar errors**, **0 Latin leaks**, and **zero files touched in `Course/` or `Web/courses/` (locked rule)**.
  - Remaining optional shard if Morad wants to push past 6,250: Shard 03 (`s03_fashion_home_everyday`, ~200 clues from `balasescu`, `karimi`, `hendelman_baavur`, `adelkhah`, `iran_almanac_1971`, `assadi_vidale`) + final 25 clues of `s08`.
- **MAIN Bank Pop-Culture & Cultural History Expansion (`main-2026-11-popculture`, `4,167` → `4,277` EN+FA rows) + Legacy `Jeopardy!` Asset Cleanup (2026-11-27):**
  - Added **110 brand-new, source-verified EN+FA mirrored clues (220 bilingual entries)** to MAIN (`QuestionBank/incoming/main-2026-11-popculture-{en,fa}.json`, recorded in `QuestionBank/parts/manifest.json`): **10 new Single-round categories** (50 clues), **10 new Double-round categories** (50 clues), and **10 new Final Genius clues** (10 clues) — bringing MAIN to **4,277 rows** (`450` single categories, `384` double categories, `107` finals).
  - Every non-final category braids **3–4 distinct corpus books** (max 2 per book) across Iranian music, cinema, Tehrangeles exile TV, broadcasting, fashion, consumer culture, youth/Blogistan, sports/zurkhaneh, *Shahnameh*, press, theatre, and intellectuals — with fresh native Persian wording, explicit calendar markers (`خورشیدی`/`میلادی`), original punny EN & FA category titles, and smug factual host lines. **Zero files in `Course/` or `Web/courses/` were touched (locked rule).**
  - Fixed `Tools/append_batch.py` trailing-newline flag for `verified_clues.json` (`True`), regenerated `Web/data/clues.js`, `Web/data/clues_fa.js`, `QuestionBank/persian_clues.json`, `App/Resources/persian_clues.json`, `QuestionBank/BANK_DIGEST*.md`, and synced `Android/app/src/main/assets/Web/data/`.
  - **GENIUS! / نابغه! Asset Cleanup:** Safely moved old `Jeopardy!` logos/icons/mockups (`Assets/Generated/logo-main-20260918-v1.png`, `icon-main-20260918-v1.png`, `App/Resources/{splash,lobby,board}_reference.png`) and 19 unreferenced legacy assets from `Web/assets/` & `Android/app/src/main/assets/Web/assets/` to `~/.Trash/jeopardy-legacy-assets-20261127/`, shrinking `Web/data/boot_assets.js` from `335` → `316` assets.
  - Cleared stale `/Volumes/San-C3PO/` Swift build cache (`swift package clean`) and verified full `./verify_all.sh`.
- **Release `v2.0.0` (build `2000`) — GENIUS! (نابغه!):**
  - Renamed release bundles, scripts, iOS payload, macOS `.app`, and live host commentary from `Jeopardy` to **`Genius`** (`Genius Iranian Edition.app` / `Genius! Iranian Edition`, `Payload/Genius.app`, `Genius-Iranian-Edition-macOS-universal.zip`, `Genius-Iranian-Edition-iOS.ipa`, `Genius-Iranian-Edition-Android.apk`) while keeping internal upgrade identifiers (`com.morad.jeopardy`, `com.morad.jeopardy-iranian-edition`) intact.
  - Updated `Web/host-layer.js` (EN/FA Double Genius & Final Genius / نابغهٔ پایانی), `build_release.sh`, `run_game.sh`, `build_ipa.sh`, `iOS/project.yml`, `README.md`, `sidestore.json`, `Web/update.js` (`VERSION = '2.0.0'`), `Tools/show_version.sh --build` (`2000`), and `Android/app/build.gradle.kts`.
  - Built & verified `Genius-Iranian-Edition-macOS-universal.zip` (`79,690,115` B, `x86_64 arm64`), unsigned `Genius-Iranian-Edition-iOS.ipa` (`81,153,499` B, `Web/` parity verified), and release-signed `Genius-Iranian-Edition-Android.apk` (`79,070,532` B, v2 signature verified).
- **Rebranded IP (`Jeopardy!` / `جپاردی!` → `GENIUS!` / `نابغه!`):**
  - **All 8 High-Res Transparent Logos Replaced & Bilingual-Synced** (icons `icon-512.png`, `apple-touch-icon.png` kept unchanged):
    - **English (`GENIUS!`):** upscaled 2x from `/Users/Morad/Desktop/New Logos/GENIUS! — English Logo Masters/2026-11-20 — Smoke Easter Egg (Subtle)` in Adobe Photoshop 2026 (`Preserve Details 2.0`), cleaned stray 21px top speck on Main Iranian Edition, saved as RGBA transparent PNGs (`2106–2124 px` wide):
      - `Web/assets/logo-wordmark.png` (`2124 × 950`)
      - `Web/courses/pahlavis/assets/logo-wordmark-course.png` (`2120 × 1012`)
      - `Web/courses/qajars/assets/logo-wordmark-course.png` (`2124 × 987`)
      - `Web/courses/iran-in-world-politics/assets/logo-wordmark-course.png` (`2106 × 1006`)
    - **Persian (`نابغه!`):** extracted from `/Users/Morad/Desktop/New Logos/NABEGHEH — Persian Logo Masters/Nabegheh_Restored_Original_Smoke.png` & `Nabegheh_Pahlavi_Restored_Original_Smoke.png`, fixed Qajar plaque typo (`نشخه قاجار` → `نسخه قاجار`), removed inter-quadrant overlap tips, upscaled in Photoshop 2026 (`Preserve Details 2.0`), and extracted clean halo-free RGBA transparency preserving all Persian letterforms, counters (`ه`), and smoke:
      - `Web/assets/logo-wordmark-fa.png` (`2059 × 742`)
      - `Web/courses/pahlavis/assets/logo-wordmark-course-fa.png` (`2066 × 888`)
      - `Web/courses/qajars/assets/logo-wordmark-course-fa.png` (`1894 × 765`)
      - `Web/courses/iran-in-world-politics/assets/logo-wordmark-course-fa.png` (`1535 × 680`)
  - **Dynamic Bilingual + Edition Logo Switching (`Web/editions.js`, `Web/app.js`, `Web/courses/*/course.js`):** `window.syncEditionLogos()` switches `#boot-logo`, `.brand-wordmark`, and all `.logo` elements dynamically on `editionchange`, `langchange`, and `DOMContentLoaded`.
  - **Opening-Page Zero-Scroll & Cross-Platform Layout Optimization (`Web/styles.css`, `Web/courses/pahlavis/course.css`, `Web/courses/qajars/course.css`, `Web/courses/iran-in-world-politics/course.css`):**
    - Fixed `#app .screen.is-active` `top` resolution (`top: 0;` fallback + `@supports (top: env(safe-area-inset-top, 0px))`) and gave `#app #screen-front.is-active` full `top: 0; bottom: 0; height: auto` (no unused `--host-band` floor cut on the front door).
    - Capped opening logos vertically as well as horizontally (`min(56.8vw, 950px, 72dvh)` for `.logo-hero`, `min(50vw, 820px, 50dvh)` for `.logo-lobby`, `min(56vw, 720px, 46dvh)` for `.brand-wordmark`, plus `pahlavis`/`qajars` `70dvh`/`48dvh` desktop and `38dvh`/`28dvh` phone caps).
    - Converted `#screen-lobby .menu` into a responsive 2-column grid (`#go-setup` spanning full width above a 2×3 secondary grid across desktop, tablet, portrait phone, and landscape phone), centered `#screen-front .circle-row` (`justify-content: safe center;`), and tightened `@media (max-height: 780px) and (min-width: 701px)` and `@media (max-height: 520px) and (orientation: landscape)` spacings so `#screen-front`, `#screen-splash`, and `#screen-lobby` fit cleanly without vertical scrolling on Mac (`1280×720`), laptop, tablet, and phone viewports.
  - **UI, Metadata & Spoken Voice Rebrand:**
    - `Web/index.html`, `Web/i18n.js`, `Web/courses/*/course.js`, `Android/app/src/main/res/values/strings.xml` (`Genius!`), `App/AppMain.swift` (`Genius! — Iranian Edition`), `iOS/JeopardyIOS/Info.plist` & `iOS/project.yml` (`Genius!`), `Web/sidestore/index.html`, `sidestore.json`.
    - Re-cloned 4 spoken Final clips (`stephanie_pahlavis_13_final_jeopardy.m4a`, `stephanie_qajars_13_final_jeopardy.m4a`, `eskandar_13_final_jeopardy.m4a`, `eskandar_30_note_right_3.m4a`) via `mlx-speech` (`fish-s2-pro`) to say **"Final Genius"**.
    - Regenerated `Web/assets/og.jpg` (`1200×630`) and `.github/assets/social-preview.jpg` (`1280×640`) via `Tools/make_og_card.py`.
    - Rebuilt `Web/data/boot_assets.js` (`335` assets, `--check` PASS) and bumped cache-buster `SW_REV = '20261121-genius-2'` in `Web/app.js`, `Web/index.html`, and `Web/sw.js`.
- **Previously Merged (AI Studio + 22 Cloned Course Voices):** commit `9f1ab0a` (cross-OS Android/Web UX + 22 `mlx-speech` `fish-s2-pro` clips for `PAHLAVI_WEEKS`, `QAJAR_WEEKS`, `SEMINAR_NOTES`).
- **Visual & Automated Verification:**
  - Verified live screenshots in Obscura headless Chromium across `1440×900` desktop and `390×844` phone in English (`GENIUS!`) and Persian (`نابغه!`) on Front Door and `?ed=pahlavis` (`0` console errors).
  - `Tools/check_bank.py` PASS (0 errors) on all 3 courses; `./verify_all.sh` PASS (12/12 steps, 27/27 Swift & engine tests).

## Notes
- `Sources/` (`3.5 GB`) and `Versions/` (`beta-1..beta-8`, `v1.0.9..v1.0.17`, plus `v2.0.0`) were consolidated from `/Volumes/San-C3PO/C3PO/C3PO-Offload/Jeopardy Sources` directly into `/Volumes/San-C3PO/C3PO/Apps & Games/Jeopardy - Iranian Edition/` (replacing the old broken `/Volumes/SanDisk-AI/...` symlinks). The empty offload directory and `/Users/Morad/Downloads/jeopardy-iranian-edition-nov-20-2026-4-56-06-pm` were moved to `~/.Trash`.
- Bundle ID `com.morad.jeopardy` and repo slug `aghamorad/jeopardy-iranian-edition` were intentionally preserved so existing native installs, localStorage saves, and the self-updater stay intact.
