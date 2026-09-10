import SwiftUI
import AppKit
import JeopardyGameEngine

@main
public struct AppMain: App {
    @NSApplicationDelegateAdaptor(JeopardyAppDelegate.self) private var appDelegate
    @StateObject private var gameState = GameState()
    @StateObject private var presentation = PresentationState()

    public init() {}

    public var body: some Scene {
        Window("Jeopardy Iranian Edition", id: "main") {
            ZStack(alignment: .topTrailing) {
                ZStack {
                    if presentation.showOpening {
                        OpeningView(selectedLanguage: $presentation.openingLanguage) { language in
                            gameState.configuration.language = language
                            withAnimation(.easeInOut(duration: 0.65)) {
                                presentation.showOpening = false
                            }
                        }
                    } else {
                        ArchivalBackdrop()
                        Group {
                            switch gameState.phase {
                            case .lobby:
                                ReferenceLobbyView(gameState: gameState)

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
                .frame(minWidth: 1100, minHeight: 620)
                .background(ArchivalTheme.studioDark)

                // Performance Telemetry HUD
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
                        onContinue: { presentation.showGameMenu = false },
                        onSave: {
                            gameState.persist()
                            presentation.savedNotice = true
                            DispatchQueue.main.asyncAfter(deadline: .now() + 1.4) { presentation.savedNotice = false }
                        },
                        onSaveAndMenu: {
                            gameState.persist()
                            presentation.showGameMenu = false
                            gameState.leaveMatch()
                        },
                        onNewMatch: {
                            presentation.showGameMenu = false
                            gameState.leaveMatch()
                        },
                        onQuit: {
                            gameState.persist()
                            NSApplication.shared.terminate(nil)
                        }
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
                setupKeyboardCapture()
            }
            .animation(.easeInOut(duration: 0.22), value: gameState.phase)
            .onChange(of: gameState.phase) { _, phase in
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
        .windowStyle(.titleBar)
        .windowToolbarStyle(.unified)
        .defaultSize(width: 1420, height: 800)
        .commands {
            CommandMenu("Match") {
                Button("New match") { gameState.leaveMatch() }.keyboardShortcut("n")
                Button("Continue to board") { if case .clueResolved = gameState.phase { gameState.returnToBoard() } }.keyboardShortcut(.return, modifiers: .command)
                Button("Stop music") { TheatreDirector.shared.stopMusic() }.keyboardShortcut("m", modifiers: [.command, .shift])
            }
        }
    }

    private func setupKeyboardCapture() {
        guard presentation.keyMonitor == nil else { return }
        presentation.keyMonitor = NSEvent.addLocalMonitorForEvents(matching: .keyDown) { event in
            if presentation.showOpening {
                switch event.keyCode {
                case 123, 126:
                    presentation.openingLanguage = .english
                case 124, 125:
                    presentation.openingLanguage = .persian
                case 36, 49:
                    gameState.configuration.language = presentation.openingLanguage
                    withAnimation(.easeInOut(duration: 0.65)) { presentation.showOpening = false }
                default:
                    break
                }
                return nil
            }
            if event.modifierFlags.contains(.command) { return event }
            if NSApp.keyWindow?.firstResponder is NSTextView { return event }
            if gameState.phase == .board {
                switch event.keyCode {
                case 123: gameState.selectedBoardColumn = max(0, gameState.selectedBoardColumn - 1); return nil
                case 124: gameState.selectedBoardColumn = min(5, gameState.selectedBoardColumn + 1); return nil
                case 125: gameState.selectedBoardRow = min(4, gameState.selectedBoardRow + 1); return nil
                case 126: gameState.selectedBoardRow = max(0, gameState.selectedBoardRow - 1); return nil
                case 36, 49: gameState.selectSlot(categoryIndex: gameState.selectedBoardColumn, valueIndex: gameState.selectedBoardRow); return nil
                default: break
                }
            }
            if let chars = event.characters {
                // Cmd+H toggles HUD
                if chars.lowercased() == "h" && event.modifierFlags.contains(.command) {
                    gameState.showPerformanceHUD.toggle()
                    return nil
                }
                // ESC returns from inspector
                if event.keyCode == 53 { // ESC
                    if presentation.showGameMenu {
                        presentation.showGameMenu = false
                        return nil
                    }
                    if case .inspector = gameState.phase {
                        gameState.closeInspector()
                        return nil
                    }
                }
                gameState.controllerManager.handleKeyboardInput(key: chars)
            }
            return event
        }
    }
}

private final class JeopardyAppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.regular)
        DispatchQueue.main.async {
            NSApp.activate(ignoringOtherApps: true)
            NSApp.windows.first?.makeKeyAndOrderFront(nil)
        }
    }

    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool {
        for window in sender.windows {
            window.makeKeyAndOrderFront(nil)
        }
        sender.activate(ignoringOtherApps: true)
        return true
    }
}

private final class PresentationState: ObservableObject {
    @Published var showOpening = true
    @Published var openingLanguage: GameLanguage = .english
    @Published var lastCuePhase = ""
    @Published var showGameMenu = false
    @Published var savedNotice = false
    var lastRound: GameRound?
    var keyMonitor: Any?
}

private struct FullScreenMatchMenu: View {
    @ObservedObject var gameState: GameState
    let onContinue: () -> Void
    let onSave: () -> Void
    let onSaveAndMenu: () -> Void
    let onNewMatch: () -> Void
    let onQuit: () -> Void

    var body: some View {
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
                            Text("ROUND (gameState.round.rawValue.uppercased())")
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
                                Button("CONTINUE PLAYING", action: onContinue)
                                    .buttonStyle(ReferenceOutlineButtonStyle(prominent: true))
                                HStack(spacing: 11) {
                                    Button("SAVE GAME", action: onSave)
                                    Button("SAVE & MAIN MENU", action: onSaveAndMenu)
                                }
                                .buttonStyle(ReferenceOutlineButtonStyle())
                                HStack(spacing: 11) {
                                    Button("NEW MATCH", action: onNewMatch)
                                    Button("SAVE & QUIT", action: onQuit)
                                }
                                .buttonStyle(ReferenceOutlineButtonStyle())
                            }
                            .frame(maxWidth: 620)
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                    }
                    Spacer(minLength: 0)
                    HStack {
                        Text("HOST  ·  BIBI ZANGZADEH")
                        Spacer()
                        Text("ESC TO RETURN  ·  CMD+S TO SAVE")
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
        return "LIVE MATCH · (gameState.players.count) CONTESTANTS"
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
                Text(player.name.isEmpty ? "CONTESTANT (index + 1)" : player.name.uppercased())
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
