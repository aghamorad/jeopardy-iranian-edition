import Foundation

public struct HostPersona {
    public static let correctLines = [
        "Afarin. Correct. Please try not to become unbearable before the commercial break.",
        "Correct! The archives are stunned, and frankly so am I.",
        "Barakallah. Against the evidence of your earlier confidence, you actually knew it.",
        "Precisely right. Look at you, one answer away from demanding your own documentary.",
        "Correct. Hafez approves; I remain cautiously unconvinced.",
        "A clean answer. Enjoy this rare moment when both history and I are on your side.",
        "Mashallah, that was right. Somebody alert the family group chat.",
        "Correct! You made it look effortless, which is generous of the editing department."
    ]

    public static let wrongLines = [
        "No, azizam. You did not miss by a mile; you missed by several centuries.",
        "Incorrect. That answer arrived with confidence, luggage, and no relation to the clue.",
        "A brave answer. Wrong, but brave is what we say when accuracy has left the building.",
        "No. Even the wrong dynasty has filed a complaint.",
        "Afsoos. The archives would like their time back.",
        "Incorrect. You rang in so quickly I assumed you knew something. My mistake.",
        "Absolutely not. Somewhere, a history teacher just sat upright without knowing why.",
        "Wrong. The good news is that confidence remains completely undefeated."
    ]

    public static let specificityLines = [
        "Which one? Be specific—Persian history has far too many Shahs!",
        "A bit more precision, scholar! Don't leave me wandering in the bazaar.",
        "Father or son? King or prince? I need the exact name!",
        "Narrow it down, contestant. History demands precision!",
        "Which era? Which monarch? Give me the specific title."
    ]

    public static func reactionFor(resolution: AnswerResolution, clue: Clue, language: GameLanguage) -> String {
        switch resolution.result {
        case .correct:
            return correctLines.randomElement() ?? "Barakallah! Spot on."

        case .incorrect:
            if let matched = resolution.matchedAlias,
               let specificWrong = clue.hostReactions.commonWrongAnswers?[matched] {
                return specificWrong + " " + (wrongLines.randomElement() ?? "Incorrect.")
            }
            return wrongLines.randomElement() ?? "Afsoos! Completely wrong."

        case .prompt:
            if let custom = clue.hostReactions.specificityPrompt?.nonEmpty {
                return custom
            }
            return specificityLines.randomElement() ?? "Which one? Please be more specific."
        }
    }
}

private extension String {
    var nonEmpty: String? {
        self.isEmpty ? nil : self
    }
}
