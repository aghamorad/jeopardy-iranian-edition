import Foundation

public struct PersianNormalizer {
    private static let arabicToPersianMap: [Character: Character] = [
        "\u{064A}": "\u{06CC}", // Arabic Yeh -> Persian Yeh
        "\u{0649}": "\u{06CC}", // Alef Maksura -> Persian Yeh
        "\u{0643}": "\u{06A9}", // Arabic Kaf -> Persian Kaf
        "\u{06C0}": "\u{0647}", // Heh with Yeh above -> Heh
        "\u{0629}": "\u{0647}"  // Teh Marbuta -> Heh
    ]

    private static let numeralMap: [Character: Character] = [
        "۰": "0", "۱": "1", "۲": "2", "۳": "3", "۴": "4", "۵": "5", "۶": "6", "۷": "7", "۸": "8", "۹": "9",
        "٠": "0", "١": "1", "٢": "2", "٣": "3", "٤": "4", "٥": "5", "٦": "6", "٧": "7", "٨": "8", "٩": "9"
    ]

    private static let diacritics: Set<Character> = [
        "\u{064B}", "\u{064C}", "\u{064D}", "\u{064E}", "\u{064F}",
        "\u{0650}", "\u{0651}", "\u{0652}", "\u{0654}", "\u{0670}"
    ]

    // Only purely conversational / modern honorifics that add zero historical identity
    private static let disposableHonorifics = [
        "dr.", "dr", "doctor", "دکتر", "دكتر", "آقای", "اقای", "mr.", "mr"
    ]

    public static func normalize(_ input: String, stripDisposableHonorifics: Bool = false) -> String {
        let text = input.precomposedStringWithCanonicalMapping

        var transformed = ""
        for char in text {
            if diacritics.contains(char) {
                continue
            }
            if let persian = arabicToPersianMap[char] {
                transformed.append(persian)
            } else if let num = numeralMap[char] {
                transformed.append(num)
            } else if char == "\u{200C}" { // ZWNJ
                transformed.append(" ")
            } else {
                transformed.append(char)
            }
        }

        // Clean punctuation and lower-case
        let allowedCharacterSet = CharacterSet.alphanumerics.union(CharacterSet.whitespaces)
        let cleaned = transformed.unicodeScalars.filter { allowedCharacterSet.contains($0) }
        var result = String(cleaned).lowercased()

        // Normalize Latin accents (e.g., Sattár -> Sattar, Liákhov -> Liakhov)
        result = result.folding(options: [.diacriticInsensitive, .caseInsensitive], locale: .current)

        var words = result.components(separatedBy: .whitespacesAndNewlines).filter { !$0.isEmpty }

        if stripDisposableHonorifics && !words.isEmpty {
            while !words.isEmpty {
                let first = words[0]
                if disposableHonorifics.contains(first) {
                    words.removeFirst()
                } else {
                    break
                }
            }
        }

        return words.joined(separator: " ")
    }

    public static func transliterationAliases(for entity: String) -> [String] {
        let norm = normalize(entity, stripDisposableHonorifics: false)
        var variants = [norm]

        // Common Persian/English transliteration clusters
        let translitClusters: [(String, [String])] = [
            ("mosaddegh", ["mossadegh", "mosaddeq", "mossadeq", "musaddiq", "mosadegh", "moussaddegh"]),
            ("nasser", ["nasir", "naser"]),
            ("ed-din", ["al-din", "aldin", "oddin", "eldin"]),
            ("din", ["deen"]),
            ("reza", ["riza"]),
            ("shariati", ["shari'ati", "shariyati"]),
            ("hoveyda", ["hoveida", "howeyda"]),
            ("sattar khan", ["sattarkhan"]),
            ("fazlollah", ["fazlullah", "fazl-allah"]),
            ("turkmenchay", ["torkamanchay", "turkmanchay", "turkmanchai", "torkamanchai"]),
            ("fayziyeh", ["feiziyeh", "fayziya", "feiziyya"]),
            ("roohangiz", ["ruhangiz", "sedigheh"]),
            ("saminejad", ["sami'nezhad", "saminezhad"]),
            ("ohanian", ["oganians", "hovhannes ohanian"])
        ]

        for (canonical, alts) in translitClusters {
            if norm.contains(canonical) {
                for alt in alts {
                    variants.append(norm.replacingOccurrences(of: canonical, with: alt))
                }
            }
        }

        return Array(Set(variants))
    }
}
