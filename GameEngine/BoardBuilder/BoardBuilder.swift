import Foundation

public final class BoardBuilder {
    private let questionBank: QuestionBank

    public init(questionBank: QuestionBank = .shared) {
        self.questionBank = questionBank
    }

    public func buildBoard(
        language: GameLanguage = .english,
        mode: GameMode = .classic,
        difficulty: Difficulty = .standard,
        round: GameRound = .single,
        randomize: Bool = false
    ) -> GameBoard {
        // The source bank keeps its historical difficulty tiers in legacy
        // dollar values; the player-facing board is denominated in toomans.
        let sourceValues = round == .double ? [400, 800, 1200, 1600, 2000] : [200, 400, 600, 800, 1000]
        let standardValues = round == .double ? [20_000_000, 50_000_000, 100_000_000, 150_000_000, 200_000_000] : [10_000_000, 25_000_000, 50_000_000, 100_000_000, 200_000_000]

        // Find categories that have all 5 values for this round
        let roundCategories = questionBank.categories(for: round).filter { cat in
            let clues = questionBank.clues(for: cat, round: round)
            return sourceValues.allSatisfy { val in clues.contains { $0.value == val } }
        }

        var chosenCategories: [String] = []
        if roundCategories.count >= 6 {
            if randomize {
                let key = "playedCategories." + round.rawValue
                let seen = Set(UserDefaults.standard.stringArray(forKey: key) ?? [])
                let fresh = roundCategories.filter { !seen.contains($0) }.shuffled()
                let previous = roundCategories.filter { seen.contains($0) }.shuffled()
                chosenCategories = Array((fresh + previous).prefix(6))
                let next = fresh.count >= 6 ? seen.union(chosenCategories) : Set(chosenCategories)
                UserDefaults.standard.set(Array(next), forKey: key)
            } else {
                chosenCategories = Array(roundCategories.prefix(6))
            }
        } else {
            // Fallback to any available categories
            chosenCategories = Array(questionBank.availableCategories.prefix(6))
        }

        // Daily Double placements:
        // Round 1 (Single): Exactly 1 Daily Double (in rows 1, 2, or 3)
        // Round 2 (Double): Exactly 2 Daily Doubles in different categories
        var wagerPositions: Set<String> = []
        if round == .single {
            let cat = randomize ? Int.random(in: 0..<6) : 1
            let row = randomize ? Int.random(in: 1..<5) : 2
            wagerPositions.insert("\(cat)_\(row)")
        } else if round == .double {
            let cat1 = randomize ? Int.random(in: 0..<6) : 1
            let row1 = randomize ? Int.random(in: 1..<5) : 2
            let cat2 = randomize ? (cat1 + Int.random(in: 1..<6)) % 6 : 4
            let row2 = randomize ? Int.random(in: 1..<5) : 3
            wagerPositions.insert("\(cat1)_\(row1)")
            wagerPositions.insert("\(cat2)_\(row2)")
        }

        var slots: [BoardSlot] = []
        for (catIdx, category) in chosenCategories.enumerated() {
            let cluesForCategory = questionBank.clues(for: category, round: round)
                .sorted { $0.value < $1.value }

            for (valIdx, value) in standardValues.enumerated() {
                let isWager = wagerPositions.contains("\(catIdx)_\(valIdx)")
                if let matchingClue = cluesForCategory.first(where: { $0.value == sourceValues[valIdx] }) {
                    let localizedClue = questionBank.localized(matchingClue, language: language)
                    let slot = BoardSlot(
                        category: category,
                        categoryIndex: catIdx,
                        valueIndex: valIdx,
                        value: value,
                        clue: randomize ? localizedClue.shufflingOptions() : localizedClue,
                        isSpecialWager: isWager
                    )
                    slots.append(slot)
                } else if valIdx < cluesForCategory.count {
                    let clue = questionBank.localized(cluesForCategory[valIdx], language: language)
                    let slot = BoardSlot(
                        category: category,
                        categoryIndex: catIdx,
                        valueIndex: valIdx,
                        value: value,
                        clue: clue,
                        isSpecialWager: isWager
                    )
                    slots.append(slot)
                }
            }
        }

        return GameBoard(categories: chosenCategories, slots: slots)
    }
}
