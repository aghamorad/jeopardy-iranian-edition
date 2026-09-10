import Foundation

public struct Player: Identifiable, Hashable, Codable {
    public let id: UUID
    public var name: String
    public var score: Int
    public var controllerIndex: Int?
    public var colorHex: String
    public var isLockedOut: Bool
    public var prematureLockoutUntil: Date?
    public var isBot: Bool

    public init(id: UUID = UUID(), name: String, score: Int = 0, controllerIndex: Int? = nil, colorHex: String = "#C49A45", isBot: Bool = false) {
        self.id = id
        self.name = name
        self.score = score
        self.controllerIndex = controllerIndex
        self.colorHex = colorHex
        self.isLockedOut = false
        self.prematureLockoutUntil = nil
        self.isBot = isBot
    }

    public mutating func awardPoints(_ points: Int) {
        score += points
    }

    public mutating func deductPoints(_ points: Int) {
        score -= points
    }
}
