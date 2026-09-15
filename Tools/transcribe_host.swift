// Transcribe recorded host clips with Apple's on-device speech model.
//
//   swift Tools/transcribe_host.swift Web/assets/audio/host_*.m4a
//
// Prints one `name<TAB>transcript` row per clip, name being the basename. That
// is deliberate: a host clip is filed under the cue name the engine announces,
// `tannaz_correct` and `tannaz_right_08_tehran_survives_another_round` alike, so the
// output keys are already the keys of the `LINES` table in Web/host-layer.js.
//
// On-device and offline: no HuggingFace weights, no network beyond the one-time
// Apple asset install. Built because the whisper model this project expected to
// have was never actually downloaded.

import AVFoundation
import Foundation
import Speech

let args = Array(CommandLine.arguments.dropFirst())
guard !args.isEmpty else {
    FileHandle.standardError.write("usage: transcribe_host.swift <audio>...\n".data(using: .utf8)!)
    exit(2)
}

let locale = Locale(identifier: "en-US")

// Biasing vocabulary. Her lines are about a small, closed set of things, and
// the model without this hears `Tehran` as "Teh" and `Mashallah` as "Michelle".
// Every one of these is a word that actually occurs in the clips, so this
// sharpens the transcription rather than putting words in her mouth.
let BIAS = [
    "Tehran", "Mashallah", "Cyrus the Great", "WhatsApp",
    "dinner party", "taxi driver", "uncle", "civilization",
    "confidence", "opinions", "evidence", "Jeopardy"
]

func makeTranscriber() -> SpeechTranscriber {
    SpeechTranscriber(locale: locale,
                      transcriptionOptions: [],
                      reportingOptions: [],
                      attributeOptions: [])
}

func transcribe(_ path: String) async throws -> String {
    let url = URL(fileURLWithPath: path)
    let transcriber = makeTranscriber()
    let analyzer = SpeechAnalyzer(modules: [transcriber])

    let bias = AnalysisContext()
    bias.contextualStrings[.general] = BIAS
    try await analyzer.setContext(bias)

    let audio = try AVAudioFile(forReading: url)

    // Results arrive on their own sequence while the file is being analyzed, so
    // the collector runs alongside rather than after.
    async let collected: String = {
        var text: [String] = []
        for try await result in transcriber.results {
            text.append(String(result.text.characters))
        }
        return text.joined(separator: " ")
    }()

    if let last = try await analyzer.analyzeSequence(from: audio) {
        try await analyzer.finalizeAndFinish(through: last)
    } else {
        await analyzer.cancelAndFinishNow()
    }

    return try await collected
}

func run() async {
    // One asset install for the whole run, not one per clip.
    let probe = makeTranscriber()
    do {
        if let request = try await AssetInventory.assetInstallationRequest(supporting: [probe]) {
            FileHandle.standardError.write("installing speech asset...\n".data(using: .utf8)!)
            try await request.downloadAndInstall()
        }
    } catch {
        FileHandle.standardError.write("asset install failed: \(error)\n".data(using: .utf8)!)
        exit(1)
    }

    for path in args {
        let name = URL(fileURLWithPath: path).deletingPathExtension().lastPathComponent
        do {
            let text = try await transcribe(path)
            print("\(name)\t\(text)")
        } catch {
            print("\(name)\t<<FAILED: \(error)>>")
        }
        fflush(stdout)
    }
}

let done = DispatchSemaphore(value: 0)
Task {
    await run()
    done.signal()
}
done.wait()
