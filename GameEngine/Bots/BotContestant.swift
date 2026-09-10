import Foundation

public enum BotSkill: String, Codable, CaseIterable { case novice, competent, expert, historian }
public enum BotRisk: String, Codable, CaseIterable { case cautious, normal, aggressive, reckless }

public struct BotProfile: Codable, Hashable {
    public var skill: BotSkill
    public var risk: BotRisk
    public var specialties: Set<String>
    public var weaknesses: Set<String>
    public var confidenceBias: Double
    public init(skill: BotSkill = .competent, risk: BotRisk = .normal, specialties: Set<String> = [], weaknesses: Set<String> = [], confidenceBias: Double = 0) {
        self.skill = skill; self.risk = risk; self.specialties = specialties; self.weaknesses = weaknesses; self.confidenceBias = confidenceBias
    }
}

public struct BotAnswerDecision: Codable, Hashable { public let answer: String?; public let confidence: Double; public let latency: TimeInterval }
public struct BotBuzzIntent: Codable, Hashable { public let playerID: UUID; public let delay: TimeInterval }

public final class BotContestant {
    public let playerID: UUID
    public var profile: BotProfile
    private var rng: RandomNumberGenerator = SystemRandomNumberGenerator()
    public init(playerID: UUID, profile: BotProfile = BotProfile()) { self.playerID = playerID; self.profile = profile }

    private var skillFactor: Double { [.novice: 0.38, .competent: 0.58, .expert: 0.78, .historian: 0.91][profile.skill]! }
    public func buzzIntent(for clue: Clue) -> BotBuzzIntent? {
        let familiarity = estimateConfidence(for: clue)
        let threshold = [.cautious: 0.72, .normal: 0.57, .aggressive: 0.43, .reckless: 0.28][profile.risk]!
        guard familiarity >= threshold else { return nil }
        let base = 0.28 + (1 - skillFactor) * 0.38
        let jitter = Double.random(in: -0.09...0.14, using: &rng)
        return BotBuzzIntent(playerID: playerID, delay: max(0.12, base + jitter))
    }
    public func answerDecision(for clue: Clue) -> BotAnswerDecision {
        let confidence = estimateConfidence(for: clue)
        guard confidence > 0.34 else { return BotAnswerDecision(answer: plausibleWrongAnswer(for: clue), confidence: confidence, latency: reactionLatency()) }
        if !clue.options.isEmpty {
            let answer = confidence > 0.62 ? clue.options[clue.correctOptionIndex] : plausibleWrongAnswer(for: clue)
            return BotAnswerDecision(answer: answer, confidence: confidence, latency: reactionLatency())
        }
        return BotAnswerDecision(answer: confidence > 0.62 ? clue.canonicalAnswer : plausibleWrongAnswer(for: clue), confidence: confidence, latency: reactionLatency())
    }
    public func wager(score: Int, clueValue: Int, confidence: Double, final: Bool = false) -> Int {
        let fraction = [.cautious: 0.18, .normal: 0.38, .aggressive: 0.68, .reckless: 0.95][profile.risk]!
        let cap = final ? max(0, score) : clueValue
        return min(cap, max(0, Int(Double(max(0, score)) * fraction * confidence)))
    }
    public func chooseCategory(_ clues: [Clue]) -> String? { clues.sorted { estimateConfidence(for: $0) > estimateConfidence(for: $1) }.first?.category }
    private func estimateConfidence(for clue: Clue) -> Double {
        var value = skillFactor
        if profile.specialties.contains(clue.theme) || profile.specialties.contains(clue.category) { value += 0.16 }
        if profile.weaknesses.contains(clue.theme) || profile.weaknesses.contains(clue.category) { value -= 0.20 }
        value -= Double(clue.difficulty.rawValue.count % 4) * 0.025
        return min(0.98, max(0.05, value + profile.confidenceBias + Double.random(in: -0.08...0.08, using: &rng)))
    }
    private func plausibleWrongAnswer(for clue: Clue) -> String? { clue.options.first(where: { $0 != clue.canonicalAnswer }) ?? clue.distractorRationales.first?.option }
    private func reactionLatency() -> TimeInterval { max(0.18, 0.32 + (1 - skillFactor) * 0.35 + Double.random(in: -0.08...0.18, using: &rng)) }
}
