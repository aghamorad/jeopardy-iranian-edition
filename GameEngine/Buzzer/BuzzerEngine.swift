import Foundation

public enum BuzzerState: Equatable {
    case idle
    case revealing
    case locked
    case reading
    case armed(armedAt: ContinuousClock.Instant)
    case playerBuzzed(playerId: UUID, playerName: String, at: ContinuousClock.Instant, latencyMicroseconds: Int64)
    case answering(playerId: UUID)
    case resolved
}

public struct BuzzAttempt {
    public let playerId: UUID
    public let timestamp: ContinuousClock.Instant
}

public final class BuzzerEngine {
    public private(set) var state: BuzzerState = .idle
    private let clock = ContinuousClock()

    // Configurable premature buzz penalty duration
    public var prematureLockoutDuration: Duration

    // Track locked out players (from wrong answers on current clue)
    public private(set) var clueLockedOutPlayers: Set<UUID> = []

    // Track premature buzz penalties (temporary lockout)
    public private(set) var prematurePenalties: [UUID: ContinuousClock.Instant] = [:]

    // Lock for thread-safe simultaneous buzz arbitration
    private let lock = NSLock()

    public init(prematureLockoutDurationMs: Double = 600.0) {
        self.prematureLockoutDuration = .milliseconds(prematureLockoutDurationMs)
    }

    public func resetForNewClue() {
        lock.lock()
        defer { lock.unlock() }
        state = .revealing
        clueLockedOutPlayers.removeAll()
        prematurePenalties.removeAll()
    }

    public func setReading() {
        lock.lock()
        defer { lock.unlock() }
        if state == .revealing || state == .locked {
            state = .reading
        }
    }

    public func armBuzzer() {
        lock.lock()
        defer { lock.unlock() }
        let now = clock.now
        state = .armed(armedAt: now)
    }

    public func registerBuzz(playerId: UUID, playerName: String) -> (accepted: Bool, reason: String) {
        lock.lock()
        defer { lock.unlock() }

        let now = clock.now

        // 1. Check if already answered wrong on this clue
        if clueLockedOutPlayers.contains(playerId) {
            return (false, "Already locked out for this clue")
        }

        // 2. Check if currently under premature penalty
        if let penaltyUntil = prematurePenalties[playerId], now < penaltyUntil {
            return (false, "Premature buzz penalty active")
        }

        // 3. Check State
        switch state {
        case .revealing, .locked, .reading:
            // Premature buzz! Apply penalty
            prematurePenalties[playerId] = now + prematureLockoutDuration
            return (false, "Premature buzz! Locked out for \(prematureLockoutDuration)")

        case .armed(let armedAt):
            let elapsed = armedAt.duration(to: now).components
            let latencyMicros = max(1, elapsed.seconds * 1_000_000 + elapsed.attoseconds / 1_000_000_000_000)
            state = .playerBuzzed(playerId: playerId, playerName: playerName, at: now, latencyMicroseconds: latencyMicros)
            return (true, "Buzz registered")

        case .playerBuzzed, .answering:
            return (false, "Another player already buzzed")

        case .idle, .resolved:
            return (false, "Buzzer not active")
        }
    }

    public func beginAnswering(playerId: UUID) {
        lock.lock()
        defer { lock.unlock() }
        state = .answering(playerId: playerId)
    }

    public func recordWrongAnswer(for playerId: UUID) -> Bool {
        lock.lock()
        defer { lock.unlock() }
        clueLockedOutPlayers.insert(playerId)
        return true
    }

    public func reopenBuzzerIfEligiblePlayers(totalPlayerIds: [UUID]) -> Bool {
        lock.lock()
        defer { lock.unlock() }

        let remaining = totalPlayerIds.filter { !clueLockedOutPlayers.contains($0) }
        if remaining.isEmpty {
            state = .resolved
            return false
        } else {
            state = .armed(armedAt: clock.now)
            return true
        }
    }

    public func resolveClue() {
        lock.lock()
        defer { lock.unlock() }
        state = .resolved
    }

    public func isPlayerLockedOut(_ playerId: UUID) -> Bool {
        lock.lock()
        defer { lock.unlock() }
        if clueLockedOutPlayers.contains(playerId) { return true }
        if let penaltyUntil = prematurePenalties[playerId], clock.now < penaltyUntil { return true }
        return false
    }
}
