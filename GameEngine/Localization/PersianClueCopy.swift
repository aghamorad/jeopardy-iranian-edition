import Foundation

public struct PersianClueCopy: Codable {
    public let clueText: String
    public let canonicalAnswer: String
    public let options: [String]
    public let explanation: String
    public let specificityPrompt: String?

    enum CodingKeys: String, CodingKey {
        case clueText = "clue_text"
        case canonicalAnswer = "canonical_answer"
        case options
        case explanation
        case specificityPrompt = "specificity_prompt"
    }
}

public extension Clue {
    func localized(language: GameLanguage, persianCopy: PersianClueCopy?) -> Clue {
        guard language == .persian, let copy = persianCopy else { return self }
        return Clue(
            id: id,
            language: "fa",
            category: category,
            historicalPeriod: historicalPeriod,
            theme: theme,
            difficulty: difficulty,
            value: value,
            round: round,
            clueText: copy.clueText,
            canonicalAnswer: copy.canonicalAnswer,
            acceptedAliases: Array(Set(acceptedAliases + [canonicalAnswer, copy.canonicalAnswer])),
            partialAnswers: partialAnswers,
            specificityPrompt: copy.specificityPrompt,
            options: copy.options.count == options.count ? copy.options : options,
            correctOptionIndex: correctOptionIndex,
            distractorRationales: distractorRationales,
            explanation: copy.explanation,
            sourceId: sourceId,
            bookTitle: bookTitle,
            author: author,
            chapter: chapter,
            page: page,
            supportingPassage: supportingPassage,
            evidenceType: evidenceType,
            confidence: confidence,
            editorialValidationStatus: editorialValidationStatus,
            hostReactions: hostReactions
        )
    }
}
