import Foundation

public struct ASRTranscription: Equatable {
    public let text: String
    public let isFinal: Bool
    public let confidence: Double
    public let latencyMs: Double

    public init(text: String, isFinal: Bool, confidence: Double = 1.0, latencyMs: Double = 0.0) {
        self.text = text
        self.isFinal = isFinal
        self.confidence = confidence
        self.latencyMs = latencyMs
    }
}

public protocol SpeechRecognitionEngine: AnyObject {
    var engineName: String { get }
    var isListening: Bool { get }
    var supportsPersian: Bool { get }
    var lastError: String? { get }

    func startListening(
        language: String,
        contextVocabulary: [String],
        onPartial: @escaping (ASRTranscription) -> Void,
        onFinal: @escaping (ASRTranscription) -> Void
    ) throws

    func stopListening()
}
