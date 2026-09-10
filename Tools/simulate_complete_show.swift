import Foundation
import JeopardyGameEngine

print("══════════════════════════════════════════════════════════════")
print("▶ SIMULATING FULL BROADCAST MATCH: SINGLE -> DOUBLE -> FINAL")
print("══════════════════════════════════════════════════════════════")

// 1. Verify Question Bank
let qb = QuestionBank.shared
print("Question Bank Total Clues: \(qb.allClues.count)")
let singleClues = qb.allClues.filter { $0.round == .single }
let doubleClues = qb.allClues.filter { $0.round == .double }
let finalClues = qb.allClues.filter { $0.round == .final }
print("  • Single Round Clues: \(singleClues.count) (\(qb.categories(for: .single).count) categories)")
print("  • Double Round Clues: \(doubleClues.count) (\(qb.categories(for: .double).count) categories)")
print("  • Final Round Clues: \(finalClues.count)")

assert(singleClues.count >= 30, "Must have at least 30 Single clues")
assert(doubleClues.count >= 30, "Must have at least 30 Double clues")
assert(finalClues.count >= 4, "Must have at least 4 Final clues")

// 2. Initialize GameState
let config = GameConfiguration(mode: .multipleChoice, language: .english, difficulty: .standard)
let gameState = GameState(configuration: config, questionBank: qb)

// Setup 3 Contestants
gameState.players = [
    Player(name: "Morad (Host)", colorHex: "#C49A45"),
    Player(name: "Simin (Scholar)", colorHex: "#5B84B1", isBot: true),
    Player(name: "Kaveh (Historian)", colorHex: "#D45844", isBot: true)
]

print("\n[STEP 1] Starting Match...")
gameState.startNewGame()
assert(gameState.phase == .board)
assert(gameState.round == .single)
assert(gameState.board.slots.count == 30)
print("  ✓ Single Jeopardy Board assembled with \(gameState.board.categories.count) categories and 30 clues.")

// Check Daily Double in Single Round
let singleWagers = gameState.board.slots.filter { $0.isSpecialWager }
print("  ✓ Single Round Daily Doubles count: \(singleWagers.count)")

// 3. Play through Single Jeopardy board
print("\n[STEP 2] Playing through Single Jeopardy Board...")
for (index, slot) in gameState.board.slots.enumerated() {
    gameState.selectSlot(categoryIndex: slot.categoryIndex, valueIndex: slot.valueIndex)
    if case .specialWager(let player, let clue) = gameState.phase {
        gameState.revealSpecialWager(amount: min(max(0, player.score) + clue.value, 1000))
    }
    if case .clueReading(let clue) = gameState.phase {
        // Human player buzzes in
        gameState.handleBuzz(playerIndex: 0)
    } else if case .buzzerArmed(let clue) = gameState.phase {
        gameState.handleBuzz(playerIndex: 0)
    }

    if case .answering(let player, let clue, _) = gameState.phase {
        // Answer correctly
        gameState.handleMultipleChoice(playerIndex: 0, optionIndex: clue.correctOptionIndex)
    }

    assert(gameState.board.slots[index].isSolved == true)
    gameState.returnToBoard()
}

print("  ✓ Single Jeopardy Board fully cleared. P1 Score: $\(gameState.players[0].score)")
print("  ✓ Transitioned to: \(gameState.round) round (Phase: \(gameState.phase))")

// 4. Verify Transition to Double Jeopardy
assert(gameState.round == .double, "Must transition to Double Jeopardy")
assert(gameState.board.slots.count == 30, "Double board must have 30 slots")
let doubleWagers = gameState.board.slots.filter { $0.isSpecialWager }
print("  ✓ Double Round Daily Doubles count: \(doubleWagers.count)")
assert(doubleWagers.count >= 1, "Must have daily doubles in double round")

// 5. Play through Double Jeopardy board
print("\n[STEP 3] Playing through Double Jeopardy Board...")
for (index, slot) in gameState.board.slots.enumerated() {
    gameState.selectSlot(categoryIndex: slot.categoryIndex, valueIndex: slot.valueIndex)
    if case .specialWager(let player, let clue) = gameState.phase {
        gameState.revealSpecialWager(amount: min(max(0, player.score) + clue.value, 2000))
    }
    if case .clueReading(let clue) = gameState.phase {
        gameState.handleBuzz(playerIndex: index % 3)
    } else if case .buzzerArmed(let clue) = gameState.phase {
        gameState.handleBuzz(playerIndex: index % 3)
    }

    if case .answering(let player, let clue, _) = gameState.phase {
        gameState.handleMultipleChoice(playerIndex: index % 3, optionIndex: clue.correctOptionIndex)
    }

    gameState.returnToBoard()
}

print("  ✓ Double Jeopardy Board fully cleared.")
print("  ✓ Transitioned to: \(gameState.round) round (Phase: \(gameState.phase))")

// 6. Verify Final Jeopardy Transition
assert(gameState.round == .final, "Must be Final round")
assert(gameState.phase == .finalWager, "Phase must be .finalWager")
print("\n[STEP 4] Final Jeopardy Category: \(gameState.activeSlot?.clue.category ?? "")")

// Enter Wagers
for p in gameState.players {
    gameState.setWager(for: p.id, amount: min(p.score, 5000))
    print("  • \(p.name) wagers: $\(gameState.wagers[p.id] ?? 0)")
}

// Reveal Final Clue
gameState.revealFinalClue()
assert(gameState.phase == .finalClue(category: gameState.activeSlot!.clue.category, clue: gameState.activeSlot!.clue))
print("  ✓ Final Clue Revealed: \"\(gameState.activeSlot!.clue.clueText)\"")

// Submit Answers
for p in gameState.players {
    gameState.submitFinalAnswer(playerID: p.id, text: gameState.activeSlot!.clue.canonicalAnswer)
}

// 7. Verify Final Winner Reveal
if case .finalReveal(let clue, let winner) = gameState.phase {
    print("\n[STEP 5] Final Ceremony Reveal:")
    print("  • Canonical Answer: \(clue.canonicalAnswer)")
    print("  • Match Winner: \(winner?.name ?? "Draw") with $\(winner?.score ?? 0)")
    for p in gameState.players {
        print("    - \(p.name): $\(p.score)")
    }
    assert(winner != nil, "Winner must be determined")
} else {
    fatalError("Must be in finalReveal phase")
}

print("\n══════════════════════════════════════════════════════════════")
print("ALL MULTI-ROUND GAMEPLAY FLOWS VERIFIED SUCCESSFULLY! ✓")
print("══════════════════════════════════════════════════════════════\n")
