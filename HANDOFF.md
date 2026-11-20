# Genius! — Iranian Edition / نابغه! — نسخهٔ ایرانی (`HANDOFF.md`)

**Repo / Working Directory:** `/Volumes/San-C3PO/C3PO/Apps & Games/Jeopardy - Iranian Edition` (`origin/main`)  
**Last Updated:** 2026-11-21 (Gemini)

## Current Verified State
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
  - **Opening-Page Logo Sizing Optimized Across Devices (`Web/styles.css`, `Web/courses/pahlavis/course.css`):**
    - `.boot-logo` (`min(520px, 84vw, 38dvh)`), `.brand-wordmark` (`min(58vw, 760px, 68vh)` desktop/tablet; `min(92vw, 390px)` phone portrait; `min(86vw, 310px)` compact phone), `.logo-hero` (`min(94vw, 430px)` phone portrait incl. Pahlavis override), `.logo-lobby` (`min(90vw, 380px)` phone portrait).
  - **UI, Metadata & Spoken Voice Rebrand:**
    - `Web/index.html`, `Web/i18n.js`, `Web/courses/*/course.js`, `Android/app/src/main/res/values/strings.xml` (`Genius!`), `App/AppMain.swift` (`Genius! — Iranian Edition`), `iOS/JeopardyIOS/Info.plist` & `iOS/project.yml` (`Genius!`), `Web/sidestore/index.html`, `sidestore.json`.
    - Re-cloned 4 spoken Final clips (`stephanie_pahlavis_13_final_jeopardy.m4a`, `stephanie_qajars_13_final_jeopardy.m4a`, `eskandar_13_final_jeopardy.m4a`, `eskandar_30_note_right_3.m4a`) via `mlx-speech` (`fish-s2-pro`) to say **"Final Genius"**.
    - Regenerated `Web/assets/og.jpg` (`1200×630`) and `.github/assets/social-preview.jpg` (`1280×640`) via `Tools/make_og_card.py`.
    - Rebuilt `Web/data/boot_assets.js` (`335` assets, `--check` PASS) and bumped cache-buster `SW_REV = '20261121-genius-1'` in `Web/app.js` and `Web/sw.js`.
- **Previously Merged (AI Studio + 22 Cloned Course Voices):** commit `9f1ab0a` (cross-OS Android/Web UX + 22 `mlx-speech` `fish-s2-pro` clips for `PAHLAVI_WEEKS`, `QAJAR_WEEKS`, `SEMINAR_NOTES`).
- **Visual & Automated Verification:**
  - Verified live screenshots in Obscura headless Chromium across `1440×900` desktop and `390×844` phone in English (`GENIUS!`) and Persian (`نابغه!`) on Front Door and `?ed=pahlavis` (`0` console errors).
  - `Tools/check_bank.py` PASS (0 errors) on all 3 courses; `./verify_all.sh` PASS (12/12 steps, 27/27 Swift & engine tests).

## Notes
- `Sources` and `Versions` in this repo are symlinks to `/Volumes/SanDisk-AI/C3PO-Offload/Jeopardy/...`; when `SanDisk-AI` is not mounted, `git status` shows `D Versions/...` — do not stage those deletions.
- Bundle ID `com.morad.jeopardy` and repo slug `aghamorad/jeopardy-iranian-edition` were intentionally preserved so existing native installs, localStorage saves, and the self-updater stay intact.
