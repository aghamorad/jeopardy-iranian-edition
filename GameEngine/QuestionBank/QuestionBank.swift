import Foundation

public final class QuestionBank {
    public static let shared = QuestionBank()

    public private(set) var allClues: [Clue] = []
    public private(set) var persianCopy: [String: PersianClueCopy] = [:]

    public init() {
        loadClues()
    }

    /// Where the package sits on the machine that compiled it. The fallbacks below
    /// are for `swift run` during development, so they can be resolved from this
    /// file's own path instead of naming anyone's home directory. `#filePath` is
    /// `<package>/GameEngine/QuestionBank/QuestionBank.swift`.
    private static var packageRoot: String {
        URL(fileURLWithPath: #filePath)
            .deletingLastPathComponent()   // GameEngine/QuestionBank
            .deletingLastPathComponent()   // GameEngine
            .deletingLastPathComponent()   // package root
            .path
    }

    public func reloadClues() {
        loadClues()
    }

    private func loadClues() {
        loadPersianCopy()
        // 1. Direct bundle resourceURL (inside .app/Contents/Resources)
        if let resURL = Bundle.main.resourceURL?.appendingPathComponent("verified_clues.json"),
           let decoded = decodeBank(at: resURL) {
            self.allClues = decoded
            return
        }

        // 2. Standard bundle resource lookup
        if let bundleURL = Bundle.main.url(forResource: "verified_clues", withExtension: "json"),
           let decoded = decodeBank(at: bundleURL) {
            self.allClues = decoded
            return
        }

        // 3. Paths relative to the package, then to the working directory
        let candidatePaths = [
            "\(Self.packageRoot)/QuestionBank/verified_clues.json",
            "QuestionBank/verified_clues.json",
            "../QuestionBank/verified_clues.json"
        ]

        for path in candidatePaths {
            if let decoded = decodeBank(at: URL(fileURLWithPath: path)) {
                self.allClues = decoded
                return
            }
        }

        fatalError("QuestionBank: no bank loaded. Looked in the bundle and at \(candidatePaths.joined(separator: ", ")).")
    }

    /// A file that is not there means try the next candidate. A file that is there
    /// and will not decode means the bank is broken, and this is the last moment
    /// anything can say so: swallow it and the game plays an empty board.
    private func decodeBank(at url: URL) -> [Clue]? {
        guard let data = try? Data(contentsOf: url) else { return nil }
        do {
            let decoded = try JSONDecoder().decode([Clue].self, from: data)
            return decoded.isEmpty ? nil : decoded
        } catch {
            fatalError("QuestionBank: \(url.path) will not decode — \(error)")
        }
    }

    public func localized(_ clue: Clue, language: GameLanguage) -> Clue {
        clue.localized(language: language, persianCopy: persianCopy[clue.id])
    }

    private func loadPersianCopy() {
        let candidates = [
            Bundle.main.resourceURL?.appendingPathComponent("persian_clues.json"),
            Bundle.main.url(forResource: "persian_clues", withExtension: "json"),
            URL(fileURLWithPath: "\(Self.packageRoot)/App/Resources/persian_clues.json"),
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
