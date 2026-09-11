import SwiftUI
import WebKit

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

/// A game show is not a web page. The theme and the host's line start on their own,
/// so the webview must not sit on them waiting for a tap that a native app never
/// asks anybody for.
private func showConfiguration() -> WKWebViewConfiguration {
    let configuration = WKWebViewConfiguration()
    configuration.mediaTypesRequiringUserActionForPlayback = []
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
