/* ── Judging a written answer ───────────────────────────────
   A port of GameEngine/AnswerResolver, so the web build and the native rules
   engine cannot drift apart about who got a clue right, and a contestant who
   learns the game in the browser is not surprised by the app.

   Two steps of the Swift ladder are gone rather than translated: the web bank
   carries `answer` and `aliases` but no `partialAnswers` and no
   `specificityPrompt`, so the two specificity prompts have no data to run on.

   Everything else is here, confusion rules included — those are the half of
   "generous" that keeps it from turning into "gullible". A contestant who
   answers with the father, the son, or the wrong Fazlollah still loses, and
   the host names the mistake instead of shrugging at them.

   The rejection lines come back as i18n keys, not English, so the host's snarl
   survives the language switch. */

(function (window) {
  'use strict';

  // ── Normalization ──────────────────────────────────────────

  /* Arabic look-alikes and the two numeral blocks, so a player typing on an
     Arabic keyboard is not penalised for a letter the Persian keyboard puts
     somewhere else. */
  var CHAR_MAP = {
    'ي': 'ی', // Arabic yeh        → Persian yeh
    'ى': 'ی', // alef maksura      → Persian yeh
    'ك': 'ک', // Arabic kaf        → Persian kaf
    'ۀ': 'ه', // heh with yeh      → heh
    'ة': 'ه', // teh marbuta       → heh
    '۰': '0', '۱': '1', '۲': '2', '۳': '3', '۴': '4',
    '۵': '5', '۶': '6', '۷': '7', '۸': '8', '۹': '9',
    '٠': '0', '١': '1', '٢': '2', '٣': '3', '٤': '4',
    '٥': '5', '٦': '6', '٧': '7', '٨': '8', '٩': '9'
  };

  var DIACRITICS = 'ًٌٍَُِّْٰٔ';

  /* Honorifics that carry no historical identity. "Dr. Mossadegh" and
     "Mossadegh" are the same answer; "Dr." alone is not an answer at all. */
  var HONORIFICS = ['dr.', 'dr', 'doctor', 'دکتر', 'دكتر', 'آقای', 'اقای', 'mr.', 'mr'];

  function stripAccents(s) {
    return s.normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  }

  function normalize(input, stripDisposable) {
    var text = String(input == null ? '' : input).normalize('NFC');
    var out = '';

    for (var i = 0; i < text.length; i++) {
      var ch = text[i];
      if (DIACRITICS.indexOf(ch) !== -1) continue;
      if (CHAR_MAP[ch] != null) { out += CHAR_MAP[ch]; continue; }
      if (ch === '‌') { out += ' '; continue; }   // ZWNJ reads as a space
      out += ch;
    }

    // Letters and digits only — the same whitelist the Swift normalizer builds
    // from CharacterSet.alphanumerics, which also drops Arabic combining marks.
    out = out.replace(/[^\p{L}\p{N}\s]/gu, '').toLowerCase();
    out = stripAccents(out);

    var words = out.split(/\s+/).filter(function (w) { return w.length > 0; });

    if (stripDisposable) {
      while (words.length && HONORIFICS.indexOf(words[0]) !== -1) words.shift();
    }

    return words.join(' ');
  }

  /* Persian names have several equally reasonable Latin spellings — q/gh,
     kh/x, i/y, ou/u, doubled letters. The key collapses them so "Mossadegh"
     and "Musaddiq" land on the same string. Non-Latin input is returned
     space-stripped and untouched: the replacement chain is written for Latin
     orthography and would mangle Persian. */
  function phoneticKey(text) {
    var value = stripAccents(String(text).toLowerCase());
    var ascii = true;
    for (var i = 0; i < value.length; i++) if (value.charCodeAt(i) > 127) { ascii = false; break; }
    if (!ascii) return value.replace(/ /g, '');

    var pairs = [
      ['tch', 'c'], ['ch', 'c'], ['kh', 'x'], ['gh', 'q'], ['zh', 'j'],
      ['sh', 's'], ['ph', 'f'], ['ou', 'u'], ['ow', 'u'], ['oo', 'u'],
      ['ee', 'i'], ['aa', 'a'], ['q', 'q'], ['y', 'i']
    ];
    for (var p = 0; p < pairs.length; p++) {
      value = value.split(pairs[p][0]).join(pairs[p][1]);
    }

    value = value.replace(/[^a-z0-9]/g, '').replace(/([a-z])\1+/g, '$1');
    if (value.slice(-2) === 'eh') value = value.slice(0, -2) + 'e';
    return value;
  }

  function levenshtein(a, b) {
    var s1 = Array.from(a), s2 = Array.from(b);
    var last = [];
    for (var j = 0; j <= s2.length; j++) last.push(j);

    for (var i = 0; i < s1.length; i++) {
      var cur = [i + 1];
      for (var k = 1; k <= s2.length; k++) {
        cur[k] = s1[i] === s2[k - 1] ? last[k - 1] : Math.min(last[k - 1], last[k], cur[k - 1]) + 1;
      }
      last = cur;
    }
    return last[s2.length];
  }

  function similarity(a, b) {
    var maxLen = Math.max(a.length, b.length);
    if (maxLen === 0) return 1;
    return 1 - levenshtein(a, b) / maxLen;
  }

  /* The clusters worth spelling more than one way. Each maps a canonical
     spelling that appears in the bank to the variants a player might type. */
  var CLUSTERS = [
    ['mosaddegh', ['mossadegh', 'mosaddeq', 'mossadeq', 'musaddiq', 'mosadegh', 'moussaddegh']],
    ['nasser', ['nasir', 'naser']],
    ['ed-din', ['al-din', 'aldin', 'oddin', 'eldin']],
    ['din', ['deen']],
    ['reza', ['riza']],
    ['shariati', ["shari'ati", 'shariyati']],
    ['hoveyda', ['hoveida', 'howeyda']],
    ['sattar khan', ['sattarkhan']],
    ['fazlollah', ['fazlullah', 'fazl-allah']],
    ['turkmenchay', ['torkamanchay', 'turkmanchay', 'turkmanchai', 'torkamanchai']],
    ['fayziyeh', ['feiziyeh', 'fayziya', 'feiziyya']],
    ['roohangiz', ['ruhangiz', 'sedigheh']],
    ['saminejad', ["sami'nezhad", 'saminezhad']],
    ['ohanian', ['oganians', 'hovhannes ohanian']]
  ];

  function transliterationAliases(entity) {
    var norm = normalize(entity, false);
    var variants = { };
    variants[norm] = true;

    for (var i = 0; i < CLUSTERS.length; i++) {
      var canonical = CLUSTERS[i][0];
      if (norm.indexOf(canonical) === -1) continue;
      var alts = CLUSTERS[i][1];
      for (var a = 0; a < alts.length; a++) {
        variants[norm.split(canonical).join(alts[a])] = true;
      }
    }
    return Object.keys(variants);
  }

  // ── Confusion rules ────────────────────────────────────────
  /* The historically adjacent names a contestant confuses with the answer.
     These run before any generous matching, because the whole point of the
     write-in mode is that it reads what was meant — and "Reza Shah" when the
     clue wanted his son is not a typo, it is a different man.

     `reason` is an i18n key, not a sentence: the host says it in the language
     of the room. */
  var NON_SURNAMES = ['shah', 'khan', 'mirza', 'seyed', 'sayyid', 'ayatollah', 'imam',
    'general', 'doctor', 'dr', 'شاه', 'خان', 'میرزا', 'آیتالله', 'امام'];

  var CONFUSIONS = [
    {
      expected: ['mohammad reza shah', 'mohammad reza pahlavi', 'محمدرضا شاه', 'محمدرضا پهلوی'],
      forbidden: ['reza shah', 'reza khan', 'reza pahlavi', 'رضا شاه', 'رضاخان', 'رضا پهلوی'],
      reason: 'judge.hisFather', prompt: false
    },
    {
      expected: ['reza shah', 'reza khan', 'رضا شاه', 'رضاخان'],
      forbidden: ['mohammad reza shah', 'mohammad reza', 'محمدرضا شاه', 'محمدرضا'],
      reason: 'judge.hisSon', prompt: false
    },
    {
      expected: ['mohammad reza shah', 'محمدرضا شاه'],
      forbidden: ['mohammad ali shah', 'محمدعلی شاه'],
      reason: 'judge.qajarMajles', prompt: false
    },
    {
      expected: ['mohammad ali shah', 'محمدعلی شاه'],
      forbidden: ['mohammad reza shah', 'محمدرضا شاه'],
      reason: 'judge.pahlaviMonarch', prompt: false
    },
    {
      expected: ['sheikh fazlollah', 'fazlollah nuri', 'فضل الله نوری', 'فضلالله نوری'],
      forbidden: ['zahedi', 'general zahedi', 'fazlollah zahedi', 'فضل الله زاهدی', 'زاهدی'],
      reason: 'judge.zahedi', prompt: false
    },
    {
      expected: ['sheikh fazlollah nuri', 'fazlollah nuri', 'فضل الله نوری'],
      forbidden: ['fazlollah', "fazlu'llah", 'فضل الله', 'فضلالله'],
      reason: 'judge.whichFazlollah', prompt: true
    },
    {
      expected: ['ahmad qavam', 'qavam al-saltaneh', 'احمد قوام', 'قوام‌السلطنه'],
      forbidden: ['qavam', 'قوام'],
      reason: 'judge.whichQavam', prompt: true
    },
    {
      expected: ['ali amini', 'علی امینی'],
      forbidden: ['ali', 'mansur', 'علی', 'منصور'],
      reason: 'judge.fullName', prompt: true
    },
    {
      expected: ['hassan taqizadeh', 'حسن تقیزاده'],
      forbidden: ['hassan', 'pirnia', 'حسن', 'پیرنیا'],
      reason: 'judge.whichHassan', prompt: true
    },
    {
      expected: ['mirza malkom khan', 'میرزا ملکم خان'],
      forbidden: ['mostowfi', 'مستوفی'],
      reason: 'judge.mostowfi', prompt: false
    }
  ];

  // ── Guards ─────────────────────────────────────────────────

  /* The bank offers four options per clue and lists one of them as correct;
     any alias that is also one of the wrong options is bank noise, not an
     answer — the game cannot tell a player an option is wrong and then accept
     it when they type it. */
  function aliasesFor(clue) {
    var options = clue.options || [];
    var wrong = [];
    for (var i = 0; i < options.length; i++) {
      if (i !== clue.correct) wrong.push(normalize(options[i], false));
    }
    return (clue.aliases || []).filter(function (a) {
      return wrong.indexOf(normalize(a, false)) === -1;
    });
  }

  var ROMAN = /^[ivxlcdm]+$/;

  /* Digits and ordinals, in the shape they survive normalization. "Resolution
     242" and "Resolution 598" are one character apart and this bank is full of
     near-miss pairs like them, so any candidate whose numbers differ is a
     different answer no matter how close the rest of the string is. Roman
     numerals are read too, since "Mithridates I" and "Mithridates II" collapse
     to the same phonetic key once doubled letters are folded. */
  function numeralSignature(s) {
    var tokens = String(s).toLowerCase().split(' ').filter(function (w) { return w.length > 0; });
    var out = [];
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      if (/^\d+$/.test(t)) { out.push(t.replace(/^0+/, '') || '0'); continue; }
      var bare = t.replace(/[^a-z]/g, '');
      if (bare.length <= 4 && ROMAN.test(bare) && bare === t) out.push(bare);
    }
    return out.join('|');
  }

  // ── The ladder ─────────────────────────────────────────────

  function judge(utterance, clue, opts) {
    var trimmed = String(utterance == null ? '' : utterance).replace(/^\s+|\s+$/g, '');
    if (!trimmed) return { result: 'incorrect', confidence: 0, method: 'empty_input' };

    var answer = clue.answer;
    var aliases = aliasesFor(clue);
    var every = [answer].concat(aliases);

    var normInput = normalize(trimmed, true);
    var normPreserved = normalize(trimmed, false);
    var normCanonical = normalize(answer, false);

    // 1. The confusion set, ahead of every generous rule. A rule that only
    // asks for more detail is skipped on the second try, so a player cannot be
    // trapped in a prompt that never accepts anything.
    for (var r = 0; r < CONFUSIONS.length; r++) {
      var rule = CONFUSIONS[r];
      if (rule.prompt && opts && opts.noPrompt) continue;
      var applies = false;
      for (var e = 0; e < rule.expected.length; e++) {
        if (normCanonical === normalize(rule.expected[e], false)) { applies = true; break; }
      }
      if (!applies) continue;

      for (var f = 0; f < rule.forbidden.length; f++) {
        var pattern = normalize(rule.forbidden[f], false);
        if (normPreserved === pattern || normInput === pattern) {
          return {
            result: rule.prompt ? 'prompt' : 'incorrect',
            confidence: rule.prompt ? 0.85 : 0.95,
            method: rule.prompt ? 'confusion_rule_prompt' : 'confusion_rule_rejection',
            clarification: rule.reason
          };
        }
      }
    }

    // 2. The answer itself.
    if (normInput === normCanonical || normPreserved === normCanonical) {
      return { result: 'correct', confidence: 1, method: 'exact_canonical', matched: answer };
    }

    // 3. Any accepted spelling of it.
    for (var i = 0; i < aliases.length; i++) {
      var alias = aliases[i];
      var nAlias = normalize(alias, false);
      if (normInput === nAlias || normInput === normalize(alias, true) || normPreserved === nAlias) {
        return { result: 'correct', confidence: 0.98, method: 'alias_exact', matched: alias };
      }
    }

    // 3.5. The clue's own distractors. A text the board has just marked wrong
    // cannot come back as right through a rule further down that forgives
    // spelling, so this sits above all of them. The answer and every accepted
    // spelling returned already, and aliasesFor dropped the aliases that were
    // themselves distractors, so nothing legitimate reaches this point.
    var options = clue.options || [];
    var wrongNorms = [];
    for (var o = 0; o < options.length; o++) {
      if (o === clue.correct) continue;
      wrongNorms.push(normalize(options[o], false));
    }
    for (var w = 0; w < wrongNorms.length; w++) {
      if (wrongNorms[w] && (normInput === wrongNorms[w] || normPreserved === wrongNorms[w])) {
        return { result: 'incorrect', confidence: 0.95, method: 'distractor' };
      }
    }

    // 3.6. A longer phrase that contains the answer as a whole word, as in "the
    // Fayziyeh school in Qom" for a clue that wanted the school. Padded with
    // spaces on both sides so "Mithridates II" does not "contain" "Mithridates
    // I", and vetoed outright when the numbers differ, because that pair is the
    // same mistake in a dozen other costumes.
    var inputNumeral = numeralSignature(normInput);
    for (var j = 0; j < every.length; j++) {
      var nFull = normalize(every[j], false);
      var nBare = normalize(every[j], true);
      if (numeralSignature(nFull) !== inputNumeral) continue;
      if ((nFull.length >= 4 && (' ' + normInput + ' ').indexOf(' ' + nFull + ' ') !== -1) ||
          (nBare.length >= 4 && (' ' + normInput + ' ').indexOf(' ' + nBare + ' ') !== -1)) {
        return { result: 'correct', confidence: 0.95, method: 'phrase_inclusion', matched: every[j] };
      }
    }

    // 5. Explicit transliteration clusters.
    var inputVariants = transliterationAliases(normInput);
    for (var k = 0; k < every.length; k++) {
      if (numeralSignature(normalize(every[k], false)) !== inputNumeral) continue;
      var aliasVariants = transliterationAliases(every[k]);
      for (var v = 0; v < inputVariants.length; v++) {
        if (aliasVariants.indexOf(inputVariants[v]) !== -1) {
          return { result: 'correct', confidence: 0.94, method: 'transliteration_mapping', matched: every[k] };
        }
      }
    }

    // 5.5. A surname alone, unless it is a title rather than a name.
    var surnamed = surnameMatch(normInput, every);
    if (surnamed) {
      return { result: 'correct', confidence: surnamed.confidence, method: surnamed.method, matched: surnamed.alias };
    }

    // 5.6. Loose phonetic comparison, for spellings no cluster anticipated.
    // Two edits is the whole allowance at this distance: a transliterated name
    // varies in its letters, not in how many words it has or which ones they
    // are, and stretching the allowance to a fifth of the string is what let
    // "Tehran International Film Festival" pass for "Fajr International Film
    // Festival" — five edits on thirty-one characters, 84% alike, and a
    // different festival.
    var inputPhonetic = phoneticKey(normInput);
    if (inputPhonetic.length >= 4) {
      for (var m = 0; m < every.length; m++) {
        if (numeralSignature(normalize(every[m], false)) !== inputNumeral) continue;
        var aliasPhonetic = phoneticKey(normalize(every[m], true));
        if (aliasPhonetic.length < 4) continue;
        var d1 = levenshtein(inputPhonetic, aliasPhonetic);
        if (similarity(inputPhonetic, aliasPhonetic) >= 0.78 && d1 <= 2) {
          return {
            result: 'correct', confidence: similarity(inputPhonetic, aliasPhonetic),
            method: 'phonetic_transliteration', matched: every[m]
          };
        }
      }
    }

    // 6. Typos, tightly bounded: same number of words (or both long), same
    // first letter, two edits at most on a string that is already close.
    var inputWords = normInput.split(' ').length;
    for (var n = 0; n < every.length; n++) {
      var candidate = normalize(every[n], false);
      if (numeralSignature(candidate) !== inputNumeral) continue;
      var aliasWords = candidate.split(' ').length;
      if (inputWords !== aliasWords && (normInput.length < 6 || candidate.length < 6)) continue;
      if (normInput.charAt(0) !== candidate.charAt(0)) continue;
      var d2 = levenshtein(normInput, candidate);
      if (Math.max(normInput.length, candidate.length) === 0) continue;
      if (similarity(normInput, candidate) >= 0.88 && d2 <= 2) {
        return { result: 'correct', confidence: similarity(normInput, candidate), method: 'fuzzy_levenshtein', matched: every[n] };
      }
    }

    return { result: 'incorrect', confidence: 0.95, method: 'no_match' };
  }

  function surnameMatch(input, answers) {
    var words = input.split(' ').filter(function (w) { return w.length > 0; });
    if (words.length !== 1) return null;
    var submitted = words[0];
    if (submitted.length < 4 || NON_SURNAMES.indexOf(submitted) !== -1) return null;

    for (var i = 0; i < answers.length; i++) {
      var normal = normalize(answers[i], true);
      var parts = normal.split(' ').filter(function (w) { return w.length > 0; });
      if (parts.length < 2) continue;
      var surname = parts[parts.length - 1];
      if (NON_SURNAMES.indexOf(surname) !== -1) continue;
      if (submitted === surname) {
        return { alias: answers[i], confidence: 0.97, method: 'surname_exact' };
      }
      var a = phoneticKey(submitted), b = phoneticKey(surname);
      if (a.length < 4 || b.length < 4) continue;
      var len = Math.max(a.length, b.length);
      var d = levenshtein(a, b);
      if (similarity(a, b) >= 0.80 && d <= Math.max(2, Math.ceil(len * 0.20))) {
        return { alias: answers[i], confidence: similarity(a, b), method: 'surname_phonetic' };
      }
    }
    return null;
  }

  window.Answers = {
    judge: judge,
    normalize: normalize,
    phoneticKey: phoneticKey
  };
})(window);
