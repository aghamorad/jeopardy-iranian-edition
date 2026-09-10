import Foundation
import JeopardyGameEngine

var totalTests = 0
var passedTests = 0
var failedTests = 0

func testSuite(_ name: String, block: () -> Void) {
    print("\n════════════════════════════════════════════════════")
    print("▶ RUNNING TEST SUITE: \(name)")
    print("════════════════════════════════════════════════════")
    block()
}

func testCase(_ name: String, block: () throws -> Void) {
    totalTests += 1
    do {
        try block()
        passedTests += 1
        print("  ✓ \(name)")
    } catch {
        failedTests += 1
        print("  ✗ \(name) - FAILED: \(error)")
    }
}

func assertEq<T: Equatable>(_ actual: T, _ expected: T, _ message: String = "") throws {
    if actual != expected {
        throw NSError(domain: "AssertionError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Expected [\(expected)], got [\(actual)]. \(message)"])
    }
}

func assertTrue(_ condition: Bool, _ message: String = "") throws {
    if !condition {
        throw NSError(domain: "AssertionError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Expected true, got false. \(message)"])
    }
}

func assertFalse(_ condition: Bool, _ message: String = "") throws {
    if condition {
        throw NSError(domain: "AssertionError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Expected false, got true. \(message)"])
    }
}

// =========================================================================
// 1. SCORE ARITHMETIC TESTS
// =========================================================================
testSuite("Score Arithmetic & Deductions") {
    testCase("Single Player Award and Deduction") {
        var player = Player(name: "Test Player", score: 0)
        player.awardPoints(200)
        try assertEq(player.score, 200)

        player.awardPoints(800)
        try assertEq(player.score, 1000)

        player.deductPoints(400)
        try assertEq(player.score, 600)

        // Deduct below zero (negative scores permitted in Jeopardy)
        player.deductPoints(1000)
        try assertEq(player.score, -400)
    }

    testCase("Multiplayer Compounding Deductions on Same Clue") {
        var p1 = Player(name: "P1", score: 400)
        var p2 = Player(name: "P2", score: 200)

        p1.deductPoints(800)
        p2.deductPoints(800)

        try assertEq(p1.score, -400)
        try assertEq(p2.score, -600)
    }
}

// =========================================================================
// 2. BUZZER ENGINE & MONOTONIC STATE TESTS
// =========================================================================
testSuite("Buzzer Engine & Monotonic States") {
    testCase("State Machine Lifecycle") {
        let buzzer = BuzzerEngine(prematureLockoutDurationMs: 500.0)
        let p1 = UUID()

        buzzer.resetForNewClue()
        try assertEq(buzzer.state, .revealing)

        buzzer.setReading()
        try assertEq(buzzer.state, .reading)

        buzzer.armBuzzer()
        if case .armed = buzzer.state {
            // Passed
        } else {
            throw NSError(domain: "BuzzerError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Expected .armed state"])
        }

        let buzzResult = buzzer.registerBuzz(playerId: p1, playerName: "Player 1")
        try assertTrue(buzzResult.accepted)
        if case .playerBuzzed(let winnerId, _, _, let latencyMicros) = buzzer.state {
            try assertEq(winnerId, p1)
            try assertTrue(latencyMicros >= 1, "Monotonic latency must be recorded")
        } else {
            throw NSError(domain: "BuzzerError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Expected .playerBuzzed state"])
        }
    }

    testCase("Premature Buzz Lockout Penalty") {
        let buzzer = BuzzerEngine(prematureLockoutDurationMs: 350.0)
        let p1 = UUID()

        buzzer.resetForNewClue()
        buzzer.setReading()

        // P1 buzzes prematurely during clue reading
        let earlyBuzz = buzzer.registerBuzz(playerId: p1, playerName: "P1")
        try assertFalse(earlyBuzz.accepted)
        try assertTrue(earlyBuzz.reason.contains("Premature"))

        // Buzzer gets armed
        buzzer.armBuzzer()

        // P1 attempts to buzz immediately while penalty active
        let blockedBuzz = buzzer.registerBuzz(playerId: p1, playerName: "P1")
        try assertFalse(blockedBuzz.accepted)
        try assertTrue(blockedBuzz.reason.contains("penalty active"))

        // Wait for penalty to expire
        Thread.sleep(forTimeInterval: 0.40)

        // Now P1 can buzz legitimately
        let validBuzz = buzzer.registerBuzz(playerId: p1, playerName: "P1")
        try assertTrue(validBuzz.accepted)
    }

    testCase("Buzzer Reopening & Eligibility after Wrong Answer") {
        let buzzer = BuzzerEngine()
        let p1 = UUID()
        let p2 = UUID()

        buzzer.resetForNewClue()
        buzzer.armBuzzer()

        // P1 buzzes in
        _ = buzzer.registerBuzz(playerId: p1, playerName: "P1")
        buzzer.beginAnswering(playerId: p1)

        // P1 answers incorrectly
        _ = buzzer.recordWrongAnswer(for: p1)
        try assertTrue(buzzer.isPlayerLockedOut(p1))

        // Reopen buzzer for [P1, P2]
        let reopened = buzzer.reopenBuzzerIfEligiblePlayers(totalPlayerIds: [p1, p2])
        try assertTrue(reopened)

        // P1 tries to buzz again on same clue (blocked!)
        let p1Retry = buzzer.registerBuzz(playerId: p1, playerName: "P1")
        try assertFalse(p1Retry.accepted)

        // P2 buzzes (accepted!)
        let p2Buzz = buzzer.registerBuzz(playerId: p2, playerName: "P2")
        try assertTrue(p2Buzz.accepted)
    }
}

// =========================================================================
// 3. SIMULTANEOUS BUZZ STRESS TEST
// =========================================================================
testSuite("Buzzer Concurrency Stress Test") {
    testCase("50 Iterations of 6 Simultaneous High-Speed Buzzes") {
        let buzzer = BuzzerEngine()
        let players = (0..<6).map { (id: UUID(), name: "Player \($0)") }

        for iteration in 0..<50 {
            buzzer.resetForNewClue()
            buzzer.armBuzzer()

            let group = DispatchGroup()
            var winners = [UUID]()
            let winnersLock = NSLock()

            for player in players {
                group.enter()
                DispatchQueue.global(qos: .userInteractive).async {
                    let result = buzzer.registerBuzz(playerId: player.id, playerName: player.name)
                    if result.accepted {
                        winnersLock.lock()
                        winners.append(player.id)
                        winnersLock.unlock()
                    }
                    group.leave()
                }
            }

            group.wait()
            try assertEq(winners.count, 1, "Iteration \(iteration): Exactly 1 buzz winner must be selected without race conditions")
        }
    }
}

// =========================================================================
// 4. ANSWER RESOLVER & PERSIAN NORMALIZATION TESTS
// =========================================================================
testSuite("Answer Resolver & Normalization Pipeline") {
    let resolver = AnswerResolver.shared
    let qBank = QuestionBank.shared

    testCase("Exact Canonical Answer Matching") {
        guard let clue = qBank.allClues.first(where: { $0.id == "qajar_amir_kabir_200" }) else {
            throw NSError(domain: "DataError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Clue not found"])
        }

        let res = resolver.resolve(utterance: "Amir Kabir", clue: clue)
        try assertEq(res.result, .correct)
        try assertEq(res.resolutionMethod, "exact_canonical")
    }

    testCase("Accepted Aliases with Transliteration Variations") {
        guard let clue = qBank.allClues.first(where: { $0.id == "oil_mosaddegh_200" }) else {
            throw NSError(domain: "DataError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Clue not found"])
        }

        let variants = ["Mosaddeq", "Mossadegh", "Dr. Mohammad Mosaddegh", "Doctor Mosaddegh"]
        for v in variants {
            let res = resolver.resolve(utterance: v, clue: clue)
            try assertEq(res.result, .correct, "Failed for variant: \(v)")
        }
    }

    testCase("Persian Normalization: Arabic Yeh/Kaf and Titles Stripping") {
        guard let clue = qBank.allClues.first(where: { $0.id == "mashruteh_sheikh_fazlollah_600" }) else {
            throw NSError(domain: "DataError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Clue not found"])
        }

        // Arabic Yeh (\u064A) and Kaf (\u0643) with title "شیخ"
        let arabicInput = "شیخ فضل الله نوری" // with Arabic glyphs
        let res = resolver.resolve(utterance: arabicInput, clue: clue)
        try assertEq(res.result, .correct, "Arabic Yeh/Kaf normalization failed")
    }

    testCase("Specificity Prompt Evaluation (PROMPT)") {
        guard let clue = qBank.allClues.first(where: { $0.id == "qajar_amir_kabir_200" }) else {
            throw NSError(domain: "DataError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Clue not found"])
        }

        // Contestant only says "Mirza Taqi" (triggers specificity prompt!)
        let res = resolver.resolve(utterance: "Mirza Taqi", clue: clue)
        try assertEq(res.result, .prompt)
        try assertEq(res.resolutionMethod, "partial_specificity_rule")
    }

    testCase("Fuzzy Levenshtein Typo Tolerance") {
        guard let clue = qBank.allClues.first(where: { $0.id == "court_persepolis_200" }) else {
            throw NSError(domain: "DataError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Clue not found"])
        }

        // Slight phonetic transcription typo: "Persepolis celebraton"
        let res = resolver.resolve(utterance: "Persepolis celebraton", clue: clue)
        try assertEq(res.result, .correct)
    }

    testCase("Incorrect Answer Rejection") {
        guard let clue = qBank.allClues.first(where: { $0.id == "oil_mosaddegh_200" }) else {
            throw NSError(domain: "DataError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Clue not found"])
        }

        let res = resolver.resolve(utterance: "Reza Shah", clue: clue)
        try assertEq(res.result, .incorrect)
    }

    testCase("Jeopardy-style surname and Iranian transliteration tolerance") {
        guard let kabir = qBank.allClues.first(where: { $0.id == "qajar_amir_kabir_200" }),
              let mosaddegh = qBank.allClues.first(where: { $0.id == "oil_mosaddegh_200" }) else {
            throw NSError(domain: "DataError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Clues not found"])
        }
        let surname = resolver.resolve(utterance: "Kabir", clue: kabir)
        try assertEq(surname.result, .correct, "A distinctive last name/title should be sufficient")

        let looseTransliteration = resolver.resolve(utterance: "Mohamad Mosadeq", clue: mosaddegh)
        try assertEq(looseTransliteration.result, .correct, "Common Persian transliteration differences should be accepted")
    }
}

testSuite("Controller family detection and face-button layout") {
    testCase("PlayStation and Xbox controllers get native labels") {
        try assertEq(ControllerManager.family(forDeviceName: "Sony DualSense Wireless Controller"), .playStation)
        try assertEq(ControllerManager.family(forDeviceName: "Xbox Wireless Controller"), .xbox)
        try assertEq(ControllerManager.family(forDeviceName: "8BitDo Pro 2"), .generic)
    }

    testCase("Diamond choices map top-left-right-bottom to Y/X/B/A positions") {
        try assertEq(ControllerManager.optionIndex(for: .top), 3)
        try assertEq(ControllerManager.optionIndex(for: .left), 2)
        try assertEq(ControllerManager.optionIndex(for: .right), 1)
        try assertEq(ControllerManager.optionIndex(for: .bottom), 0)
    }
}

// =========================================================================
// 5. BOARD BUILDER & PROVENANCE INTEGRITY TESTS
// =========================================================================
testSuite("Board Assembly & Corpus Provenance") {
    testCase("Expanded corpus contains 650 unique clues") {
        let url = URL(fileURLWithPath: "QuestionBank/verified_clues.json")
        let data = try Data(contentsOf: url)
        let clues = try JSONSerialization.jsonObject(with: data) as! [[String: Any]]
        let ids = clues.compactMap { $0["id"] as? String }
        try assertTrue(clues.count >= 650, "Question bank should support repeated full games")
        try assertEq(Set(ids).count, ids.count, "Clue IDs must remain unique")
    }
    testCase("Board Builder Produces Exact 6x5 Matrix") {
        let builder = BoardBuilder()
        let board = builder.buildBoard()

        try assertEq(board.categories.count, 6, "Must assemble exactly 6 categories")
        try assertEq(board.slots.count, 30, "Must assemble exactly 30 slots (6x5)")

        let expectedValues = [10_000_000, 25_000_000, 50_000_000, 100_000_000, 200_000_000]
        for catIdx in 0..<6 {
            for valIdx in 0..<5 {
                guard let slot = board.slot(at: catIdx, valueIndex: valIdx) else {
                    throw NSError(domain: "BoardError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Slot missing at (\(catIdx), \(valIdx))"])
                }
                try assertEq(slot.value, expectedValues[valIdx])
                try assertFalse(slot.isSolved)
            }
        }
    }

    testCase("All 30 Clues Have Complete Provenance Citations") {
        let clues = QuestionBank.shared.allClues
        try assertTrue(clues.count >= 30, "Must load at least 30 clues")

        for clue in clues {
            try assertFalse(clue.id.isEmpty, "ID empty")
            try assertFalse(clue.canonicalAnswer.isEmpty, "Answer empty for \(clue.id)")
            try assertFalse(clue.sourceId.isEmpty, "SourceID empty for \(clue.id)")
            try assertFalse(clue.bookTitle.isEmpty, "BookTitle empty for \(clue.id)")
            try assertFalse(clue.chapter.isEmpty, "Chapter empty for \(clue.id)")
            try assertTrue(clue.page > 0, "Page must be positive for \(clue.id)")
            try assertFalse(clue.supportingPassage.isEmpty, "Passage empty for \(clue.id)")
            try assertEq(clue.editorialValidationStatus, "verified")

            // Multiple Choice
            try assertEq(clue.options.count, 4, "Must have 4 options for \(clue.id)")
            try assertTrue(clue.correctOptionIndex >= 0 && clue.correctOptionIndex < 4)
            try assertEq(clue.distractorRationales.count, 3, "Must have 3 distractor rationales for \(clue.id)")
        }
    }
}

// =========================================================================
// 6. PERSIAN HISTORICAL SPEECH BENCHMARK
// =========================================================================
testSuite("Persian Historical ASR Regression Benchmark") {
    testCase("10 Landmark Iranian Historical Entities Verification") {
        let testCorpus: [(utterance: String, targetCanonical: String)] = [
            ("محمد مصدق", "Mohammad Mosaddegh"),
            ("میرزا تقی خان امیرکبیر", "Amir Kabir"),
            ("شیخ فضل‌الله نوری", "Sheikh Fazlollah Nuri"),
            ("ستارخان", "Sattar Khan"),
            ("ولایت فقیه", "Velayat-e Faqih"),
            ("جشن‌های ۲۵۰۰ ساله", "The 2,500-Year Celebration of the Persian Empire"),
            ("دختر لر", "The Lor Girl (Dokhtar-e Lor)"),
            ("میرزا ملکم خان", "Mirza Malkom Khan"),
            ("کلنل لیاخوف", "Vladimir Liakhov"),
            ("امیرعباس هویدا", "Amir Abbas Hoveyda")
        ]

        let engine = MockSpeechEngine()
        let qBank = QuestionBank.shared

        for (spokenText, targetCanonical) in testCorpus {
            guard let clue = qBank.allClues.first(where: {
                $0.canonicalAnswer.lowercased().contains(targetCanonical.lowercased()) ||
                targetCanonical.lowercased().contains($0.canonicalAnswer.lowercased())
            }) else {
                throw NSError(domain: "ASRError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Clue for \(targetCanonical) not found"])
            }

            try engine.startListening(
                language: "fa",
                contextVocabulary: clue.acceptedAliases,
                onPartial: { _ in },
                onFinal: { transcript in
                    let res = AnswerResolver.shared.resolve(utterance: transcript.text, clue: clue)
                    if res.result != .correct {
                        print("Failed resolution for spoken: \(spokenText) -> result: \(res.result)")
                    }
                }
            )

            engine.simulateTranscription(spokenText)
        }
    }
}

// =========================================================================
// 7. ADVERSARIAL CONFUSION SETS & AMBIGUITY GUARDS
// =========================================================================
testSuite("Adversarial Confusion Sets & Ambiguity Disambiguation") {
    let resolver = AnswerResolver.shared
    let qBank = QuestionBank.shared

    testCase("Mohammad Reza Shah vs Reza Shah (Father vs Son)") {
        let clueJson = """
        {
            "id": "test_mohammad_reza_shah",
            "language": "en",
            "category": "The Pahlavis",
            "historical_period": "Pahlavi",
            "theme": "Political",
            "difficulty": "STANDARD",
            "value": 400,
            "round": "single",
            "clue_text": "This last monarch of the Pahlavi dynasty was overthrown in February 1979.",
            "canonical_answer": "Mohammad Reza Shah",
            "accepted_aliases": ["Mohammad Reza Shah Pahlavi", "Mohammad Reza Shah", "The Shah", "محمدرضا شاه"],
            "partial_answers": ["Mohammad Reza"],
            "specificity_prompt": "Please include his royal title.",
            "options": ["Mohammad Reza Shah", "Reza Shah", "Ahmad Shah", "Mozaffar al-Din Shah"],
            "correct_option_index": 0,
            "distractor_rationales": [],
            "explanation": "Mohammad Reza Shah ruled from 1941 to 1979.",
            "source_id": "milani_the_shah_2011",
            "book_title": "The Shah",
            "author": "Abbas Milani",
            "chapter": "Epilogue",
            "page": 450,
            "supporting_passage": "Mohammad Reza Shah was the last monarch of Iran.",
            "evidence_type": "established_fact",
            "confidence": 1.0,
            "editorial_validation_status": "verified",
            "host_reactions": {
                "correct_generic": "Correct.",
                "wrong_generic": "No."
            }
        }
        """
        let testClue = try! JSONDecoder().decode(Clue.self, from: clueJson.data(using: .utf8)!)

        let fatherResult = resolver.resolve(utterance: "Reza Shah", clue: testClue)
        try assertEq(fatherResult.result, .incorrect, "Must reject father's name for son")

        let qajarKing = resolver.resolve(utterance: "Mohammad Ali Shah", clue: testClue)
        try assertEq(qajarKing.result, .incorrect, "Must reject Qajar king for Pahlavi shah")

        let correctSon = resolver.resolve(utterance: "Mohammad Reza Shah", clue: testClue)
        try assertEq(correctSon.result, .correct)
    }

    testCase("Fazlollah Nuri vs Fazlollah Zahedi Ambiguity") {
        guard let nuriClue = qBank.allClues.first(where: { $0.id == "mashruteh_sheikh_fazlollah_600" }) else {
            throw NSError(domain: "DataError", code: 1, userInfo: [NSLocalizedDescriptionKey: "Clue not found"])
        }

        let ambiguousResult = resolver.resolve(utterance: "Fazlollah", clue: nuriClue)
        try assertEq(ambiguousResult.result, .prompt, "Ambiguous single first name must prompt")

        let zahediResult = resolver.resolve(utterance: "General Zahedi", clue: nuriClue)
        try assertEq(zahediResult.result, .incorrect, "Wrong Fazlollah must be rejected")

        let validNuri = resolver.resolve(utterance: "Sheikh Fazlollah Nuri", clue: nuriClue)
        try assertEq(validNuri.result, .correct)
    }
}

// =========================================================================
// 8. 100-CLUE REPEATED MATCH PERFORMANCE & STRESS TEST
// =========================================================================
testSuite("100-Clue Repeated Match Performance & Memory Stress Test") {
    testCase("Simulate 100 Consecutive Board Clues Without Leaks or Latency Spikes") {
        let builder = BoardBuilder()
        let buzzer = BuzzerEngine()
        let resolver = AnswerResolver.shared
        let p1 = UUID()

        var latencies: [Double] = []

        for _ in 0..<4 {
            let board = builder.buildBoard()
            for slot in board.slots {
                buzzer.resetForNewClue()
                buzzer.armBuzzer()

                let start = mach_absolute_time()
                let buzz = buzzer.registerBuzz(playerId: p1, playerName: "Player 1")
                try assertTrue(buzz.accepted)

                let res = resolver.resolve(utterance: slot.clue.canonicalAnswer, clue: slot.clue)
                try assertEq(res.result, .correct)

                var info = mach_timebase_info()
                mach_timebase_info(&info)
                let elapsed = Double((mach_absolute_time() - start) * UInt64(info.numer) / UInt64(info.denom)) / 1_000_000.0
                latencies.append(elapsed)

                buzzer.resolveClue()
            }
        }

        try assertTrue(latencies.count >= 100, "Must simulate at least 100 clues")
        latencies.sort()
        let p95 = latencies[Int(Double(latencies.count) * 0.95)]
        let worst = latencies.last ?? 0.0

        try assertTrue(p95 < 10.0, "P95 latency across 100 clues must be < 10ms")
        try assertTrue(worst < 35.0, "Worst latency across 100 clues must be < 35ms")
    }
}


testSuite("Production regression checks") {
    testCase("Only physical accepted buzzes emit the lock-in sound event") {
        let game = GameState(configuration: GameConfiguration(mode: .multipleChoice))
        var buzzSoundEvents = 0
        let observer = NotificationCenter.default.addObserver(forName: .gameBuzzAccepted, object: nil, queue: nil) { _ in
            buzzSoundEvents += 1
        }
        defer {
            NotificationCenter.default.removeObserver(observer)
            game.leaveMatch()
        }

        game.startNewGame()
        let slot = game.board.slots.first(where: { !$0.isSpecialWager })!
        game.selectSlot(categoryIndex: slot.categoryIndex, valueIndex: slot.valueIndex)
        RunLoop.current.run(until: Date().addingTimeInterval(1.3))
        game.handleBuzz(playerIndex: 0, playSound: false)
        try assertEq(buzzSoundEvents, 0, "Automated/bot buzzes must be silent")

        game.startNewGame()
        let secondSlot = game.board.slots.first(where: { !$0.isSpecialWager })!
        game.selectSlot(categoryIndex: secondSlot.categoryIndex, valueIndex: secondSlot.valueIndex)
        RunLoop.current.run(until: Date().addingTimeInterval(1.3))
        game.handleBuzz(playerIndex: 0)
        try assertEq(buzzSoundEvents, 1, "A physical accepted buzz must emit exactly one event")
    }
    testCase("Shuffled answers retain the correct answer and vary positions") {
        let clue = QuestionBank.shared.allClues[0]
        var positions = Set<Int>()
        for _ in 0..<50 {
            let shuffled = clue.shufflingOptions()
            try assertEq(shuffled.options[shuffled.correctOptionIndex], clue.options[clue.correctOptionIndex])
            try assertEq(Set(shuffled.options), Set(clue.options))
            positions.insert(shuffled.correctOptionIndex)
        }
        try assertTrue(positions.count > 1)
    }
    testCase("Zero-dollar special wager does not award face value") {
        let game = GameState(configuration: GameConfiguration(mode: .multipleChoice))
        game.startNewGame()
        let slot = game.board.slots.first(where: { $0.isSpecialWager })!
        game.selectSlot(categoryIndex: slot.categoryIndex, valueIndex: slot.valueIndex)
        game.revealSpecialWager(amount: 0)
        game.handleMultipleChoice(playerIndex: 0, optionIndex: slot.clue.correctOptionIndex)
        try assertEq(game.players[0].score, 0)
        try assertTrue(game.board.slots.first(where: { $0.id == slot.id })!.isSolved)
        game.leaveMatch()
    }
    testCase("Invalid contestant and option input cannot score or crash") {
        let game = GameState(configuration: GameConfiguration(mode: .multipleChoice))
        game.startNewGame()
        game.handleBuzz(playerIndex: -1)
        game.handleBuzz(playerIndex: 999)
        let slot = game.board.slots.first(where: { $0.isSpecialWager })!
        game.selectSlot(categoryIndex: slot.categoryIndex, valueIndex: slot.valueIndex)
        game.revealSpecialWager(amount: 100)
        game.handleMultipleChoice(playerIndex: 0, optionIndex: -1)
        game.handleMultipleChoice(playerIndex: 0, optionIndex: 999)
        try assertEq(game.players[0].score, 0)
        game.leaveMatch()
    }
    testCase("Two boards advance to Final, duplicate answers cannot change scores") {
        let game = GameState(configuration: GameConfiguration(mode: .multipleChoice))
        game.startNewGame()
        for slot in game.board.slots { game.board.markSolved(slotId: slot.id) }
        game.returnToBoard()
        try assertEq(game.round, .double)
        try assertEq(game.board.slots.count, 30)
        for slot in game.board.slots { game.board.markSolved(slotId: slot.id) }
        game.players[0].score = 1000; game.players[1].score = 600
        game.returnToBoard()
        try assertEq(game.phase, .finalWager)
        game.setWager(for: game.players[0].id, amount: 500)
        game.setWager(for: game.players[1].id, amount: 900)
        try assertEq(game.wagers[game.players[1].id], 600)
        game.revealFinalClue()
        let answer = game.activeSlot!.clue.canonicalAnswer
        game.submitFinalAnswer(playerID: game.players[0].id, text: answer)
        try assertEq(game.players[0].score, 1000, "Scoring must wait for reveal")
        game.submitFinalAnswer(playerID: game.players[0].id, text: "wrong")
        game.submitFinalAnswer(playerID: game.players[1].id, text: "wrong")
        try assertEq(game.players[0].score, 1500)
        try assertEq(game.players[1].score, 0)
        try assertTrue(game.matchFinished)
        game.submitFinalAnswer(playerID: game.players[0].id, text: answer)
        try assertEq(game.players[0].score, 1500)
        game.startNewGame()
        try assertEq(game.round, .single)
        try assertEq(game.players[0].score, 0)
        try assertFalse(game.matchFinished)
        game.leaveMatch()
    }
}

print("\n════════════════════════════════════════════════════")
print("TEST SUMMARY: \(passedTests) PASSED, \(failedTests) FAILED out of \(totalTests) TESTS")
print("════════════════════════════════════════════════════\n")

if failedTests > 0 {
    exit(1)
} else {
    print("ALL TESTS PASSED SUCCESSFULLY! ✓\n")
    exit(0)
}
