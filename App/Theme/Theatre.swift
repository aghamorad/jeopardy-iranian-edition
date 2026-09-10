import SwiftUI
import AVFoundation
import JeopardyGameEngine

public enum TheatreCue: String {
    case menu
    case join
    case select
    case armed
    case buzz
    case correct
    case incorrect
    case wager
    case round
    case round2
    case finalRound
    case finalThink
    case winner
}

@MainActor
public final class TheatreDirector: ObservableObject {
    public static let shared = TheatreDirector()

    private init() {
        NotificationCenter.default.addObserver(forName: .gameBuzzAccepted, object: nil, queue: .main) { [weak self] _ in
            Task { @MainActor in self?.play(.buzz) }
        }
    }

    @Published public private(set) var pulse: Int = 0

    private var sfxPlayer: AVAudioPlayer?
    private var hostPlayer: AVAudioPlayer?
    private var musicPlayer: AVAudioPlayer?
    private var currentMusicName: String?
    private var musicVolume: Float = 0.30

    public func playOpeningChallenge() {
        guard let url = resolveAudioURL(named: "host_challenge") else { return }
        hostPlayer?.stop()
        hostPlayer = try? AVAudioPlayer(contentsOf: url)
        hostPlayer?.volume = 0.95
        musicPlayer?.setVolume(0.10, fadeDuration: 0.25)
        hostPlayer?.prepareToPlay()
        hostPlayer?.play()
        let duration = hostPlayer?.duration ?? 15
        DispatchQueue.main.asyncAfter(deadline: .now() + duration) { [weak self] in
            guard let self else { return }
            self.musicPlayer?.setVolume(self.musicVolume, fadeDuration: 0.7)
        }
    }

    public func playHost(_ name: String) {
        guard let url = Bundle.main.url(forResource: "host_" + name, withExtension: "mp3") else { return }
        hostPlayer = try? AVAudioPlayer(contentsOf: url)
        hostPlayer?.volume = 0.9
        musicPlayer?.setVolume(0.10, fadeDuration: 0.25)
        hostPlayer?.play()
        let duration = hostPlayer?.duration ?? 12
        DispatchQueue.main.asyncAfter(deadline: .now() + duration) { [weak self] in
            guard let self else { return }
            self.musicPlayer?.setVolume(self.musicVolume, fadeDuration: 0.7)
        }
    }

    public func play(_ cue: TheatreCue) {
        pulse &+= 1
        let soundName = cue.resourceName
        if let url = resolveAudioURL(named: soundName) {
            do {
                sfxPlayer = try AVAudioPlayer(contentsOf: url)
                sfxPlayer?.volume = cue.volume
                sfxPlayer?.prepareToPlay()
                sfxPlayer?.play()
            } catch {
                print("Failed to play sound \(soundName): \(error)")
            }
        }
    }

    public func startMenuMusic() {
        startLoop(named: "menu_theme", volume: 0.35)
    }

    public func startGameplayMusic() {
        startLoop(named: "menu_theme", volume: 0.24)
    }

    public func startThinkingMusic() {
        startLoop(named: "thinking_loop", volume: 0.30)
    }

    public func playBumper(for round: GameRound) {
        startGameplayMusic()
        let trackName = round == .double ? "round2_bumper" : (round == .final ? "wager" : "round1_bumper")
        playResource(trackName, volume: 0.70)
    }

    public func startFinalThinkMusic() {
        startTrack(named: "final", volume: 0.50, loops: 0)
    }

    public func playVictoryCelebration() {
        startTrack(named: "winner", volume: 0.58, loops: 0)
        let duration = musicPlayer?.duration ?? 10
        DispatchQueue.main.asyncAfter(deadline: .now() + duration) { [weak self] in
            self?.startMenuMusic()
        }
    }

    public func stopMusic() {
        musicPlayer?.stop()
        hostPlayer?.stop()
        musicPlayer = nil
        currentMusicName = nil
    }

    private func startLoop(named name: String, volume: Float) {
        if currentMusicName == name, musicPlayer?.isPlaying == true {
            musicVolume = volume
            musicPlayer?.setVolume(volume, fadeDuration: 0.45)
            return
        }
        startTrack(named: name, volume: volume, loops: -1)
    }

    private func startTrack(named name: String, volume: Float, loops: Int) {
        guard let url = resolveAudioURL(named: name) else { return }
        do {
            musicPlayer?.setVolume(0, fadeDuration: 0.18)
            musicPlayer?.stop()
            let player = try AVAudioPlayer(contentsOf: url)
            player.numberOfLoops = loops
            player.volume = volume
            player.prepareToPlay()
            player.play()
            musicPlayer = player
            currentMusicName = name
            musicVolume = volume
        } catch {
            print("Failed to start music \(name): \(error)")
        }
    }

    private func playResource(_ name: String, volume: Float) {
        guard let url = resolveAudioURL(named: name) else { return }
        do {
            sfxPlayer = try AVAudioPlayer(contentsOf: url)
            sfxPlayer?.volume = volume
            sfxPlayer?.prepareToPlay()
            sfxPlayer?.play()
        } catch {
            print("Failed to play \(name): \(error)")
        }
    }

    private func resolveAudioURL(named name: String) -> URL? {
        for ext in ["wav", "mp3", "m4a"] {
            if let url = Bundle.main.url(forResource: name, withExtension: ext, subdirectory: "Sounds") {
                return url
            }
            if let url = Bundle.main.url(forResource: name, withExtension: ext) {
                return url
            }
        }
        // 1. Direct bundle resourceURL
        if let resURL = Bundle.main.resourceURL?.appendingPathComponent("Sounds/\(name).wav"),
           FileManager.default.fileExists(atPath: resURL.path) {
            return resURL
        }
        if let resURL = Bundle.main.resourceURL?.appendingPathComponent("\(name).wav"),
           FileManager.default.fileExists(atPath: resURL.path) {
            return resURL
        }
        // 2. Standard Bundle lookups
        
        // 3. Absolute and relative project paths
        let candidatePaths = [
            "/Users/Morad/Desktop/Jeopardy - Iranian Edition/App/Resources/Sounds/\(name).wav",
            "App/Resources/Sounds/\(name).wav",
            "../App/Resources/Sounds/\(name).wav"
        ]
        for path in candidatePaths {
            if FileManager.default.fileExists(atPath: path) {
                return URL(fileURLWithPath: path)
            }
        }
        return nil
    }
}

private extension TheatreCue {
    var resourceName: String {
        switch self {
        case .menu: return "join"
        case .join: return "join"
        case .select: return "select"
        case .armed: return "armed"
        case .buzz: return "buzz"
        case .correct: return "correct"
        case .incorrect: return "incorrect"
        case .wager: return "wager"
        case .round: return "round1_bumper"
        case .round2: return "round2_bumper"
        case .finalRound: return "wager"
        case .finalThink: return "final"
        case .winner: return "winner"
        }
    }

    var volume: Float {
        switch self {
        case .buzz: return 0.58
        case .correct: return 0.58
        case .incorrect: return 0.48
        case .wager: return 0.55
        case .winner: return 0.62
        case .armed: return 0.30
        case .select: return 0.28
        default: return 0.42
        }
    }
}

public struct ArchivalPulse: ViewModifier {
    @ObservedObject var theatre = TheatreDirector.shared
    public func body(content: Content) -> some View {
        content
            .scaleEffect(theatre.pulse % 2 == 0 ? 1.0 : 1.003)
            .animation(.easeOut(duration: 0.18), value: theatre.pulse)
    }
}

public extension View {
    func archivalPulse() -> some View {
        modifier(ArchivalPulse())
    }
}
