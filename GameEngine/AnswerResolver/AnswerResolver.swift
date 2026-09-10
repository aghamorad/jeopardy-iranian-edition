import Foundation

public enum AnswerResult: String, Codable {
    case correct
    case incorrect
    case prompt
}

public struct AnswerResolution: Codable {
    public let result: AnswerResult
    public let confidence: Double
    public let matchedAlias: String?
    public let resolutionMethod: String
    public let latencyMs: Double
    public let specificityClarification: String?

    public init(
        result: AnswerResult,
        confidence: Double,
        matchedAlias: String? = nil,
        resolutionMethod: String,
        latencyMs: Double,
        specificityClarification: String? = nil
    ) {
        self.result = result
        self.confidence = confidence
        self.matchedAlias = matchedAlias
        self.resolutionMethod = resolutionMethod
        self.latencyMs = latencyMs
        self.specificityClarification = specificityClarification
    }
}

public final class AnswerResolver {
    public static let shared = AnswerResolver()

    // Explicit historical confusion pairs where simple fuzzy/partial match is dangerous
    private struct ConfusionRule {
        let expectedKeywords: [String]
        let forbiddenInputPatterns: [String]
        let rejectionReason: String
        let shouldPromptInstead: Bool
    }

    private let confusionRules: [ConfusionRule] = [
        // Reza Shah vs Mohammad Reza Shah
        ConfusionRule(
            expectedKeywords: ["mohammad reza shah", "mohammad reza pahlavi", "محمدرضا شاه", "محمدرضا پهلوی"],
            forbiddenInputPatterns: ["reza shah", "reza khan", "reza pahlavi", "رضا شاه", "رضاخان", "رضا پهلوی"],
            rejectionReason: "That would be his father.",
            shouldPromptInstead: false
        ),
        ConfusionRule(
            expectedKeywords: ["reza shah", "reza khan", "رضا شاه", "رضاخان"],
            forbiddenInputPatterns: ["mohammad reza shah", "mohammad reza", "محمدرضا شاه", "محمدرضا"],
            rejectionReason: "You're a generation too late; that was his son.",
            shouldPromptInstead: false
        ),
        // Mohammad Ali Shah vs Mohammad Reza Shah
        ConfusionRule(
            expectedKeywords: ["mohammad reza shah", "محمدرضا شاه"],
            forbiddenInputPatterns: ["mohammad ali shah", "محمدعلی شاه"],
            rejectionReason: "No. Mohammad Ali Shah was the Qajar monarch who bombarded the Majles.",
            shouldPromptInstead: false
        ),
        ConfusionRule(
            expectedKeywords: ["mohammad ali shah", "محمدعلی شاه"],
            forbiddenInputPatterns: ["mohammad reza shah", "محمدرضا شاه"],
            rejectionReason: "No, Mohammad Reza Shah was the Pahlavi monarch.",
            shouldPromptInstead: false
        ),
        // Fazlollah Nuri vs Fazlollah Zahedi
        ConfusionRule(
            expectedKeywords: ["sheikh fazlollah", "fazlollah nuri", "فضل الله نوری", "فضل‌الله نوری"],
            forbiddenInputPatterns: ["zahedi", "general zahedi", "fazlollah zahedi", "فضل الله زاهدی", "زاهدی"],
            rejectionReason: "No. General Zahedi was the 1953 premier, not the constitutional-era cleric.",
            shouldPromptInstead: false
        ),
        // Ambiguous lone names that must prompt
        ConfusionRule(
            expectedKeywords: ["sheikh fazlollah nuri", "fazlollah nuri", "فضل الله نوری"],
            forbiddenInputPatterns: ["fazlollah", "fazlu'llah", "فضل الله", "فضل‌الله"],
            rejectionReason: "Which Fazlollah? Please provide his title or surname.",
            shouldPromptInstead: true
        ),
        ConfusionRule(
            expectedKeywords: ["ahmad qavam", "qavam al-saltaneh", "احمد قوام", "قوام‌السلطنه"],
            forbiddenInputPatterns: ["qavam", "قوام"],
            rejectionReason: "Which Qavam? Please specify.",
            shouldPromptInstead: true
        ),
        ConfusionRule(
            expectedKeywords: ["ali amini", "علی امینی"],
            forbiddenInputPatterns: ["ali", "mansur", "علی", "منصور"],
            rejectionReason: "Please provide the full name.",
            shouldPromptInstead: true
        ),
        ConfusionRule(
            expectedKeywords: ["hassan taqizadeh", "حسن تقی‌زاده"],
            forbiddenInputPatterns: ["hassan", "pirnia", "حسن", "پیرنیا"],
            rejectionReason: "Which Hassan? Please provide his surname.",
            shouldPromptInstead: true
        ),
        ConfusionRule(
            expectedKeywords: ["mirza malkom khan", "میرزا ملکم خان"],
            forbiddenInputPatterns: ["mostowfi", "مستوفی"],
            rejectionReason: "No, that was Mostowfi ol-Mamalek.",
            shouldPromptInstead: false
        )
    ]

    public init() {}

    public func resolve(utterance: String, clue: Clue) -> AnswerResolution {
        let startTime = mach_absolute_time()

        let trimmed = utterance.trimmingCharacters(in: .whitespacesAndNewlines)
        if trimmed.isEmpty {
            let elapsedMs = computeElapsedMs(from: startTime)
            return AnswerResolution(
                result: .incorrect,
                confidence: 0.0,
                matchedAlias: nil,
                resolutionMethod: "empty_input",
                latencyMs: elapsedMs
            )
        }

        let normInput = PersianNormalizer.normalize(trimmed, stripDisposableHonorifics: true)
        let normInputPreserved = PersianNormalizer.normalize(trimmed, stripDisposableHonorifics: false)

        // 1. Adversarial Confusion Set / Ambiguity Rules FIRST
        let normCanonical = PersianNormalizer.normalize(clue.canonicalAnswer, stripDisposableHonorifics: false)
        for rule in confusionRules {
            let matchesExpected = rule.expectedKeywords.contains { exp in
                let normExp = PersianNormalizer.normalize(exp, stripDisposableHonorifics: false)
                return normCanonical == normExp
            }
            if matchesExpected {
                for pattern in rule.forbiddenInputPatterns {
                    let normPattern = PersianNormalizer.normalize(pattern, stripDisposableHonorifics: false)
                    if normInputPreserved == normPattern || normInput == normPattern {
                        let elapsedMs = computeElapsedMs(from: startTime)
                        if rule.shouldPromptInstead {
                            return AnswerResolution(
                                result: .prompt,
                                confidence: 0.85,
                                matchedAlias: pattern,
                                resolutionMethod: "confusion_rule_prompt",
                                latencyMs: elapsedMs,
                                specificityClarification: rule.rejectionReason
                            )
                        } else {
                            return AnswerResolution(
                                result: .incorrect,
                                confidence: 0.95,
                                matchedAlias: pattern,
                                resolutionMethod: "confusion_rule_rejection",
                                latencyMs: elapsedMs,
                                specificityClarification: rule.rejectionReason
                            )
                        }
                    }
                }
            }
        }

        // 2. Exact Canonical Match
        if normInput == normCanonical || normInputPreserved == normCanonical {
            let elapsedMs = computeElapsedMs(from: startTime)
            return AnswerResolution(
                result: .correct,
                confidence: 1.0,
                matchedAlias: clue.canonicalAnswer,
                resolutionMethod: "exact_canonical",
                latencyMs: elapsedMs
            )
        }

        // 3. Accepted Aliases Lookup
        for alias in clue.acceptedAliases {
            let normAlias = PersianNormalizer.normalize(alias, stripDisposableHonorifics: false)
            let normAliasStripped = PersianNormalizer.normalize(alias, stripDisposableHonorifics: true)
            if normInput == normAlias || normInput == normAliasStripped || normInputPreserved == normAlias {
                let elapsedMs = computeElapsedMs(from: startTime)
                return AnswerResolution(
                    result: .correct,
                    confidence: 0.98,
                    matchedAlias: alias,
                    resolutionMethod: "alias_exact",
                    latencyMs: elapsedMs
                )
            }
        }

        // 3.5 Substring Phrase Inclusion (e.g. "مدرسه فیضیه قم" contains "مدرسه فیضیه")
        for alias in [clue.canonicalAnswer] + clue.acceptedAliases {
            let normAlias = PersianNormalizer.normalize(alias, stripDisposableHonorifics: false)
            let normAliasStripped = PersianNormalizer.normalize(alias, stripDisposableHonorifics: true)
            if (normAlias.count >= 4 && normInput.contains(normAlias)) ||
               (normAliasStripped.count >= 4 && normInput.contains(normAliasStripped)) {
                let elapsedMs = computeElapsedMs(from: startTime)
                return AnswerResolution(
                    result: .correct,
                    confidence: 0.95,
                    matchedAlias: alias,
                    resolutionMethod: "phrase_inclusion",
                    latencyMs: elapsedMs
                )
            }
        }

        // 4. Check Partial Answers for Specificity Prompt (when user's whole answer is the partial term)
        for partial in clue.partialAnswers {
            let normPartial = PersianNormalizer.normalize(partial, stripDisposableHonorifics: false)
            if normInput == normPartial || normInputPreserved == normPartial {
                let elapsedMs = computeElapsedMs(from: startTime)
                return AnswerResolution(
                    result: .prompt,
                    confidence: 0.80,
                    matchedAlias: partial,
                    resolutionMethod: "partial_specificity_rule",
                    latencyMs: elapsedMs,
                    specificityClarification: clue.specificityPrompt ?? "Please be more specific."
                )
            }
        }

        // 5. Transliteration Normalization
        let inputVariants = PersianNormalizer.transliterationAliases(for: normInput)
        for alias in [clue.canonicalAnswer] + clue.acceptedAliases {
            let aliasVariants = PersianNormalizer.transliterationAliases(for: alias)
            for iv in inputVariants {
                if aliasVariants.contains(iv) {
                    let elapsedMs = computeElapsedMs(from: startTime)
                    return AnswerResolution(
                        result: .correct,
                        confidence: 0.94,
                        matchedAlias: alias,
                        resolutionMethod: "transliteration_mapping",
                        latencyMs: elapsedMs
                    )
                }
            }
        }

        // 5.5 Jeopardy-style surname acceptance. A surname alone is normally
        // sufficient for a person unless an explicit ambiguity rule above
        // requires more information.
        if let surnameMatch = surnameMatch(input: normInput, answers: [clue.canonicalAnswer] + clue.acceptedAliases) {
            let elapsedMs = computeElapsedMs(from: startTime)
            return AnswerResolution(
                result: .correct,
                confidence: surnameMatch.confidence,
                matchedAlias: surnameMatch.alias,
                resolutionMethod: surnameMatch.method,
                latencyMs: elapsedMs
            )
        }

        // 5.6 Loose phonetic transliteration. Persian names have many equally
        // reasonable Latin spellings (q/gh, kh/x, i/y, ou/u, doubled letters).
        // Compare a conservative phonetic key after the explicit confusion
        // guards have already rejected historically different people.
        let inputPhonetic = phoneticTransliterationKey(normInput)
        if inputPhonetic.count >= 4 {
            for alias in [clue.canonicalAnswer] + clue.acceptedAliases {
                let aliasNorm = PersianNormalizer.normalize(alias, stripDisposableHonorifics: true)
                let aliasPhonetic = phoneticTransliterationKey(aliasNorm)
                guard aliasPhonetic.count >= 4 else { continue }
                let distance = levenshteinDistance(s1: inputPhonetic, s2: aliasPhonetic)
                let maxLen = max(inputPhonetic.count, aliasPhonetic.count)
                let similarity = 1.0 - Double(distance) / Double(maxLen)
                let allowance = max(2, Int(ceil(Double(maxLen) * 0.22)))
                if similarity >= 0.78 && distance <= allowance {
                    let elapsedMs = computeElapsedMs(from: startTime)
                    return AnswerResolution(
                        result: .correct,
                        confidence: similarity,
                        matchedAlias: alias,
                        resolutionMethod: "phonetic_transliteration",
                        latencyMs: elapsedMs
                    )
                }
            }
        }

        // 6. Tightened Fuzzy Levenshtein Comparison (88% threshold, edit distance <= 2, matching word count)
        let inputWordCount = normInput.components(separatedBy: .whitespaces).count
        for alias in [clue.canonicalAnswer] + clue.acceptedAliases {
            let normAlias = PersianNormalizer.normalize(alias, stripDisposableHonorifics: false)
            let aliasWordCount = normAlias.components(separatedBy: .whitespaces).count

            // Only allow fuzzy matching if word counts match, or both are multi-letter single words
            guard inputWordCount == aliasWordCount || (normInput.count >= 6 && normAlias.count >= 6) else {
                continue
            }

            // Do not fuzzy match if initial characters differ on key words
            if let firstIn = normInput.first, let firstAl = normAlias.first, firstIn != firstAl {
                continue
            }

            let distance = levenshteinDistance(s1: normInput, s2: normAlias)
            let maxLen = max(normInput.count, normAlias.count)
            if maxLen > 0 {
                let similarity = 1.0 - (Double(distance) / Double(maxLen))
                if similarity >= 0.88 && distance <= 2 {
                    let elapsedMs = computeElapsedMs(from: startTime)
                    return AnswerResolution(
                        result: .correct,
                        confidence: similarity,
                        matchedAlias: alias,
                        resolutionMethod: "fuzzy_levenshtein",
                        latencyMs: elapsedMs
                    )
                }
            }
        }

        // 7. Substring partial fallback: If input contained a partial answer keyword but didn't match full alias, prompt!
        for partial in clue.partialAnswers {
            let normPartial = PersianNormalizer.normalize(partial, stripDisposableHonorifics: false)
            if normInput.contains(normPartial) && normInput.count < (normCanonical.count + 4) {
                let elapsedMs = computeElapsedMs(from: startTime)
                return AnswerResolution(
                    result: .prompt,
                    confidence: 0.70,
                    matchedAlias: partial,
                    resolutionMethod: "partial_substring_prompt",
                    latencyMs: elapsedMs,
                    specificityClarification: clue.specificityPrompt ?? "Please be more specific."
                )
            }
        }

        // If none matched: Incorrect
        let elapsedMs = computeElapsedMs(from: startTime)
        return AnswerResolution(
            result: .incorrect,
            confidence: 0.95,
            matchedAlias: nil,
            resolutionMethod: "no_match",
            latencyMs: elapsedMs
        )
    }

    private func levenshteinDistance(s1: String, s2: String) -> Int {
        let empty = [Int](repeating: 0, count: s2.count + 1)
        var last = [Int](0...s2.count)

        for (i, char1) in s1.enumerated() {
            var cur = [i + 1] + empty[1...]
            for (j, char2) in s2.enumerated() {
                cur[j + 1] = char1 == char2 ? last[j] : min(last[j], last[j + 1], cur[j]) + 1
            }
            last = cur
        }
        return last[s2.count]
    }

    private func surnameMatch(input: String, answers: [String]) -> (alias: String, confidence: Double, method: String)? {
        let inputWords = input.split(separator: " ").map(String.init)
        guard inputWords.count == 1, let submitted = inputWords.first, submitted.count >= 4 else { return nil }
        let nonSurnames: Set<String> = ["shah", "khan", "mirza", "seyed", "sayyid", "ayatollah", "imam", "general", "doctor", "dr", "شاه", "خان", "میرزا", "آیتالله", "امام"]
        guard !nonSurnames.contains(submitted) else { return nil }

        for alias in answers {
            let normalized = PersianNormalizer.normalize(alias, stripDisposableHonorifics: true)
            let words = normalized.split(separator: " ").map(String.init)
            guard words.count >= 2, let surname = words.last, !nonSurnames.contains(surname) else { continue }
            if submitted == surname {
                return (alias, 0.97, "surname_exact")
            }
            let a = phoneticTransliterationKey(submitted)
            let b = phoneticTransliterationKey(surname)
            guard a.count >= 4, b.count >= 4 else { continue }
            let distance = levenshteinDistance(s1: a, s2: b)
            let similarity = 1.0 - Double(distance) / Double(max(a.count, b.count))
            if similarity >= 0.80 && distance <= max(2, Int(ceil(Double(max(a.count, b.count)) * 0.20))) {
                return (alias, similarity, "surname_phonetic")
            }
        }
        return nil
    }

    private func phoneticTransliterationKey(_ text: String) -> String {
        var value = text.lowercased().folding(options: [.diacriticInsensitive, .caseInsensitive], locale: Locale(identifier: "en_US_POSIX"))
        guard value.unicodeScalars.allSatisfy({ $0.isASCII }) else { return value.replacingOccurrences(of: " ", with: "") }
        let replacements: [(String, String)] = [
            ("tch", "c"), ("ch", "c"), ("kh", "x"), ("gh", "q"), ("zh", "j"),
            ("sh", "s"), ("ph", "f"), ("ou", "u"), ("ow", "u"), ("oo", "u"),
            ("ee", "i"), ("aa", "a"), ("q", "q"), ("y", "i")
        ]
        for (from, to) in replacements { value = value.replacingOccurrences(of: from, with: to) }
        value = value.replacingOccurrences(of: "[^a-z0-9]", with: "", options: .regularExpression)
        value = value.replacingOccurrences(of: "([a-z])\\1+", with: "$1", options: .regularExpression)
        if value.hasSuffix("eh") { value.removeLast(2); value.append("e") }
        return value
    }

    private func computeElapsedMs(from start: UInt64) -> Double {
        var info = mach_timebase_info()
        mach_timebase_info(&info)
        let elapsedNanos = (mach_absolute_time() - start) * UInt64(info.numer) / UInt64(info.denom)
        return Double(elapsedNanos) / 1_000_000.0
    }
}
