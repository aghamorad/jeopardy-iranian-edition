import Foundation

public final class MockSpeechEngine: SpeechRecognitionEngine {
    public let engineName = "Mock Test Speech Engine"
    public private(set) var isListening: Bool = false
    public let supportsPersian: Bool = true
    public private(set) var lastError: String?

    private var onFinalCallback: ((ASRTranscription) -> Void)?

    public init() {}

    public func startListening(
        language: String,
        contextVocabulary: [String],
        onPartial: @escaping (ASRTranscription) -> Void,
        onFinal: @escaping (ASRTranscription) -> Void
    ) throws {
        lastError = nil
        isListening = true
        onFinalCallback = onFinal
    }

    public func simulateTranscription(_ text: String) {
        guard isListening else { return }
        isListening = false
        onFinalCallback?(ASRTranscription(text: text, isFinal: true, confidence: 1.0, latencyMs: 42.0))
    }

    public func stopListening() {
        isListening = false
    }
}
