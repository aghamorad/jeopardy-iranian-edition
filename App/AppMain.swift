#if os(macOS)
import SwiftUI
import AppKit

/// The Mac app is the web show in a window. There is no second copy of the game
/// anywhere in this project — see `ShowWebView`.
@main
struct JeopardyApp: App {
    @NSApplicationDelegateAdaptor(ShowAppDelegate.self) private var appDelegate

    var body: some Scene {
        Window("Jeopardy Iranian Edition", id: "main") {
            ShowWebView()
                .ignoresSafeArea()
                .preferredColorScheme(.dark)
                .background(Color.black)
        }
        // The show draws its own chrome down to the last hairline, so the window
        // contributes none: no toolbar, no title bar. The traffic lights stay, so
        // there is still a way to close it.
        .windowStyle(.hiddenTitleBar)
        .defaultSize(width: 1280, height: 720)
    }
}

private final class ShowAppDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        NSApp.setActivationPolicy(.regular)
        DispatchQueue.main.async {
            NSApp.activate(ignoringOtherApps: true)
            NSApp.windows.first?.makeKeyAndOrderFront(nil)
        }
    }

    func applicationShouldHandleReopen(_ sender: NSApplication, hasVisibleWindows flag: Bool) -> Bool {
        sender.windows.forEach { $0.makeKeyAndOrderFront(nil) }
        sender.activate(ignoringOtherApps: true)
        return true
    }
}
#endif
