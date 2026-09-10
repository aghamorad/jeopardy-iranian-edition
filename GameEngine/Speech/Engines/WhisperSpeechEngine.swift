import Foundation
import AVFoundation
import Speech

/// Native microphone recognizer. The compatibility name remains WhisperSpeechEngine,
/// but recognition is performed by Apple's native Speech framework with live audio.
public final class WhisperSpeechEngine: NSObject, SpeechRecognitionEngine {
    public let engineName = "Native Speech Recognition"
    public private(set) var isListening = false
    public var supportsPersian: Bool { SFSpeechRecognizer.supportedLocales().contains { $0.identifier.hasPrefix("fa") } }
    private var sessionID = UUID()
    public private(set) var lastError: String?

    private var recognizer: SFSpeechRecognizer?
    private var request: SFSpeechAudioBufferRecognitionRequest?
    private var recognitionTask: SFSpeechRecognitionTask?
    private let audioEngine = AVAudioEngine()
    private var inputTapInstalled = false
    private var partialHandler: ((ASRTranscription) -> Void)?
    private var finalHandler: ((ASRTranscription) -> Void)?
    private var startTimestamp: UInt64 = 0
    private var currentLanguage = "en"
    private var currentVocabulary: [String] = []

    public override init() { super.init() }

    public func startListening(
        language: String,
        contextVocabulary: [String],
        onPartial: @escaping (ASRTranscription) -> Void,
        onFinal: @escaping (ASRTranscription) -> Void
    ) throws {
        stopListening()
        let session = sessionID
        lastError = nil
        currentLanguage = language.lowercased()
        currentVocabulary = contextVocabulary
        partialHandler = onPartial
        finalHandler = onFinal
        startTimestamp = mach_absolute_time()

        let locale = currentLanguage.hasPrefix("fa") ? Locale(identifier: "fa-IR") : Locale(identifier: "en-US")
        guard let speechRecognizer = SFSpeechRecognizer(locale: locale), speechRecognizer.isAvailable else {
            fail("Speech recognition is unavailable. Type your answer below.")
            return
        }
        recognizer = speechRecognizer

        switch SFSpeechRecognizer.authorizationStatus() {
        case .denied, .restricted:
            fail("Speech recognition permission is off. Type your answer below.")
        case .notDetermined:
            SFSpeechRecognizer.requestAuthorization { [weak self] status in
                DispatchQueue.main.async {
                    guard let self, self.sessionID == session else { return }
                    guard status == .authorized else {
                        self.fail("Speech recognition permission is off. Type your answer below.")
                        return
                    }
                    self.beginAudioCapture()
                }
            }
        case .authorized:
            beginAudioCapture()
        @unknown default:
            fail("Speech recognition is unavailable. Type your answer below.")
        }
    }

    private func beginAudioCapture() {
        guard let recognizer, recognizer.isAvailable else {
            fail("Speech recognition is unavailable. Type your answer below.")
            return
        }
        let session = sessionID
        AVCaptureDevice.requestAccess(for: .audio) { [weak self] granted in
            DispatchQueue.main.async {
                guard let self, self.sessionID == session else { return }
                guard granted else {
                    self.fail("Microphone permission is off. Type your answer below.")
                    return
                }
                self.configureAudioCapture(recognizer: recognizer)
            }
        }
    }

    private func configureAudioCapture(recognizer: SFSpeechRecognizer) {
        stopAudioOnly()
        let recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        recognitionRequest.shouldReportPartialResults = true
        recognitionRequest.taskHint = .dictation
        if #available(macOS 10.15, *) { recognitionRequest.requiresOnDeviceRecognition = false }
        if !currentVocabulary.isEmpty { recognitionRequest.contextualStrings = currentVocabulary }
        request = recognitionRequest

        let inputNode = audioEngine.inputNode
        let format = inputNode.outputFormat(forBus: 0)
        guard format.sampleRate > 0, format.channelCount > 0 else { fail("No microphone input. Type your answer below."); return }
        inputNode.removeTap(onBus: 0)
        inputNode.installTap(onBus: 0, bufferSize: 1024, format: format) { [weak self] buffer, _ in
            self?.request?.append(buffer)
        }
        inputTapInstalled = true

        recognitionTask = recognizer.recognitionTask(with: recognitionRequest) { [weak self] result, error in
            guard let self else { return }
            if let result {
                let best = result.bestTranscription
                let confidence = best.segments.last?.confidence ?? 0.0
                let transcript = ASRTranscription(
                    text: best.formattedString,
                    isFinal: result.isFinal,
                    confidence: Double(confidence),
                    latencyMs: self.elapsedMs
                )
                if result.isFinal { self.finish(transcript) }
                else { self.partialHandler?(transcript) }
            }
            if error != nil, self.isListening {
                DispatchQueue.main.async { self.fail("Speech recognition stopped. Type your answer below.") }
            }
        }

        do {
            try audioEngine.start()
            isListening = true
        } catch {
            fail("Microphone could not start. Type your answer below.")
        }
    }

    public func stopListening() {
        sessionID = UUID()
        stopAudioOnly()
        isListening = false
    }

    private func stopAudioOnly() {
        audioEngine.stop()
        if inputTapInstalled {
            audioEngine.inputNode.removeTap(onBus: 0)
            inputTapInstalled = false
        }
        request?.endAudio()
        recognitionTask?.cancel()
        recognitionTask = nil
        request = nil
    }

    private func finish(_ transcript: ASRTranscription) {
        guard isListening else { return }
        stopAudioOnly()
        isListening = false
        finalHandler?(transcript)
    }

    private func fail(_ message: String) {
        lastError = message
        stopAudioOnly()
        isListening = false
        partialHandler?(ASRTranscription(text: "", isFinal: false, confidence: 0, latencyMs: elapsedMs))
    }

    private var elapsedMs: Double {
        guard startTimestamp != 0 else { return 0 }
        var info = mach_timebase_info()
        mach_timebase_info(&info)
        let nanos = (mach_absolute_time() - startTimestamp) * UInt64(info.numer) / UInt64(info.denom)
        return Double(nanos) / 1_000_000.0
    }

    /// Deterministic injection seam for balancing and QA.
    public func feedAudioSample(transcribedText: String, isFinal: Bool) {
        guard isListening else { return }
        let transcript = ASRTranscription(text: transcribedText, isFinal: isFinal, confidence: 0.95, latencyMs: elapsedMs)
        if isFinal { finish(transcript) } else { partialHandler?(transcript) }
    }
}
