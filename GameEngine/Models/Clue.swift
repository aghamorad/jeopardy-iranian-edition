import Foundation

public enum Difficulty: String, Codable, CaseIterable {
    case casual = "CASUAL"
    case standard = "STANDARD"
    case scholar = "SCHOLAR"
    case insufferable = "INSUFFERABLE"
}

public enum GameRound: String, Codable {
    case single
    case double
    case final
}

public enum EvidenceType: String, Codable {
    case establishedFact = "established_fact"
    case scholarlyInterpretation = "scholarly_interpretation"
    case primaryTestimony = "primary_testimony"
    case disputed = "disputed"
}

public struct DistractorRationale: Codable, Hashable {
    public let option: String
    public let whyPlausible: String
    public let whyWrong: String

    enum CodingKeys: String, CodingKey {
        case option
        case whyPlausible = "why_plausible"
        case whyWrong = "why_wrong"
    }

    public init(option: String, whyPlausible: String, whyWrong: String) {
        self.option = option
        self.whyPlausible = whyPlausible
        self.whyWrong = whyWrong
    }
}

public struct HostReactions: Codable {
    public let correctGeneric: String
    public let wrongGeneric: String
    public let commonWrongAnswers: [String: String]?
    public let specificityPrompt: String?
    public let explanation: String?

    enum CodingKeys: String, CodingKey {
        case correctGeneric = "correct_generic"
        case wrongGeneric = "wrong_generic"
        case commonWrongAnswers = "common_wrong_answers"
        case specificityPrompt = "specificity_prompt"
        case explanation
    }

    public init(correctGeneric: String, wrongGeneric: String, commonWrongAnswers: [String: String]? = nil, specificityPrompt: String? = nil, explanation: String? = nil) {
        self.correctGeneric = correctGeneric
        self.wrongGeneric = wrongGeneric
        self.commonWrongAnswers = commonWrongAnswers
        self.specificityPrompt = specificityPrompt
        self.explanation = explanation
    }
}

public struct Clue: Identifiable, Codable, Hashable {
    public let id: String
    public let language: String
    public let category: String
    public let historicalPeriod: String
    public let theme: String
    public let difficulty: Difficulty
    public let value: Int
    public let round: GameRound
    public let clueText: String
    public let canonicalAnswer: String
    public let acceptedAliases: [String]
    public let partialAnswers: [String]
    public let specificityPrompt: String?
    public let options: [String]
    public let correctOptionIndex: Int
    public let distractorRationales: [DistractorRationale]
    public let explanation: String
    public let sourceId: String
    public let bookTitle: String
    public let author: String
    public let chapter: String
    public let page: Int
    public let supportingPassage: String
    public let evidenceType: EvidenceType
    public let confidence: Double
    public let editorialValidationStatus: String
    public let hostReactions: HostReactions

    enum CodingKeys: String, CodingKey {
        case id
        case language
        case category
        case historicalPeriod = "historical_period"
        case theme
        case difficulty
        case value
        case round
        case clueText = "clue_text"
        case canonicalAnswer = "canonical_answer"
        case acceptedAliases = "accepted_aliases"
        case partialAnswers = "partial_answers"
        case specificityPrompt = "specificity_prompt"
        case options
        case correctOptionIndex = "correct_option_index"
        case distractorRationales = "distractor_rationales"
        case explanation
        case sourceId = "source_id"
        case bookTitle = "book_title"
        case author
        case chapter
        case page
        case supportingPassage = "supporting_passage"
        case evidenceType = "evidence_type"
        case confidence
        case editorialValidationStatus = "editorial_validation_status"
        case hostReactions = "host_reactions"
    }

    public func hash(into hasher: inout Hasher) {
        hasher.combine(id)
    }

    public static func == (lhs: Clue, rhs: Clue) -> Bool {
        lhs.id == rhs.id
    }
}

public extension Clue {
    func shufflingOptions() -> Clue {
        guard options.indices.contains(correctOptionIndex),
              let data = try? JSONEncoder().encode(self),
              var object = (try? JSONSerialization.jsonObject(with: data)) as? [String: Any] else { return self }
        let answer = options[correctOptionIndex]
        let shuffled = options.shuffled()
        object["options"] = shuffled
        object["correct_option_index"] = shuffled.firstIndex(of: answer) ?? 0
        guard let output = try? JSONSerialization.data(withJSONObject: object), let clue = try? JSONDecoder().decode(Clue.self, from: output) else { return self }
        return clue
    }
}
