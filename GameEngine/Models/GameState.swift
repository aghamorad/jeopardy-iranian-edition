import Foundation

public extension Notification.Name {
    static let gameBuzzAccepted = Notification.Name("gameBuzzAccepted")
}
import Combine

public enum GameScreenPhase: Equatable {
    case lobby
    case board
    case clueReading(clue: Clue)
    case buzzerArmed(clue: Clue)
    case answering(player: Player, clue: Clue, remainingSeconds: Double)
    case specialWager(player: Player, clue: Clue)
    case evaluating(player: Player, clue: Clue)
    case clueResolved(clue: Clue, winner: Player?, hostRemark: String, explanation: String)
    case finalWager
    case finalClue(category: String, clue: Clue)
    case finalAnswering(player: Player, clue: Clue)
    case finalReveal(clue: Clue, winner: Player?)
    case inspector(clue: Clue, returnTo: Box<GameScreenPhase>)
}

// Helper wrapper for recursive enum
public final class Box<T>: Equatable where T: Equatable {
    public let value: T
    public init(_ value: T) { self.value = value }
    public static func == (lhs: Box<T>, rhs: Box<T>) -> Bool {
        lhs.value == rhs.value
    }
}

public final class GameState: ObservableObject {
    @Published public var configuration: GameConfiguration
    @Published public var players: [Player]
    @Published public var board: GameBoard
    @Published public var phase: GameScreenPhase = .lobby
    @Published public var activeSlot: BoardSlot?
    @Published public var liveTranscript: String = ""
    @Published public var speechListening: Bool = false
    @Published public var speechErrorMessage: String = ""
    @Published public var hostStatusMessage: String = ""
    @Published public var hostRulingMessage: String = ""
    @Published public var hostRulingIsCorrect: Bool?
    @Published public var currentTurnPlayerIndex: Int = 0
    @Published public var showPerformanceHUD: Bool = false
    @Published public var newPlayerNameInput: String = ""
    @Published public var selectedBoardColumn = 0
    @Published public var selectedBoardRow = 0
    @Published public var manualAnswerInput: String = ""
    @Published public private(set) var round: GameRound = .single
    @Published public private(set) var matchFinished: Bool = false
    @Published public var wagers: [UUID: Int] = [:]
    @Published public var finalDrafts: [UUID: String] = [:]
    @Published public private(set) var finalResponses: Set<UUID> = []
    @Published public private(set) var finalRemaining: Int = 30
    private var finalTimer: Timer?
    private var finalAnswers: [UUID: String] = [:]
    private var botBrains: [UUID: BotContestant] = [:]
    @Published public var activeSpecialWager: Int = 0

    public let buzzerEngine: BuzzerEngine
    public let answerResolver: AnswerResolver
    public var speechEngine: SpeechRecognitionEngine
    public let controllerManager: ControllerManager
    public let performanceMonitor: PerformanceMonitor
    private let boardBuilder: BoardBuilder

    private var answeringTimer: Timer?
    private var cancellables = Set<AnyCancellable>()

    public init(
        configuration: GameConfiguration = GameConfiguration(),
        questionBank: QuestionBank = .shared
    ) {
        self.configuration = configuration
        self.players = [
            Player(name: "Player 1", colorHex: "#C49A45"),
            Player(name: "Player 2", colorHex: "#5B84B1")
        ]
        self.boardBuilder = BoardBuilder(questionBank: questionBank)
        self.board = boardBuilder.buildBoard(
            language: configuration.language,
            mode: configuration.mode,
            difficulty: configuration.difficulty, round: .single
        )
        self.buzzerEngine = BuzzerEngine(prematureLockoutDurationMs: configuration.buzzerLockoutPenaltyMs)
        self.answerResolver = AnswerResolver.shared
        self.speechEngine = WhisperSpeechEngine()
        self.controllerManager = ControllerManager.shared
        self.performanceMonitor = PerformanceMonitor.shared

        for player in players where player.isBot { botBrains[player.id] = BotContestant(playerID: player.id) }

        setupControllerCallbacks()
        controllerManager.requiresOptionHold = { [weak self] in
            guard let self else { return false }
            if case .answering = self.phase { return self.configuration.mode == .multipleChoice }
            return false
        }
    }

    private func setupControllerCallbacks() {
        controllerManager.onAction = { [weak self] action in
            guard let self = self else { return }
            DispatchQueue.main.async {
                switch action {
                case .move(let col, let row):
                    guard self.phase == .board else { return }
                    self.selectedBoardColumn = min(5, max(0, self.selectedBoardColumn + col))
                    self.selectedBoardRow = min(4, max(0, self.selectedBoardRow + row))
                case .primary(let playerIdx):
                    switch self.phase {
                    case .lobby: self.startNewGame()
                    case .board: self.selectSlot(categoryIndex: self.selectedBoardColumn, valueIndex: self.selectedBoardRow)
                    case .answering: self.handleMultipleChoice(playerIndex: playerIdx, optionIndex: 0)
                    case .clueResolved: self.returnToBoard()
                    case .specialWager: self.revealSpecialWager()
                    default: self.handleBuzz(playerIndex: playerIdx)
                    }
                case .buzz(let playerIdx):
                    self.handleBuzz(playerIndex: playerIdx)
                case .back:
                    break
                case .selectOption(let playerIdx, let optionIdx):
                    self.handleMultipleChoice(playerIndex: playerIdx, optionIndex: optionIdx)
                }
            }
        }
    }

    public func leaveMatch() {
        answeringTimer?.invalidate()
        finalTimer?.invalidate()
        speechEngine.stopListening()
        speechListening = false
        HostAudioPlayer.shared.stop()
        phase = .lobby
    }

    public func startNewGame() {
        finalTimer?.invalidate()
        answeringTimer?.invalidate()
        speechEngine.stopListening()
        speechListening = false
        HostAudioPlayer.shared.stop()
        currentTurnPlayerIndex = 0
        activeSlot = nil
        activeSpecialWager = 0
        finalResponses = []
        round = .single
        matchFinished = false
        wagers = [:]
        finalDrafts = [:]
        self.board = boardBuilder.buildBoard(
            language: configuration.language,
            mode: configuration.mode,
            difficulty: configuration.difficulty,
            round: round,
            randomize: true
        )
        for i in 0..<players.count {
            players[i].score = 0
            players[i].isLockedOut = false
            if players[i].isBot { botBrains[players[i].id] = BotContestant(playerID: players[i].id, profile: defaultBotProfile(for: i)) }
        }
        self.phase = .board
        self.hostStatusMessage = "Select a category and clue value."
        self.hostRulingMessage = ""
        self.hostRulingIsCorrect = nil
        persist()
    }

    public func selectSlot(categoryIndex: Int, valueIndex: Int) {
        guard phase == .board else { return }
        guard let slot = board.slot(at: categoryIndex, valueIndex: valueIndex), !slot.isSolved else { return }

        self.activeSpecialWager = 0
        self.manualAnswerInput = ""
        self.liveTranscript = ""
        self.speechErrorMessage = ""
        self.speechListening = false
        self.hostRulingMessage = ""
        self.hostRulingIsCorrect = nil
        self.activeSlot = slot
        if slot.isSpecialWager {
            let player = players[currentTurnPlayerIndex]
            activeSpecialWager = player.isBot ? (botBrains[player.id]?.wager(score: player.score, clueValue: slot.value, confidence: 0.7) ?? slot.value) : 0
            phase = .specialWager(player: player, clue: slot.clue)
            hostStatusMessage = "A sealed wager. \(player.name), choose your stake."
            if player.isBot { DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) { [weak self] in self?.revealSpecialWager() } }
            return
        }
        self.buzzerEngine.resetForNewClue()
        self.phase = .clueReading(clue: slot.clue)
        self.hostStatusMessage = "Reading clue..."

        // The complete clue is visible on the card; written mode keeps the
        // round deterministic and avoids unreliable speech recognition/TTS.
        buzzerEngine.setReading()
        // Six seconds, not one: with the whole clue on the card, nobody can
        // read it and reach the button in a beat. The buzz window opens when
        // the room has had its chance to read.
        DispatchQueue.main.asyncAfter(deadline: .now() + 6.0) { [weak self] in
            guard let self = self, case .clueReading = self.phase else { return }
            self.armBuzzer(for: slot.clue)
        }
    }

    public func revealSpecialWager(amount: Int? = nil) {
        guard case .specialWager(let player, _) = phase, let clue = activeSlot?.clue else { return }
        activeSpecialWager = min(max(0, amount ?? activeSpecialWager), max(max(0, player.score), round == .double ? 200_000_000 : 200_000_000))
        phase = .answering(player: player, clue: clue, remainingSeconds: configuration.answeringTimeoutSeconds)
        startAnsweringWindow(for: player)
    }

    private func armBuzzer(for clue: Clue) {
        self.buzzerEngine.armBuzzer()
        self.phase = .buzzerArmed(clue: clue)
        self.hostStatusMessage = "BUZZERS ARMED!"

        scheduleBotBuzzes(for: clue)
    }

    private func scheduleBotBuzzes(for clue: Clue) {
        // Bots participate through the same buzzer arbitration as humans.
        for (index, player) in players.enumerated() where player.isBot {
            guard let delay = botBrains[player.id]?.buzzIntent(for: clue)?.delay else { continue }
            DispatchQueue.main.asyncAfter(deadline: .now() + delay) { [weak self] in
                guard let self = self, case .buzzerArmed = self.phase else { return }
                self.handleBuzz(playerIndex: index, playSound: false)
            }
        }
    }

    private func defaultBotProfile(for index: Int) -> BotProfile {
        let skills: [BotSkill] = [.novice, .competent, .expert, .historian]
        let risks: [BotRisk] = [.cautious, .normal, .aggressive, .reckless]
        return BotProfile(skill: skills[index % skills.count], risk: risks[index % risks.count])
    }

    public func setBot(_ playerID: UUID, enabled: Bool) {
        guard let index = players.firstIndex(where: { $0.id == playerID }) else { return }
        players[index].isBot = enabled
        if enabled { botBrains[playerID] = BotContestant(playerID: playerID, profile: defaultBotProfile(for: index)) }
        else { botBrains.removeValue(forKey: playerID) }
    }

    public func handleBuzz(playerIndex: Int, playSound: Bool = true) {
        guard players.indices.contains(playerIndex) else { return }
        switch phase { case .buzzerArmed, .clueReading: break; default: return }
        let player = players[playerIndex]

        let result = buzzerEngine.registerBuzz(playerId: player.id, playerName: player.name)
        if result.accepted {
            // Only a physical contestant action should make the lock-in sound.
            // Bots use this same arbitration path, but their scheduled buzzes are silent.
            if playSound {
                NotificationCenter.default.post(name: .gameBuzzAccepted, object: nil)
            }
            if case .playerBuzzed(_, _, _, let latencyMicros) = buzzerEngine.state {
                performanceMonitor.recordBuzzLatency(micros: latencyMicros)
            }
            buzzerEngine.beginAnswering(playerId: player.id)
            self.currentTurnPlayerIndex = playerIndex
            self.startAnsweringWindow(for: player)
        } else {
            // If premature buzz, update status
            if result.reason.contains("Premature") {
                self.hostStatusMessage = "\(player.name): \(result.reason)"
            }
        }
    }

    private func startAnsweringWindow(for player: Player) {
        guard let slot = activeSlot else { return }
        let timeout = configuration.answeringTimeoutSeconds
        self.phase = .answering(player: player, clue: slot.clue, remainingSeconds: timeout)
        self.hostStatusMessage = "\(player.name) buzzed in! Answer now..."
        self.liveTranscript = ""

        if player.isBot {
            let decision = botBrains[player.id]?.answerDecision(for: slot.clue)
            let clueAnswer = decision?.answer ?? slot.clue.canonicalAnswer
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.45) { [weak self] in
                guard let self = self, case .answering(let current, let activeClue, _) = self.phase, current.id == player.id, activeClue.id == slot.clue.id else { return }
                if self.configuration.mode == .multipleChoice {
                    let index = slot.clue.options.firstIndex(of: clueAnswer) ?? self.botWrongOption(for: slot.clue)
                    self.handleMultipleChoice(playerIndex: self.currentTurnPlayerIndex, optionIndex: index)
                } else {
                    self.submitManualOrSimulatedAnswer(clueAnswer)
                }
            }
        }

        // Countdown timer
        answeringTimer?.invalidate()
        var remaining = timeout
        answeringTimer = Timer.scheduledTimer(withTimeInterval: 0.1, repeats: true) { [weak self] timer in
            guard let self = self else { timer.invalidate(); return }
            remaining -= 0.1
            if remaining <= 0 {
                timer.invalidate()
                self.handleAnsweringTimeout(for: player)
            } else {
                if case .answering(let p, let c, _) = self.phase {
                    self.phase = .answering(player: p, clue: c, remainingSeconds: remaining)
                }
            }
        }
    }

    private func botAccuracy(for player: Player) -> Double {
        let n = player.name.lowercased()
        if n.contains("historian") { return 0.86 }
        if n.contains("expert") { return 0.72 }
        if n.contains("novice") { return 0.38 }
        return 0.58
    }

    private func botWrongOption(for clue: Clue) -> Int {
        clue.options.indices.filter { $0 != clue.correctOptionIndex }.randomElement() ?? 0
    }

    private func botGuess(for clue: Clue) -> String {
        clue.acceptedAliases.first ?? clue.options.first(where: { $0 != clue.canonicalAnswer }) ?? "I don't know"
    }

    public func handleMultipleChoice(playerIndex: Int, optionIndex: Int) {
        guard case .answering(let player, let clue, _) = phase,
              configuration.mode == .multipleChoice,
              playerIndex == currentTurnPlayerIndex else { return }

        answeringTimer?.invalidate()
        guard clue.options.indices.contains(optionIndex) else { return }
        let chosenOption = clue.options[optionIndex]
        let isCorrect = (optionIndex == clue.correctOptionIndex)

        processJudgement(isCorrect: isCorrect, player: player, clue: clue, answeredText: chosenOption)
    }

    public func submitManualOrSimulatedAnswer(_ text: String) {
        guard case .answering(let player, let clue, _) = phase else { return }
        answeringTimer?.invalidate()
        speechEngine.stopListening()
        speechListening = false
        evaluateAnswer(transcript: text, player: player, clue: clue)
    }

    public func toggleVoiceAnswer() {
        if speechListening {
            speechEngine.stopListening()
            speechListening = false
            return
        }
        guard case .answering(let player, let clue, _) = phase,
              !player.isBot,
              configuration.mode == .classic else { return }

        speechErrorMessage = ""
        liveTranscript = ""
        do {
            try speechEngine.startListening(
                language: configuration.language == .persian ? "fa" : "en",
                contextVocabulary: [clue.canonicalAnswer] + clue.acceptedAliases,
                onPartial: { [weak self] transcript in
                    DispatchQueue.main.async {
                        guard let self else { return }
                        if !transcript.text.isEmpty {
                            self.liveTranscript = transcript.text
                            self.manualAnswerInput = transcript.text
                        } else if let error = self.speechEngine.lastError {
                            self.speechListening = false
                            self.speechErrorMessage = error
                        }
                    }
                },
                onFinal: { [weak self] transcript in
                    DispatchQueue.main.async {
                        guard let self,
                              case .answering(let activePlayer, let activeClue, _) = self.phase,
                              activePlayer.id == player.id,
                              activeClue.id == clue.id else { return }
                        self.speechListening = false
                        self.liveTranscript = transcript.text
                        self.manualAnswerInput = transcript.text
                        self.submitManualOrSimulatedAnswer(transcript.text)
                    }
                }
            )
            speechListening = true
        } catch {
            speechListening = false
            speechErrorMessage = "Microphone recognition could not start. Type your response instead."
        }
    }

    private func evaluateAnswer(transcript: String, player: Player, clue: Clue) {
        self.phase = .evaluating(player: player, clue: clue)
        let resolution = answerResolver.resolve(utterance: transcript, clue: clue)
        performanceMonitor.record(name: "AnswerResolver", durationMs: resolution.latencyMs)

        switch resolution.result {
        case .correct:
            processJudgement(isCorrect: true, player: player, clue: clue, answeredText: transcript)

        case .incorrect:
            processJudgement(isCorrect: false, player: player, clue: clue, answeredText: transcript)

        case .prompt:
            // Host asks for specificity; resets a brief 3s answering window without penalty!
            self.hostStatusMessage = resolution.specificityClarification ?? "Please be more specific."
            self.phase = .answering(player: player, clue: clue, remainingSeconds: 3.5)
            answeringTimer = Timer.scheduledTimer(withTimeInterval: 3.5, repeats: false) { [weak self] _ in
                guard let self, case .answering(let current, _, _) = self.phase, current.id == player.id else { return }
                self.handleAnsweringTimeout(for: player)
            }
        }
    }

    private func handleAnsweringTimeout(for player: Player) {
        guard let slot = activeSlot else { return }
        speechEngine.stopListening()
        speechListening = false
        processJudgement(isCorrect: false, player: player, clue: slot.clue, answeredText: "(Time Expired)")
    }

    private func processJudgement(isCorrect: Bool, player: Player, clue: Clue, answeredText: String) {
        guard let slot = activeSlot else { return }
        let playerIdx = players.firstIndex(where: { $0.id == player.id }) ?? 0

        if isCorrect {
            let points = slot.isSpecialWager ? activeSpecialWager : slot.value
            players[playerIdx].awardPoints(points)
            board.markSolved(slotId: slot.id)
            buzzerEngine.resolveClue()

            let hostRemark = HostPersona.reactionFor(
                resolution: AnswerResolution(result: .correct, confidence: 1.0, resolutionMethod: "adjudicated", latencyMs: 0),
                clue: clue,
                language: configuration.language
            )

            hostRulingMessage = hostRemark
            hostRulingIsCorrect = true

            self.phase = .clueResolved(clue: clue, winner: players[playerIdx], hostRemark: hostRemark, explanation: clue.explanation)
            if players[playerIdx].isBot { scheduleBotBoardSelection() }
        } else {
            let points = slot.isSpecialWager ? activeSpecialWager : slot.value
            players[playerIdx].deductPoints(points)
            if slot.isSpecialWager {
                board.markSolved(slotId: slot.id)
                buzzerEngine.resolveClue()
                let hostRemark = HostPersona.reactionFor(resolution: AnswerResolution(result: .incorrect, confidence: 1.0, resolutionMethod: "adjudicated", latencyMs: 0), clue: clue, language: configuration.language)
                hostRulingMessage = hostRemark
                hostRulingIsCorrect = false
                self.phase = .clueResolved(clue: clue, winner: nil, hostRemark: hostRemark, explanation: clue.explanation)
                persist()
                activeSpecialWager = 0
                return
            }
            _ = buzzerEngine.recordWrongAnswer(for: player.id)

            let hostRemark = HostPersona.reactionFor(
                resolution: AnswerResolution(result: .incorrect, confidence: 1.0, resolutionMethod: "adjudicated", latencyMs: 0),
                clue: clue,
                language: configuration.language
            )
            hostRulingMessage = hostRemark
            hostRulingIsCorrect = false

            // Reopen buzzer if other players are still eligible
            let allIds = players.map { $0.id }
            let hasRemaining = buzzerEngine.reopenBuzzerIfEligiblePlayers(totalPlayerIds: allIds)

            if hasRemaining {
                self.phase = .buzzerArmed(clue: clue)
                self.hostStatusMessage = "\(hostRemark) Buzzer reopened!"
                scheduleBotBuzzes(for: clue)
            } else {
                // All players got it wrong
                board.markSolved(slotId: slot.id)
                self.phase = .clueResolved(clue: clue, winner: nil, hostRemark: hostRemark, explanation: clue.explanation)
            }
        }
        persist()
        activeSpecialWager = 0
    }

    private func scheduleBotBoardSelection() {
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) { [weak self] in
            guard let self = self, case .clueResolved = self.phase else { return }
            self.returnToBoard()
            guard self.phase == .board, !self.board.isComplete else { return }
            let available = self.board.slots.filter { !$0.isSolved }
            guard let choice = available.max(by: { ($0.clue.value, $0.clue.difficulty.rawValue) < ($1.clue.value, $1.clue.difficulty.rawValue) }) else { return }
            self.selectSlot(categoryIndex: choice.categoryIndex, valueIndex: choice.valueIndex)
        }
    }

    public func passClue() {
        guard case .buzzerArmed(let clue) = phase, let slot = activeSlot else { return }
        board.markSolved(slotId: slot.id)
        buzzerEngine.resolveClue()
        phase = .clueResolved(clue: clue, winner: nil, hostRemark: "The answer was " + clue.canonicalAnswer + ".", explanation: clue.explanation)
        persist()
    }

    public func returnToBoard() {
        if board.isComplete {
            if round == .single {
                round = .double
                board = boardBuilder.buildBoard(
                    language: configuration.language,
                    mode: configuration.mode,
                    difficulty: configuration.difficulty,
                    round: round,
                    randomize: true
                )
                phase = .board
                hostStatusMessage = "Round II: Double Jeopardy! Values rise to 200,000,000 تومان."
            } else {
                beginFinalRound()
                return
            }
            persist()
            activeSpecialWager = 0
            return
        }
        self.phase = .board
        self.activeSlot = nil
        self.liveTranscript = ""
        self.hostStatusMessage = "Select the next clue."
    }

    public func setWager(for playerID: UUID, amount: Int) {
        guard case .finalWager = phase, let player = players.first(where: { $0.id == playerID }) else { return }
        wagers[playerID] = min(max(0, amount), max(0, player.score)); persist()
    }

    public func beginFinalRound() {
        guard round == .double, board.isComplete else { return }
        round = .final
        guard let clue = QuestionBank.shared.randomFinalClue() else { hostStatusMessage = "No Final clues available."; return }
        wagers = Dictionary(uniqueKeysWithValues: players.map { ($0.id, 0) })
        finalDrafts = Dictionary(uniqueKeysWithValues: players.map { ($0.id, "") })
        for player in players where player.isBot {
            let confidence = botBrains[player.id]?.answerDecision(for: clue).confidence ?? 0.5
            wagers[player.id] = botBrains[player.id]?.wager(score: player.score, clueValue: max(0, player.score), confidence: confidence, final: true) ?? 0
        }
        finalResponses = []
        finalAnswers = [:]
        finalRemaining = 30
        phase = .finalWager
        activeSlot = BoardSlot(category: clue.category, categoryIndex: 0, valueIndex: 0, value: 0, clue: clue)
        hostStatusMessage = "Final category revealed: \(clue.category). Enter private wagers."
        persist()
    }

    public func revealFinalClue() {
        guard case .finalWager = phase else { return }
        guard let clue = activeSlot?.clue else { return }
        phase = .finalClue(category: clue.category, clue: clue)
        hostStatusMessage = "Final clue. Wagers are locked."
        finalTimer?.invalidate()
        finalTimer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { [weak self] timer in
            guard let self else { timer.invalidate(); return }
            self.finalRemaining -= 1
            if self.finalRemaining <= 0 { timer.invalidate(); self.finishFinal() }
        }
        for player in players where player.isBot {
            let decision = botBrains[player.id]?.answerDecision(for: clue)
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.0 + Double.random(in: 0...0.8)) { [weak self] in
                guard let self = self, case .finalClue = self.phase else { return }
                self.submitFinalAnswer(playerID: player.id, text: decision?.answer ?? "")
            }
        }
    }

    public func submitFinalAnswer(playerID: UUID, text: String) {
        guard !finalResponses.contains(playerID) else { return }
        switch phase { case .finalClue, .finalAnswering: break; default: return }
        guard let clue = activeSlot?.clue, let index = players.firstIndex(where: { $0.id == playerID }) else { return }
        finalAnswers[playerID] = text
        finalDrafts[playerID] = ""
        finalResponses.insert(playerID)
        if finalResponses.count == players.count { finishFinal() }
    }

    private func finishFinal() {
        guard let clue = activeSlot?.clue, round == .final, !matchFinished else { return }
        finalTimer?.invalidate()
        for index in players.indices {
            let id = players[index].id
            let correct = answerResolver.resolve(utterance: finalAnswers[id] ?? "", clue: clue).result == .correct
            let wager = min(max(0, wagers[id] ?? 0), max(0, players[index].score))
            if correct { players[index].awardPoints(wager) } else { players[index].deductPoints(wager) }
        }
        let best = players.map(\.score).max() ?? 0
        let winners = players.filter { $0.score == best }
        matchFinished = true
        phase = .finalReveal(clue: clue, winner: winners.count == 1 ? winners.first : nil)
        persist()
    }

    public func persist() {
        struct Snapshot: Codable { let configuration: GameConfiguration; let players: [Player]; let board: GameBoard; let round: GameRound }
        let snapshot = Snapshot(configuration: configuration, players: players, board: board, round: round)
        if let data = try? JSONEncoder().encode(snapshot) {
            try? FileManager.default.createDirectory(at: Self.saveURL.deletingLastPathComponent(), withIntermediateDirectories: true)
            try? data.write(to: Self.saveURL, options: .atomic)
        }
    }

    public func restoreSavedGame() {
        struct Snapshot: Codable { let configuration: GameConfiguration; let players: [Player]; let board: GameBoard; let round: GameRound }
        guard let data = try? Data(contentsOf: Self.saveURL), let snapshot = try? JSONDecoder().decode(Snapshot.self, from: data) else { return }
        configuration = snapshot.configuration; players = snapshot.players; board = snapshot.board; round = snapshot.round; phase = .board
        botBrains.removeAll()
        for (index, player) in players.enumerated() where player.isBot {
            botBrains[player.id] = BotContestant(playerID: player.id, profile: defaultBotProfile(for: index))
        }
    }

    public var hasSavedGame: Bool {
        FileManager.default.fileExists(atPath: Self.saveURL.path)
    }

    public func deleteSavedGame() {
        try? FileManager.default.removeItem(at: Self.saveURL)
    }

    private static var saveURL: URL { FileManager.default.urls(for: .applicationSupportDirectory, in: .userDomainMask)[0].appendingPathComponent("JeopardyIranianEdition/match.json") }

    public func inspectProvenance(for clue: Clue) {
        self.phase = .inspector(clue: clue, returnTo: Box(phase))
    }

    public func closeInspector() {
        if case .inspector(_, let returnTo) = phase {
            self.phase = returnTo.value
        } else {
            self.phase = .board
        }
    }
}
