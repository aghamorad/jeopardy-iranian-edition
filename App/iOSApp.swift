#if os(iOS)
import SwiftUI
import AVFoundation

/// The iPhone and iPad app is the same web show in a window — see `ShowWebView`.
@main
struct JeopardyIOSApp: App {
    @Environment(\.scenePhase) private var scenePhase

    init() { ShowAudio.claim() }

    var body: some Scene {
        WindowGroup {
            ShowWebView()
                .statusBarHidden(true)
                .persistentSystemOverlays(.hidden)
                .preferredColorScheme(.dark)
                .ignoresSafeArea()
                .onChange(of: scenePhase) { _, phase in
                    if phase == .active { ShowAudio.claim() }
                }
        }
    }
}

/// A game show with the ringer switch on should still be a game show. `.playback`
/// is the category that ignores the silent switch; the show has no recording to do,
/// so nothing here needs the microphone.
enum ShowAudio {
    static func claim() {
        let session = AVAudioSession.sharedInstance()
        try? session.setCategory(.playback, mode: .moviePlayback)
        try? session.setActive(true)
    }
}
#endif
