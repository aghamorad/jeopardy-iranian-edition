import SwiftUI
import WebKit
#if os(iOS)
import UIKit
#endif

/// The show exists once, as the web build, and both apps are a window onto it.
/// Nothing below decides how anything looks or sounds — it finds the build in the
/// bundle, hands it to a webview, and gets out of the way.
enum ShowSource {
    static let directory = "Web"

    /// `Web/index.html` inside the app bundle.
    static var indexURL: URL? {
        if let url = Bundle.main.url(
            forResource: "index", withExtension: "html", subdirectory: directory
        ) {
            return url
        }
        // `swift run` during development: the executable lives inside the package,
        // so the build is a couple of levels up from this file.
        let besideSources = URL(fileURLWithPath: #filePath)
            .deletingLastPathComponent()   // App/
            .deletingLastPathComponent()   // package root
            .appendingPathComponent(directory)
            .appendingPathComponent("index.html")
        return FileManager.default.fileExists(atPath: besideSources.path) ? besideSources : nil
    }
}

/// The one sense the show cannot reach from inside a web page. No Safari on any
/// version of iOS has a Vibration API, so a buzz the page has already decided to
/// feel arrives here as a word instead, and this answers it with the platform's own
/// feedback generator.
///
/// Deliberately vocabulary-free: it knows which words exist but not what a buzz is.
/// The page still decides what a player should feel and when — the shell only knows
/// how to say it.
///
/// On a Mac there is nothing to say it with beyond a tick, and `NSHapticFeedbackManager`
/// silently does nothing on hardware without a Force Touch trackpad.
final class ShowHaptics: NSObject, WKScriptMessageHandler {
    static let name = "haptics"

    func userContentController(
        _ controller: WKUserContentController,
        didReceive message: WKScriptMessage
    ) {
        guard let word = message.body as? String else { return }

        #if os(iOS)
        switch word {
        case "take":
            // A thumb landing on the plate, and the heaviest thing the game says.
            UIImpactFeedbackGenerator(style: .heavy).impactOccurred()
        case "beat":
            // Somebody else got there first. Light, and gone.
            UIImpactFeedbackGenerator(style: .light).impactOccurred()
        case "foul":
            // Jumped the lamp. The notification generator's error is the only
            // pattern on the platform that reads as a refusal rather than a touch.
            UINotificationFeedbackGenerator().notificationOccurred(.error)
        default:
            UIImpactFeedbackGenerator(style: .light).impactOccurred(intensity: 0.6)
        }
        #else
        NSHapticFeedbackManager.defaultPerformer.perform(.generic, performanceTime: .now)
        #endif
    }
}

/// A game show is not a web page. The theme and the host's line start on their own,
/// so the webview must not sit on them waiting for a tap that a native app never
/// asks anybody for.
private func showConfiguration() -> WKWebViewConfiguration {
    let configuration = WKWebViewConfiguration()
    configuration.mediaTypesRequiringUserActionForPlayback = []
    configuration.userContentController.add(ShowHaptics(), name: ShowHaptics.name)
    #if os(iOS)
    configuration.allowsInlineMediaPlayback = true
    configuration.allowsPictureInPictureMediaPlayback = false
    #endif
    return configuration
}

/// A stage, not a document: no bouncing, no zooming, no back-swipe.
private func dressStage(_ view: WKWebView) {
    view.allowsBackForwardNavigationGestures = false
    view.allowsLinkPreview = false
    #if os(macOS)
    view.allowsMagnification = false
    view.underPageBackgroundColor = .black
    view.enclosingScrollView?.drawsBackground = false
    #else
    view.scrollView.isScrollEnabled = false
    view.scrollView.bounces = false
    view.isOpaque = false
    view.backgroundColor = .black
    #endif
}

private func loadShow(into view: WKWebView) {
    guard let index = ShowSource.indexURL else {
        view.loadHTMLString(
            """
            <body style="margin:0;background:#000;color:#f4f1ea;\
            font:16px -apple-system,system-ui;display:grid;place-items:center;height:100vh">
            The show is missing from this build.
            </body>
            """,
            baseURL: nil
        )
        return
    }
    view.loadFileURL(index, allowingReadAccessTo: index.deletingLastPathComponent())
}

#if os(macOS)
struct ShowWebView: NSViewRepresentable {
    func makeNSView(context: Context) -> WKWebView {
        let view = WKWebView(frame: .zero, configuration: showConfiguration())
        dressStage(view)
        loadShow(into: view)
        return view
    }

    func updateNSView(_ view: WKWebView, context: Context) {}
}
#else
struct ShowWebView: UIViewRepresentable {
    func makeUIView(context: Context) -> WKWebView {
        let view = WKWebView(frame: .zero, configuration: showConfiguration())
        dressStage(view)
        loadShow(into: view)
        return view
    }

    func updateUIView(_ view: WKWebView, context: Context) {}
}
#endif
