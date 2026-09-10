#if os(macOS)
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
            RootShowView(gameState: gameState, presentation: presentation, onReady: setupKeyboardCapture)
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
                    presentation.beginShow(gameState: gameState)
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
#endif
