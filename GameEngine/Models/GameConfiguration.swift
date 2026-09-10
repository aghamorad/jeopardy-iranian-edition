import Foundation

public enum GameMode: String, CaseIterable, Codable {
    case classic = "Typed Response"
    case multipleChoice = "Multiple Choice (4 Options)"
}

public enum GameLanguage: String, CaseIterable, Codable {
    case english = "English"
    case persian = "فارسی (Persian)"
}

public struct GameConfiguration: Codable {
    public var language: GameLanguage
    public var mode: GameMode
    public var difficulty: Difficulty
    public var buzzerLockoutPenaltyMs: Double
    public var answeringTimeoutSeconds: Double
    public var audioSpeechEnabled: Bool
    public var hostCommentaryEnabled: Bool

    public init(
        language: GameLanguage = .english,
        mode: GameMode = .classic,
        difficulty: Difficulty = .standard,
        buzzerLockoutPenaltyMs: Double = 600.0,
        answeringTimeoutSeconds: Double = 12.0,
        audioSpeechEnabled: Bool = false,
        hostCommentaryEnabled: Bool = true
    ) {
        self.language = language
        self.mode = mode
        self.difficulty = difficulty
        self.buzzerLockoutPenaltyMs = buzzerLockoutPenaltyMs
        self.answeringTimeoutSeconds = answeringTimeoutSeconds
        self.audioSpeechEnabled = audioSpeechEnabled
        self.hostCommentaryEnabled = hostCommentaryEnabled
    }
}
