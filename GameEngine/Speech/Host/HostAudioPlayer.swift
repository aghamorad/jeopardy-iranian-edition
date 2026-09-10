import Foundation
import AVFoundation

public enum HostVoiceSelection: String, CaseIterable, Codable {
    case british = "Daniel (British)"
    case american = "Samantha (American)"
    case australian = "Karen (Australian)"
    case irish = "Moira (Irish)"

    public var languageCode: String {
        switch self {
        case .british: return "en-GB"
        case .american: return "en-US"
        case .australian: return "en-AU"
        case .irish: return "en-IE"
        }
    }
}

public final class HostAudioPlayer: NSObject, ObservableObject, AVSpeechSynthesizerDelegate {
    public static let shared = HostAudioPlayer()

    private let synthesizer = AVSpeechSynthesizer()
    @Published public private(set) var isSpeaking: Bool = false
    @Published public var selectedVoice: HostVoiceSelection = .american
    public var onFinishedSpeaking: (() -> Void)?

    private override init() {
        super.init()
        synthesizer.delegate = self
    }

    public func speak(text: String, language: GameLanguage = .english, completion: (() -> Void)? = nil) {
        self.onFinishedSpeaking = completion
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }

        let cleanText = naturalize(text)
        guard !cleanText.isEmpty else {
            completion?()
            return
        }

        let utterance = AVSpeechUtterance(string: cleanText)
        // Natural speech parameters matching broadcast standards
        let punctuationLift: Float = cleanText.contains("!") ? 1.12 : (cleanText.contains("?") ? 1.07 : 1.03)
        utterance.rate = cleanText.contains("!") ? 0.53 : 0.48
        utterance.pitchMultiplier = punctuationLift
        utterance.preUtteranceDelay = cleanText.count > 90 ? 0.10 : 0.05
        utterance.volume = 1.0
        utterance.preUtteranceDelay = 0.04
        utterance.postUtteranceDelay = cleanText.contains("!") ? 0.16 : 0.11
        utterance.voice = voice(for: language)

        isSpeaking = true
        synthesizer.speak(utterance)
    }

    private func voice(for language: GameLanguage) -> AVSpeechSynthesisVoice? {
        if language == .persian {
            let voices = AVSpeechSynthesisVoice.speechVoices()
            if let farsi = voices.first(where: { $0.language.lowercased().hasPrefix("fa") }) {
                return farsi
            }
        }
        // Use selected high-quality host voice
        let voices = AVSpeechSynthesisVoice.speechVoices()
        return voices.first(where: { $0.language.lowercased() == selectedVoice.languageCode.lowercased() })
            ?? AVSpeechSynthesisVoice(language: selectedVoice.languageCode)
            ?? AVSpeechSynthesisVoice(language: "en-US")
    }

    private func naturalize(_ text: String) -> String {
        var t = text
        // Clean markdown and quotes
        t = t.replacingOccurrences(of: "**", with: "")
        t = t.replacingOccurrences(of: "*", with: "")
        t = t.replacingOccurrences(of: "\"", with: "")
        t = t.replacingOccurrences(of: "“", with: "")
        t = t.replacingOccurrences(of: "”", with: "")
        t = t.replacingOccurrences(of: "—", with: ", ")
        t = t.replacingOccurrences(of: "–", with: " to ")
        t = t.replacingOccurrences(of: "c.", with: "around ")
        t = t.replacingOccurrences(of: "BC", with: "B C")
        t = t.replacingOccurrences(of: "AD", with: "A D")
        t = t.replacingOccurrences(of: "$", with: "")
        t = t.replacingOccurrences(of: "dollars", with: "toomans")
        t = t.replacingOccurrences(of: "dollar", with: "tooman")
        t = t.replacingOccurrences(of: "  ", with: " ")
        return t.trimmingCharacters(in: .whitespacesAndNewlines)
    }

    public func stop() {
        if synthesizer.isSpeaking {
            synthesizer.stopSpeaking(at: .immediate)
        }
        isSpeaking = false
    }

    public func speechSynthesizer(_ synthesizer: AVSpeechSynthesizer, didFinish utterance: AVSpeechUtterance) {
        DispatchQueue.main.async {
            self.isSpeaking = false
            self.onFinishedSpeaking?()
            self.onFinishedSpeaking = nil
        }
    }
}
