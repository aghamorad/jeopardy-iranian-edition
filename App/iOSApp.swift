#if os(iOS)
import SwiftUI
import JeopardyGameEngine

/// The iPhone stage. The show itself is identical to the Mac's — same views,
/// same cues, same clue bank — so this only supplies the things a window provided
/// there: a scene, a screen shaped for a 16:9 broadcast, and an audio session
/// that survives the ringer switch.
@main
struct JeopardyIOSApp: App {
    @StateObject private var gameState = GameState()
    @StateObject private var presentation = PresentationState()
    @Environment(\.scenePhase) private var scenePhase

    init() {
        PlatformApp.configureAudioSession()
    }

    var body: some Scene {
        WindowGroup {
            RootShowView(gameState: gameState, presentation: presentation)
                .statusBarHidden(true)
                .persistentSystemOverlays(.hidden)
                .preferredColorScheme(.dark)
                .ignoresSafeArea()
                .onChange(of: scenePhase) { _, phase in
                    if phase == .active { PlatformApp.activateAudioSession() }
                }
        }
    }
}
#endif
