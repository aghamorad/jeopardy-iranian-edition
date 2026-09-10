import SwiftUI
import AVFoundation

#if os(macOS)
import AppKit
public typealias PlatformImage = NSImage
#else
import UIKit
public typealias PlatformImage = UIImage
#endif

public extension Image {
    /// `Image(nsImage:)` on macOS, `Image(uiImage:)` on iOS.
    init(platformImage: PlatformImage) {
        #if os(macOS)
        self.init(nsImage: platformImage)
        #else
        self.init(uiImage: platformImage)
        #endif
    }
}

public enum PlatformImageLoader {
    public static func load(contentsOf url: URL) -> PlatformImage? {
        #if os(macOS)
        return NSImage(contentsOf: url)
        #else
        return UIImage(contentsOfFile: url.path)
        #endif
    }

    public static func load(name: String, extensions: [String] = ["png", "jpg"]) -> PlatformImage? {
        for ext in extensions {
            if let url = Bundle.main.url(forResource: name, withExtension: ext),
               let image = load(contentsOf: url) {
                return image
            }
        }
        return nil
    }
}

/// Quit on macOS. iOS deliberately has no programmatic exit — quitting an app
/// there is a crash by convention — so this is a no-op that callers can ignore.
public enum PlatformApp {
    public static func quit() {
        #if os(macOS)
        NSApplication.shared.terminate(nil)
        #endif
    }

    /// iOS suspends and silences an app's audio unless the shared session is
    /// configured as playback. Without this the show runs silent with the
    /// ringer switch off — the single biggest audio difference from macOS.
    public static func configureAudioSession() {
        #if os(iOS)
        let session = AVAudioSession.sharedInstance()
        try? session.setCategory(.playback, mode: .default)
        try? session.setActive(true)
        #endif
    }

    public static func activateAudioSession() {
        #if os(iOS)
        try? AVAudioSession.sharedInstance().setActive(true)
        #endif
    }
}
