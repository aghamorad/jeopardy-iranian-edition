import Foundation

public final class QuestionBank {
    public static let shared = QuestionBank()

    public private(set) var allClues: [Clue] = []
    public private(set) var persianCopy: [String: PersianClueCopy] = [:]

    public init() {
        loadClues()
    }

    public func reloadClues() {
        loadClues()
    }

    private func loadClues() {
        loadPersianCopy()
        // 1. Direct bundle resourceURL (inside .app/Contents/Resources)
        if let resURL = Bundle.main.resourceURL?.appendingPathComponent("verified_clues.json"),
           let data = try? Data(contentsOf: resURL),
           let decoded = try? JSONDecoder().decode([Clue].self, from: data), !decoded.isEmpty {
            self.allClues = decoded
            return
        }

        // 2. Standard bundle resource lookup
        if let bundleURL = Bundle.main.url(forResource: "verified_clues", withExtension: "json"),
           let data = try? Data(contentsOf: bundleURL),
           let decoded = try? JSONDecoder().decode([Clue].self, from: data), !decoded.isEmpty {
            self.allClues = decoded
            return
        }

        // 3. Absolute path and relative paths
        let candidatePaths = [
            "/Users/Morad/Desktop/Jeopardy - Iranian Edition/QuestionBank/verified_clues.json",
            "QuestionBank/verified_clues.json",
            "../QuestionBank/verified_clues.json"
        ]

        for path in candidatePaths {
            let url = URL(fileURLWithPath: path)
            if let data = try? Data(contentsOf: url),
               let decoded = try? JSONDecoder().decode([Clue].self, from: data), !decoded.isEmpty {
                self.allClues = decoded
                return
            }
        }
    }

    public func localized(_ clue: Clue, language: GameLanguage) -> Clue {
        clue.localized(language: language, persianCopy: persianCopy[clue.id])
    }

    private func loadPersianCopy() {
        let candidates = [
            Bundle.main.resourceURL?.appendingPathComponent("persian_clues.json"),
            Bundle.main.url(forResource: "persian_clues", withExtension: "json"),
            URL(fileURLWithPath: "/Users/Morad/Desktop/Jeopardy - Iranian Edition/App/Resources/persian_clues.json"),
            URL(fileURLWithPath: "App/Resources/persian_clues.json")
        ].compactMap { $0 }
        for url in candidates {
            if let data = try? Data(contentsOf: url),
               let decoded = try? JSONDecoder().decode([String: PersianClueCopy].self, from: data),
               !decoded.isEmpty {
                persianCopy = decoded
                return
            }
        }
    }

    public func getClues(forCategory category: String) -> [Clue] {
        allClues.filter { $0.category.lowercased() == category.lowercased() }
    }

    public func clues(for category: String, round: GameRound) -> [Clue] {
        allClues.filter { $0.category.lowercased() == category.lowercased() && $0.round == round }
    }

    public var availableCategories: [String] {
        Array(Set(allClues.map { $0.category })).sorted()
    }

    public func categories(for round: GameRound) -> [String] {
        let roundClues = allClues.filter { $0.round == round }
        return Array(Set(roundClues.map { $0.category })).sorted()
    }

    public func randomFinalClue() -> Clue? {
        let finals = allClues.filter { $0.round == .final }
        return finals.randomElement() ?? allClues.first
    }
}
