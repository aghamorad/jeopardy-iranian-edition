import SwiftUI
import JeopardyGameEngine

/// The five things you can do from the in-match menu, in the order the cursor
/// steps through them.
public enum MatchMenuItem: Int, CaseIterable {
    case continuePlaying, saveGame, saveAndMenu, newMatch, saveAndQuit

    public var title: String {
        switch self {
        case .continuePlaying: return "CONTINUE PLAYING"
        case .saveGame: return "SAVE GAME"
        case .saveAndMenu: return "SAVE & MAIN MENU"
        case .newMatch: return "NEW MATCH"
        case .saveAndQuit: return "SAVE & QUIT"
        }
    }

    public func advanced(by step: Int) -> MatchMenuItem {
        let count = MatchMenuItem.allCases.count
        let index = (rawValue + step % count + count) % count
        return MatchMenuItem(rawValue: index) ?? .continuePlaying
    }
}

/// Drives the show from outside `GameState`: which curtain is up, which cue has
/// already played, and the match-control overlay. Shared by the macOS window and
/// the iOS scene so both run the identical show.
public final class PresentationState: ObservableObject {
    @Published public var showOpening = true
    @Published public var openingLanguage: GameLanguage = .english
    @Published public var lastCuePhase = ""
    @Published public var showGameMenu = false
    @Published public var savedNotice = false
    @Published public var matchMenuSelection: MatchMenuItem = .continuePlaying
    public var lastRound: GameRound?
    #if os(macOS)
    public var keyMonitor: Any?
    #endif

    /// A view that owns controller input while it is on screen. The lobby sets
    /// this so its own overlays (setup, settings, how-to) stay navigable without
    /// the show having to know they exist.
    public var lobbyMenuHandler: ((ControllerAction) -> Void)?

    public init() {}

    // MARK: - Menus driven by a gamepad

    /// Routes stick and face input into whichever menu currently owns the screen.
    /// Falls through to opening the match menu on the back button.
    public func attachControllers(to manager: ControllerManager, gameState: GameState) {
        manager.isCapturingMenuInput = { [weak self, weak gameState] in
            guard let self, let gameState else { return false }
            if self.showOpening || self.showGameMenu { return true }
            return gameState.phase == .lobby && self.lobbyMenuHandler != nil
        }

        manager.onMenuAction = { [weak self] action in
            guard let self else { return }
            if self.showOpening {
                self.handleOpeningAction(action, gameState: gameState)
            } else if self.showGameMenu {
                self.handleMatchMenuAction(action, gameState: gameState)
            } else if gameState.phase == .lobby, let handler = self.lobbyMenuHandler {
                handler(action)
            } else if case .back = action {
                self.openMatchMenu(gameState: gameState)
            }
        }
    }

    public func beginShow(gameState: GameState) {
        gameState.configuration.language = openingLanguage
        withAnimation(.easeInOut(duration: 0.65)) { showOpening = false }
    }

    public func openMatchMenu(gameState: GameState) {
        guard !showOpening, gameState.phase != .lobby else { return }
        matchMenuSelection = .continuePlaying
        showGameMenu = true
    }

    private func handleOpeningAction(_ action: ControllerAction, gameState: GameState) {
        switch action {
        case .move(let column, _):
            if column < 0 { openingLanguage = .english }
            if column > 0 { openingLanguage = .persian }
        case .primary, .buzz:
            beginShow(gameState: gameState)
        default:
            break
        }
    }

    private func handleMatchMenuAction(_ action: ControllerAction, gameState: GameState) {
        switch action {
        case .move(_, let row):
            matchMenuSelection = matchMenuSelection.advanced(by: row)
        case .primary, .buzz:
            runMatchMenuAction(matchMenuSelection, gameState: gameState)
        case .back:
            showGameMenu = false
        default:
            break
        }
    }

    /// The single definition of what each menu entry does, shared by the mouse
    /// and the gamepad so the two can never drift apart.
    public func runMatchMenuAction(_ item: MatchMenuItem, gameState: GameState) {
        switch item {
        case .continuePlaying:
            showGameMenu = false
        case .saveGame:
            gameState.persist()
            savedNotice = true
            DispatchQueue.main.asyncAfter(deadline: .now() + 1.4) { [weak self] in
                self?.savedNotice = false
            }
        case .saveAndMenu:
            gameState.persist()
            showGameMenu = false
            gameState.leaveMatch()
        case .newMatch:
            showGameMenu = false
            gameState.leaveMatch()
        case .saveAndQuit:
            gameState.persist()
            PlatformApp.quit()
        }
    }
}

public struct RootShowView: View {
    @ObservedObject var gameState: GameState
    @ObservedObject var presentation: PresentationState
    var onReady: () -> Void

    public init(gameState: GameState, presentation: PresentationState, onReady: @escaping () -> Void = {}) {
        self.gameState = gameState
        self.presentation = presentation
        self.onReady = onReady
    }

    public var body: some View {
        ZStack(alignment: .topTrailing) {
            ZStack {
                if presentation.showOpening {
                    OpeningView(selectedLanguage: $presentation.openingLanguage) { language in
                        presentation.openingLanguage = language
                        presentation.beginShow(gameState: gameState)
                    }
                } else {
                    ArchivalBackdrop()
                    Group {
                        switch gameState.phase {
                        case .lobby:
                            ReferenceLobbyView(gameState: gameState, presentation: presentation)

                        case .board:
                            ReferenceBoardView(gameState: gameState)

                        case .clueReading, .buzzerArmed, .answering, .evaluating, .clueResolved, .specialWager, .finalWager, .finalClue, .finalAnswering, .finalReveal:
                            ReferenceClueView(gameState: gameState)

                        case .inspector(let clue, _):
                            SourceInspectorView(clue: clue) {
                                gameState.closeInspector()
                            }
                        }
                    }
                }
            }
            .modifier(StageFrame())
            .background(ArchivalTheme.studioDark)

            if gameState.showPerformanceHUD && gameState.phase != .lobby {
                PerformanceHUDView()
                    .padding(16)
            }

            if !presentation.showOpening && gameState.phase != .lobby {
                Button("MENU") { presentation.showGameMenu.toggle() }
                    .font(.system(size: 11, weight: .bold))
                    .tracking(2.5)
                    .buttonStyle(.plain)
                    .foregroundColor(.white.opacity(0.78))
                    .padding(.horizontal, 16)
                    .frame(height: 34)
                    .background(Color.black.opacity(0.78))
                    .overlay(RoundedRectangle(cornerRadius: 4).stroke(.white.opacity(0.28), lineWidth: 1))
                    .padding(18)
            }

            if presentation.showGameMenu {
                FullScreenMatchMenu(
                    gameState: gameState,
                    selection: presentation.matchMenuSelection,
                    onContinue: { presentation.runMatchMenuAction(.continuePlaying, gameState: gameState) },
                    onSave: { presentation.runMatchMenuAction(.saveGame, gameState: gameState) },
                    onSaveAndMenu: { presentation.runMatchMenuAction(.saveAndMenu, gameState: gameState) },
                    onNewMatch: { presentation.runMatchMenuAction(.newMatch, gameState: gameState) },
                    onQuit: { presentation.runMatchMenuAction(.saveAndQuit, gameState: gameState) }
                )
            }

            if presentation.savedNotice {
                Text("GAME SAVED")
                    .font(.system(size: 12, weight: .bold)).tracking(3)
                    .foregroundColor(.white)
                    .padding(.horizontal, 24).padding(.vertical, 13)
                    .background(Color.black.opacity(0.92))
                    .overlay(RoundedRectangle(cornerRadius: 5).stroke(.green, lineWidth: 1))
                    .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .bottom)
                    .padding(.bottom, 36)
            }
        }
        .environment(\.layoutDirection, gameState.configuration.language == .persian ? .rightToLeft : .leftToRight)
        .onAppear {
            presentation.attachControllers(to: gameState.controllerManager, gameState: gameState)
            onReady()
        }
        .animation(.easeInOut(duration: 0.22), value: gameState.phase)
        .onChange(of: gameState.phase) { _, phase in advanceShow(to: phase) }
    }

    /// The show's cue sheet: music, bumpers and host dialogue per phase.
    private func advanceShow(to phase: GameScreenPhase) {
        let cueKey: String
        switch phase {
        case .answering(let player, let clue, _): cueKey = "answer-\(player.id)-\(clue.id)"
        case .board: cueKey = "board"
        default: cueKey = String(describing: phase)
        }
        guard cueKey != presentation.lastCuePhase else { return }
        presentation.lastCuePhase = cueKey
        switch phase {
        case .board:
            TheatreDirector.shared.startGameplayMusic()
            if presentation.lastRound != gameState.round {
                presentation.lastRound = gameState.round
                TheatreDirector.shared.playBumper(for: gameState.round)
            }
        case .lobby:
            presentation.lastRound = nil
            presentation.showGameMenu = false
            TheatreDirector.shared.startMenuMusic()
        case .clueReading:
            OstadFaniEngine.shared.currentDialogue = "Read carefully. The light opens the buzzers."
            TheatreDirector.shared.startThinkingMusic()
        case .buzzerArmed:
            OstadFaniEngine.shared.currentDialogue = "The floor is open. Who has it?"
        case .answering(let player, _, _):
            OstadFaniEngine.shared.currentDialogue = player.name + ", your answer."
        case .specialWager:
            TheatreDirector.shared.startThinkingMusic()
            TheatreDirector.shared.play(.wager)
        case .clueResolved(_, let winner, let remark, _):
            OstadFaniEngine.shared.currentDialogue = remark
            if let winner {
                OstadFaniEngine.shared.reactToAnswer(player: winner.name, correct: true, value: gameState.activeSlot?.value ?? 0)
            } else {
                OstadFaniEngine.shared.reactToAnswer(player: "Contestant", correct: false, value: gameState.activeSlot?.value ?? 0)
            }
            TheatreDirector.shared.play(winner == nil ? .incorrect : .correct)
        case .finalWager:
            TheatreDirector.shared.startGameplayMusic()
            TheatreDirector.shared.play(.finalRound)
        case .finalClue:
            TheatreDirector.shared.startFinalThinkMusic()
        case .finalReveal:
            if let winner = gameState.players.max(by: { $0.score < $1.score }) {
                OstadFaniEngine.shared.sayVictory(champion: winner.name)
            }
            TheatreDirector.shared.playVictoryCelebration()
        default:
            break
        }
    }
}

/// The stage floor is a 16:9 broadcast canvas. On macOS it wants a real window.
/// On iOS the phone is a different shape entirely (19.5:9), so the whole show is
/// laid out at the broadcast resolution and scaled down as one piece. Every view
/// inside already sizes itself against that canvas, so the composition — and the
/// tap targets positioned on the plate — land exactly where they do on the Mac.
private struct StageFrame: ViewModifier {
    private static let canvas = CGSize(width: 1672, height: 941)

    func body(content: Content) -> some View {
        #if os(macOS)
        content.frame(minWidth: 1100, minHeight: 620)
        #else
        GeometryReader { proxy in
            let scale = min(
                proxy.size.width / Self.canvas.width,
                proxy.size.height / Self.canvas.height
            )
            content
                .frame(width: Self.canvas.width, height: Self.canvas.height)
                .scaleEffect(scale)
                .frame(width: proxy.size.width, height: proxy.size.height)
        }
        #endif
    }
}

public struct FullScreenMatchMenu: View {
    @ObservedObject var gameState: GameState
    let selection: MatchMenuItem
    let onContinue: () -> Void
    let onSave: () -> Void
    let onSaveAndMenu: () -> Void
    let onNewMatch: () -> Void
    let onQuit: () -> Void
    @ObservedObject private var controllers = ControllerManager.shared
    @Namespace private var shine

    /// What to tell the player to press, in their pad's own alphabet.
    private var padHint: String? {
        guard !controllers.connectedControllers.isEmpty else { return nil }
        let glyphs = controllers.glyphs(forPlayerIndex: 0) ?? ControllerManager.fallbackGlyphs
        return "STICK / D-PAD MOVE  ·  \(glyphs.bottom) SELECT  ·  \(glyphs.right) BACK"
    }

    public init(
        gameState: GameState,
        selection: MatchMenuItem = .continuePlaying,
        onContinue: @escaping () -> Void,
        onSave: @escaping () -> Void,
        onSaveAndMenu: @escaping () -> Void,
        onNewMatch: @escaping () -> Void,
        onQuit: @escaping () -> Void
    ) {
        self.gameState = gameState
        self.selection = selection
        self.onContinue = onContinue
        self.onSave = onSave
        self.onSaveAndMenu = onSaveAndMenu
        self.onNewMatch = onNewMatch
        self.onQuit = onQuit
    }

    private func item(_ entry: MatchMenuItem, action: @escaping () -> Void) -> some View {
        Button(entry.title, action: action)
            .buttonStyle(ReferenceOutlineButtonStyle())
            .selectionShine(selection == entry, in: shine)
    }

    public var body: some View {
        ZStack {
            ArchivalBackdrop()
                .overlay(Color.black.opacity(0.42))
                .ignoresSafeArea()

            GeometryReader { proxy in
                let compact = proxy.size.width < 1180
                VStack(spacing: 0) {
                    HStack(alignment: .top) {
                        VStack(alignment: .leading, spacing: 7) {
                            Text("JEOPARDY! IRANIAN EDITION")
                                .font(.system(size: compact ? 21 : 27, weight: .black, design: .rounded))
                                .tracking(3)
                                .foregroundStyle(
                                    LinearGradient(colors: [.green, .white, .red], startPoint: .leading, endPoint: .trailing)
                                )
                            Text("MATCH CONTROL ROOM")
                                .font(.system(size: 11, weight: .bold))
                                .tracking(4)
                                .foregroundColor(.white.opacity(0.62))
                        }
                        Spacer()
                        VStack(alignment: .trailing, spacing: 5) {
                            Text("ROUND \(gameState.round.rawValue.uppercased())")
                                .font(.system(size: 12, weight: .bold)).tracking(2)
                            Text(statusLine)
                                .font(.system(size: 13, design: .serif))
                                .foregroundColor(.white.opacity(0.68))
                        }
                    }
                    .padding(.bottom, 22)

                    Rectangle()
                        .fill(LinearGradient(colors: [.green, .white.opacity(0.75), .red], startPoint: .leading, endPoint: .trailing))
                        .frame(height: 2)
                        .padding(.bottom, 24)

                    HStack(alignment: .top, spacing: compact ? 24 : 42) {
                        VStack(alignment: .leading, spacing: 14) {
                            Text("CONTESTANTS")
                                .font(.system(size: 11, weight: .bold)).tracking(3)
                                .foregroundColor(.white.opacity(0.62))
                            ForEach(Array(gameState.players.enumerated()), id: \.element.id) { index, player in
                                contestantCard(index: index, player: player)
                            }
                            Spacer(minLength: 0)
                        }
                        .frame(maxWidth: compact ? 370 : 440, alignment: .leading)

                        VStack(alignment: .leading, spacing: 12) {
                            Text("ON AIR")
                                .font(.system(size: 11, weight: .bold)).tracking(3)
                                .foregroundColor(.white.opacity(0.62))
                            Text(onAirTitle)
                                .font(.system(size: compact ? 24 : 31, weight: .semibold, design: .serif))
                                .foregroundColor(.white)
                            Text(onAirDetail)
                                .font(.system(size: 14, design: .serif))
                                .foregroundColor(.white.opacity(0.65))
                                .fixedSize(horizontal: false, vertical: true)
                                .padding(.bottom, 12)

                            VStack(spacing: 11) {
                                item(.continuePlaying, action: onContinue)
                                HStack(spacing: 11) {
                                    item(.saveGame, action: onSave)
                                    item(.saveAndMenu, action: onSaveAndMenu)
                                }
                                HStack(spacing: 11) {
                                    item(.newMatch, action: onNewMatch)
                                    item(.saveAndQuit, action: onQuit)
                                }
                            }
                            .frame(maxWidth: 620)
                            .animation(.easeInOut(duration: 0.14), value: selection)
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    Spacer(minLength: 0)
                    HStack {
                        Text("HOST  ·  BIBI ZANGZADEH")
                        Spacer()
                        if let padHint {
                            Text(padHint)
                        } else {
                            #if os(macOS)
                            Text("ESC TO RETURN  ·  CMD+S TO SAVE")
                            #else
                            Text("TAP AN OPTION TO RETURN")
                            #endif
                        }
                    }
                    .font(.system(size: 10, weight: .bold)).tracking(2)
                    .foregroundColor(.white.opacity(0.46))
                    .padding(.top, 22)
                }
                .padding(.horizontal, compact ? 34 : 72)
                .padding(.vertical, compact ? 28 : 48)
            }
        }
        .foregroundColor(.white)
        .transition(.opacity)
    }

    private var statusLine: String {
        if gameState.hasSavedGame { return "SAVED MATCH AVAILABLE" }
        return "LIVE MATCH · \(gameState.players.count) CONTESTANTS"
    }

    private var onAirTitle: String {
        switch gameState.phase {
        case .board: return "The board is waiting."
        case .clueReading, .buzzerArmed: return "The clue is in the lights."
        case .answering: return "A contestant has the floor."
        case .specialWager, .finalWager: return "Wagers are being sealed."
        case .finalClue, .finalAnswering: return "Final Jeopardy is live."
        case .finalReveal: return "The archive has rendered its verdict."
        default: return "The studio is on standby."
        }
    }

    private var onAirDetail: String {
        if let slot = gameState.activeSlot {
            return "\(slot.clue.category)  ·  \(formatted(slot.value)) تومان"
        }
        return "Choose Continue Playing when you are ready to return to the stage."
    }

    private func contestantCard(index: Int, player: Player) -> some View {
        HStack(spacing: 13) {
            Text(String(format: "%02d", index + 1))
                .font(.system(size: 12, weight: .black, design: .monospaced))
                .foregroundColor(index.isMultiple(of: 2) ? .green : .red)
                .frame(width: 26)
            VStack(alignment: .leading, spacing: 4) {
                Text(player.name.isEmpty ? "CONTESTANT \(index + 1)" : player.name.uppercased())
                    .font(.system(size: 14, weight: .bold)).tracking(1.2)
                Text(player.isBot ? "AUTOMATED OPPONENT" : "HUMAN CONTESTANT")
                    .font(.system(size: 9, weight: .semibold)).tracking(1.5)
                    .foregroundColor(.white.opacity(0.48))
            }
            Spacer()
            Text(formatted(player.score))
                .font(.system(size: 16, weight: .bold, design: .monospaced))
                .foregroundColor(.white.opacity(0.9))
        }
        .padding(.horizontal, 15).padding(.vertical, 13)
        .background(Color.black.opacity(0.48))
        .overlay(RoundedRectangle(cornerRadius: 5).stroke(.white.opacity(0.2), lineWidth: 1))
    }

    private func formatted(_ value: Int) -> String {
        let formatter = NumberFormatter()
        formatter.numberStyle = .decimal
        formatter.groupingSeparator = ","
        return formatter.string(from: NSNumber(value: value)) ?? "0"
    }
}
