import SwiftUI
import AppKit
import JeopardyGameEngine

// MARK: - Game Stage Themes
public enum GameStageTheme: String, CaseIterable, Codable, Identifiable {
    case royalIsfahan = "Royal Isfahan (Lapis & Gold)"
    case tehranStudio = "Tehran 1975 (Retro Studio)"
    case caspianVelvet = "Caspian Velvet (Emerald & Walnut)"
    case persepolisStone = "Persepolis (Stone & Bronze)"

    public var id: String { rawValue }

    public var persianName: String {
        switch self {
        case .royalIsfahan: return "اصفهان فیروزه‌ای • کاخ چهلستون"
        case .tehranStudio: return "استودیو جام‌جم • دهه پنجاه"
        case .caspianVelvet: return "عمارت کاسپین • مخمل و گردو"
        case .persepolisStone: return "تخت جمشید • تالار آپادانا"
        }
    }

    public var primaryBackgrounds: [Color] {
        switch self {
        case .royalIsfahan:
            return [
                Color(red: 0.05, green: 0.08, blue: 0.16), // Deep Lapis
                Color(red: 0.08, green: 0.12, blue: 0.22),
                Color(red: 0.03, green: 0.05, blue: 0.10)
            ]
        case .tehranStudio:
            return [
                Color(red: 0.08, green: 0.07, blue: 0.06), // Warm Mahogany
                Color(red: 0.14, green: 0.11, blue: 0.09),
                Color(red: 0.05, green: 0.04, blue: 0.04)
            ]
        case .caspianVelvet:
            return [
                Color(red: 0.04, green: 0.10, blue: 0.07), // Emerald Forest
                Color(red: 0.07, green: 0.15, blue: 0.11),
                Color(red: 0.02, green: 0.06, blue: 0.04)
            ]
        case .persepolisStone:
            return [
                Color(red: 0.09, green: 0.09, blue: 0.11), // Basalt & Charcoal
                Color(red: 0.14, green: 0.14, blue: 0.16),
                Color(red: 0.05, green: 0.05, blue: 0.07)
            ]
        }
    }

    public var goldAccent: Color {
        switch self {
        case .royalIsfahan: return Color(red: 0.98, green: 0.82, blue: 0.35)
        case .tehranStudio: return Color(red: 1.0, green: 0.74, blue: 0.28)
        case .caspianVelvet: return Color(red: 0.92, green: 0.78, blue: 0.40)
        case .persepolisStone: return Color(red: 0.88, green: 0.65, blue: 0.32) // Burnished bronze
        }
    }

    public var secondaryAccent: Color {
        switch self {
        case .royalIsfahan: return Color(red: 0.22, green: 0.76, blue: 0.80) // Turquoise
        case .tehranStudio: return Color(red: 0.95, green: 0.38, blue: 0.24) // Studio red
        case .caspianVelvet: return Color(red: 0.30, green: 0.85, blue: 0.60) // Malachite
        case .persepolisStone: return Color(red: 0.85, green: 0.45, blue: 0.28) // Terracotta
        }
    }

    public var cardSurface: Color {
        switch self {
        case .royalIsfahan: return Color(red: 0.09, green: 0.12, blue: 0.20)
        case .tehranStudio: return Color(red: 0.15, green: 0.13, blue: 0.12)
        case .caspianVelvet: return Color(red: 0.08, green: 0.14, blue: 0.11)
        case .persepolisStone: return Color(red: 0.13, green: 0.13, blue: 0.16)
        }
    }

    public var cardBorder: Color {
        switch self {
        case .royalIsfahan: return Color(red: 0.28, green: 0.38, blue: 0.55)
        case .tehranStudio: return Color(red: 0.42, green: 0.32, blue: 0.24)
        case .caspianVelvet: return Color(red: 0.22, green: 0.40, blue: 0.30)
        case .persepolisStone: return Color(red: 0.36, green: 0.36, blue: 0.42)
        }
    }
}

// MARK: - Bibi Zangzadeh (The Host with Attitude)
public enum HostEmotion: String {
    case neutral = "🧐"
    case smug = "😏"
    case delighted = "👏"
    case disappointed = "🤦‍♂️"
    case shocked = "😱"
    case dramatic = "🏛️"
}

public struct HostQuote {
    public let text: String
    public let persian: String
    public let emotion: HostEmotion
}

public final class OstadFaniEngine: ObservableObject {
    public static let shared = OstadFaniEngine()

    @Published public var currentEmotion: HostEmotion = .neutral
    @Published public var currentDialogue: String = "Welcome to Jeopardy: Iranian Edition. I brought questions; you brought confidence. Adorable."
    @Published public var currentPersianQuote: String = "به مسابقه بزرگ تاریخ ایران خوش آمدید."
    @Published public var isTalking: Bool = false

    private init() {}

    public func sayWelcome() {
        let quotes = [
            HostQuote(
                text: "Welcome, scholars and gamblers of history! 500 years of blood, poetry, and petroleum await you. Let us see who honors their ancestors!",
                persian: "به استودیوی تاریخ خوش آمدید! بیایید ببینیم چه کسی آبروی نیاکان را حفظ می‌کند.",
                emotion: .dramatic
            ),
            HostQuote(
                text: "The board is set, the studio lights are burning. Hands on your buzzers, and remember: the archives forgive nothing.",
                persian: "صحنه آماده است. دست‌ها روی زنگ‌ها؛ تاریخ هیچ اشتباهی را نمی‌بخشد!",
                emotion: .smug
            )
        ]
        deliver(quotes.randomElement()!)
    }

    public func sayCorrect(player: String, value: Int) {
        let quotes = [
            HostQuote(
                text: "Barakallah, \(player)! Spot on. Sa'di himself would nod in approval. That adds \(value) to your ledger!",
                persian: "بارک‌الله! کاملاً دقیق. خود سعدی هم به نشانه تأیید سر تکان می‌دهد!",
                emotion: .delighted
            ),
            HostQuote(
                text: "Afarin! Right on the money and not a second to spare. A scholar of the realm indeed!",
                persian: "آفرین! کاملاً درست و در اوج مهارت. معلوم است تاریخ را خوب خوانده‌اید.",
                emotion: .delighted
            ),
            HostQuote(
                text: "Precisely so. The royal court was never so generous, but I am forced to award you \(value) toomans!",
                persian: "دقیقاً همینطور است. درباریان هم اینقدر دست‌ودلباز نبودند، ولی این امتیاز مال شماست!",
                emotion: .smug
            ),
            HostQuote(
                text: "Accurate down to the year! You clearly did not waste your years in the tea houses.",
                persian: "دقیق تا سال واقعه! مشخص است وقتتان را در قهوه‌خانه‌ها تلف نکرده‌اید.",
                emotion: .smug
            )
        ]
        deliver(quotes.randomElement()!)
    }

    public func sayWrong(player: String, value: Int) {
        let quotes = [
            HostQuote(
                text: "Afsoos, \(player)! A catastrophic reading of the archives! A stinging deduction of \(value) toomans.",
                persian: "افسوس! یک فاجعه کامل در خواندن تاریخ! کسر امتیاز به حساب شما ثبت شد.",
                emotion: .disappointed
            ),
            HostQuote(
                text: "Good heavens, no! The court chroniclers are weeping in their graves. Deduct the stake!",
                persian: "پناه بر خدا، خیر! وقایع‌نگاران دربار در گور لرزیدند. امتیاز کسر می‌شود!",
                emotion: .shocked
            ),
            HostQuote(
                text: "Completely erroneous. Did you study Iranian history from the back of a matchbox?",
                persian: "کاملاً غلط! تاریخ ایران را از روی قوطی کبریت خوانده‌اید؟",
                emotion: .smug
            ),
            HostQuote(
                text: "Alas! An expensive hallucination. Into the red you go, my dear contestant.",
                persian: "افسوس! توهمی بسیار گران‌قیمت. رفتید توی ارقام منفی!",
                emotion: .disappointed
            )
        ]
        deliver(quotes.randomElement()!)
    }

    public func sayDailyDouble(player: String) {
        let quotes = [
            HostQuote(
                text: "A Sealed Imperial Wager! The music halts, the stage dims. \(player), the eyes of the court are upon you. Name your stakes!",
                persian: "حکم مهروموم سلطنتی! صحنه تاریک می‌شود. همه نگاه‌ها به شماست؛ شرط خود را اعلام کنید!",
                emotion: .dramatic
            ),
            HostQuote(
                text: "The Daily Double! A true test of nerve. Will you wager like a cautious bureaucrat, or risk it all like a desert khan?",
                persian: "خان بزرگ تاریخ! مثل یک دیوان‌سالار محتاط شرط می‌بندید یا مثل یک سردار شجاع همه را قمار می‌کنید؟",
                emotion: .smug
            )
        ]
        deliver(quotes.randomElement()!)
    }

    public func sayFinalJeopardy() {
        let quote = HostQuote(
            text: "This is the final reckoning. Write your wagers in secret. When the music ceases, the champion of Iranian history will be crowned.",
            persian: "لحظه سرنوشت‌ساز نهایی. شرط‌هایتان را در خفا بنویسید. تاریخ بی‌رحم و جاودانه است.",
            emotion: .dramatic
        )
        deliver(quote)
    }

    public func sayVictory(champion: String) {
        let quote = HostQuote(
            text: "All hail \(champion)! A magnificent demonstration of historical erudition. The Persepolis Winged Lion trophy is yours!",
            persian: "درود بر قهرمان ما! تندیس شیر بالدار پرسپولیس با افتخار به شما تقدیم می‌شود!",
            emotion: .delighted
        )
        deliver(quote)
    }

    public func reactToAnswer(player: String, correct: Bool, value: Int) {
        if correct {
            sayCorrect(player: player, value: value)
        } else {
            sayWrong(player: player, value: value)
        }
    }

    private func deliver(_ quote: HostQuote) {
        currentEmotion = quote.emotion
        currentDialogue = quote.text
        currentPersianQuote = quote.persian
        isTalking = true

        DispatchQueue.main.asyncAfter(deadline: .now() + 4.5) { [weak self] in
            self?.isTalking = false
        }
    }
}

// MARK: - Core Theme & Design Tokens
public struct ArchivalTheme {
    // Current Active Global Theme
    public static var currentTheme: GameStageTheme = .tehranStudio

    // Palette Getters
    public static var studioDark: Color { currentTheme.primaryBackgrounds[0] }
    public static var backgroundDark: Color { currentTheme.primaryBackgrounds[1] }
    public static var cardSurface: Color { currentTheme.cardSurface }
    public static var cardBorder: Color { currentTheme.cardBorder }
    public static var gold24k: Color { currentTheme.goldAccent }
    public static var bronzeAccent: Color { currentTheme.goldAccent.opacity(0.85) }
    public static var bronzeMuted: Color { currentTheme.cardBorder }
    public static var textParchment: Color { Color(red: 0.96, green: 0.94, blue: 0.90) }
    public static var textMuted: Color { Color(red: 0.68, green: 0.70, blue: 0.76) }

    public static let buzzerArmedGlow = Color(red: 1.0, green: 0.80, blue: 0.20)
    public static let correctGreen = Color(red: 0.18, green: 0.82, blue: 0.45)
    public static let wrongRed = Color(red: 0.90, green: 0.22, blue: 0.22)
    public static let redSeal = Color(red: 0.72, green: 0.14, blue: 0.14)
    public static let lapisBlue = Color(red: 0.12, green: 0.28, blue: 0.58)
    public static let turquoise = Color(red: 0.18, green: 0.74, blue: 0.78)
    public static let ink = Color(red: 0.03, green: 0.035, blue: 0.045)
    public static let paper = Color(red: 0.14, green: 0.13, blue: 0.11)

    // Player Color Presets
    public static let playerColors: [Color] = [
        Color(red: 0.95, green: 0.75, blue: 0.25), // Imperial Gold
        Color(red: 0.25, green: 0.60, blue: 0.90), // Lapis Lazuli
        Color(red: 0.90, green: 0.35, blue: 0.25), // Terracotta
        Color(red: 0.20, green: 0.78, blue: 0.55), // Caspian Emerald
        Color(red: 0.75, green: 0.42, blue: 0.85), // Amethyst Royal
        Color(red: 0.95, green: 0.55, blue: 0.20)  // Persian Saffron
    ]

    public static func serifFont(size: CGFloat, weight: Font.Weight = .regular) -> Font {
        Font.system(size: size, weight: weight, design: .serif)
    }

    public static func sansFont(size: CGFloat, weight: Font.Weight = .regular) -> Font {
        Font.system(size: size, weight: weight, design: .default)
    }

    public static func monoFont(size: CGFloat, weight: Font.Weight = .bold) -> Font {
        Font.system(size: size, weight: weight, design: .monospaced)
    }

    public static func roundValueFormat(for value: Int) -> String {
        toman(value)
    }

    public static func toman(_ value: Int) -> String {
        let sign = value < 0 ? "−" : ""
        let absolute = abs(value)
        if absolute >= 1_000_000 && absolute % 1_000_000 == 0 {
            let digits = String(absolute / 1_000_000).map { ["۰","۱","۲","۳","۴","۵","۶","۷","۸","۹"][Int(String($0))!] }.joined()
            return "\(sign)\(digits) میلیون تومان"
        }
        return "\(sign)\(absolute.formatted()) تومان"
    }
}

// MARK: - Animated Host Avatar & Dialogue Card
public struct HostBroadcastHUD: View {
    @ObservedObject var host = OstadFaniEngine.shared
    @ObservedObject var speech = HostAudioPlayer.shared
    public init() {}
    public var body: some View {
        HStack(spacing: 12) {
            Image(systemName: "mic.fill").font(.system(size: 22)).foregroundColor(ArchivalTheme.gold24k)
            Text("BIBI ZANGZADEH").font(.system(size: 10, weight: .bold)).tracking(2).foregroundColor(ArchivalTheme.gold24k)
            Rectangle().fill(ArchivalTheme.gold24k.opacity(0.4)).frame(width: 1, height: 24)
        Text(host.currentDialogue).font(.system(size: 13, design: .serif)).foregroundColor(ArchivalTheme.textParchment).lineLimit(2).transition(.opacity)
            Spacer()
            if speech.isSpeaking { Image(systemName: "waveform").symbolEffect(.variableColor.iterative).foregroundColor(ArchivalTheme.gold24k) }
        }.padding(14).background(ArchivalTheme.ink.opacity(0.90)).clipShape(RoundedRectangle(cornerRadius: 8))
    }
}

// MARK: - Confetti Particles Fountain (Pure Canvas, No @State)
public struct ConfettiFountainView: View {
    public init() {}
    public var body: some View {
        TimelineView(.animation) { timeline in
            Canvas { context, size in
                let time = timeline.date.timeIntervalSinceReferenceDate
                let count = 38
                let colors: [Color] = [
                    ArchivalTheme.gold24k,
                    Color(red: 0.22, green: 0.76, blue: 0.80),
                    Color(red: 0.90, green: 0.22, blue: 0.22),
                    Color.white,
                    Color(red: 0.95, green: 0.65, blue: 0.25)
                ]
                for i in 0..<count {
                    let seed = Double(i) * 73.0
                    let speed = 140.0 + Double(i % 6) * 30.0
                    let y = (time * speed + seed).truncatingRemainder(dividingBy: Double(size.height + 40)) - 20
                    let x = (Double(size.width) * (0.05 + 0.9 * sin(Double(i) * 0.45 + time * 0.7))).truncatingRemainder(dividingBy: Double(size.width))
                    let rot = Angle(degrees: (time * 240 + seed).truncatingRemainder(dividingBy: 360))
                    let w = 8.0 + Double(i % 4) * 2.0
                    let h = 12.0 + Double(i % 3) * 3.0

                    var piece = Path()
                    piece.addRect(CGRect(x: -w/2, y: -h/2, width: w, height: h))
                    let transform = CGAffineTransform(translationX: CGFloat(x), y: CGFloat(y)).rotated(by: CGFloat(rot.radians))
                    context.fill(piece.applying(transform), with: .color(colors[i % colors.count].opacity(0.9)))
                }
            }
        }
        .ignoresSafeArea()
        .allowsHitTesting(false)
    }
}

// MARK: - Digital LED Scoreboard Meter
public struct DigitalLEDScoreMeter: View {
    public let score: Int
    public let previousScore: Int?
    public let color: Color

    public init(score: Int, previousScore: Int? = nil, color: Color = ArchivalTheme.gold24k) {
        self.score = score
        self.previousScore = previousScore
        self.color = color
    }

    public var body: some View {
        HStack(spacing: 3) {
            Text(score < 0 ? "-" : "")
                .font(ArchivalTheme.monoFont(size: 20, weight: .black))
                .foregroundColor(ArchivalTheme.wrongRed)

            Text(ArchivalTheme.toman(score))
                .font(ArchivalTheme.monoFont(size: 20, weight: .black))
                .foregroundColor(score >= 0 ? color : ArchivalTheme.wrongRed)
                .shadow(color: (score >= 0 ? color : ArchivalTheme.wrongRed).opacity(0.6), radius: 6)
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 4)
        .background(Color.black.opacity(0.85))
        .cornerRadius(6)
        .overlay(RoundedRectangle(cornerRadius: 6).stroke(color.opacity(0.3), lineWidth: 1))
    }
}

// MARK: - Button Styles
public struct PrimaryShowButtonStyle: ButtonStyle {
    public init() {}
    public func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(ArchivalTheme.sansFont(size: 13, weight: .black))
            .tracking(2)
            .foregroundColor(ArchivalTheme.ink)
            .padding(.horizontal, 24)
            .padding(.vertical, 14)
            .background(ArchivalTheme.gold24k)
            .cornerRadius(8)
            .scaleEffect(configuration.isPressed ? 0.97 : 1)
            .shadow(color: ArchivalTheme.gold24k.opacity(0.35), radius: 12, y: 5)
    }
}

public struct QuietButtonStyle: ButtonStyle {
    public init() {}
    public func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
            .tracking(1.4)
            .foregroundColor(ArchivalTheme.textParchment)
            .padding(.horizontal, 17)
            .padding(.vertical, 11)
            .background(ArchivalTheme.cardSurface)
            .cornerRadius(6)
            .overlay(RoundedRectangle(cornerRadius: 6).stroke(ArchivalTheme.cardBorder, lineWidth: 1))
            .opacity(configuration.isPressed ? 0.7 : 1)
    }
}

public struct ClueTileButtonStyle: ButtonStyle {
    public init() {}
    public func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.95 : 1.0)
            .brightness(configuration.isPressed ? 0.15 : 0.0)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }
}

// MARK: - Dynamic Archival Backdrop (No @State)
public enum StageAssets {
    private static var images: [String: NSImage] = [:]
    public static func image(_ name: String) -> NSImage? {
        if let cached = images[name] { return cached }
        for ext in ["png", "jpg"] {
            if let url = Bundle.main.url(forResource: name, withExtension: ext), let image = NSImage(contentsOf: url) { images[name] = image; return image }
        }
        return nil
    }
}

public struct ArchivalBackdrop: View {
    @ObservedObject private var theatre = TheatreDirector.shared
    public init() {}
    public var body: some View {
        GeometryReader { geo in
            ZStack {
                Color(red: 0.025, green: 0.045, blue: 0.08)
                let artName: String = {
                    switch ArchivalTheme.currentTheme {
                    case .royalIsfahan: return "stage_isfahan"
                    case .tehranStudio: return "studio_stage_bg"
                    case .caspianVelvet: return "persian_shamseh"
                    case .persepolisStone: return "sealed_wager_card"
                    }
                }()
                if let art = StageAssets.image(artName) {
                    Image(nsImage: art).resizable().scaledToFill()
                        .frame(width: geo.size.width, height: geo.size.height).clipped()
                        .opacity(ArchivalTheme.currentTheme == .tehranStudio ? 0.86 : 0.64)
                }
                themeMotif
                HStack(spacing: 0) {
                    LinearGradient(colors: [.clear, Color(red: 0.0, green: 0.78, blue: 0.38).opacity(0.52), .black.opacity(0.24)], startPoint: .leading, endPoint: .trailing)
                        .frame(width: geo.size.width * 0.16)
                    Spacer()
                    LinearGradient(colors: [.black.opacity(0.24), Color.white.opacity(0.18), Color(red: 0.95, green: 0.10, blue: 0.14).opacity(0.58)], startPoint: .leading, endPoint: .trailing)
                        .frame(width: geo.size.width * 0.16)
                }
                LinearGradient(colors: [ArchivalTheme.currentTheme.primaryBackgrounds[0].opacity(0.34), .black.opacity(0.18), .black.opacity(0.78)], startPoint: .top, endPoint: .bottom)
                    .blendMode(.multiply)
                LinearGradient(colors: [.black.opacity(0.20), .clear, .black.opacity(0.58)], startPoint: .top, endPoint: .bottom)
                VStack(spacing: 0) {
                    Rectangle().fill(Color(red: 0.0, green: 0.78, blue: 0.38).opacity(0.78)).frame(height: 2)
                    Rectangle().fill(Color.white.opacity(0.78)).frame(height: 2)
                    Rectangle().fill(Color(red: 0.95, green: 0.10, blue: 0.14).opacity(0.78)).frame(height: 2)
                    Spacer()
                }
            }
        }.ignoresSafeArea().allowsHitTesting(false)
    }

    @ViewBuilder private var themeMotif: some View {
        switch ArchivalTheme.currentTheme {
        case .royalIsfahan:
            Image(systemName: "building.columns.fill").font(.system(size: 420)).foregroundColor(.cyan.opacity(0.06)).rotationEffect(.degrees(-8)).offset(x: 360, y: 120)
        case .tehranStudio:
            VStack(spacing: 0) { ForEach(0..<18, id: \.self) { _ in Rectangle().fill(Color.orange.opacity(0.08)).frame(height: 2).padding(.vertical, 10) } }.rotationEffect(.degrees(-12)).offset(x: 80, y: 80)
        case .caspianVelvet:
            Image(systemName: "leaf.fill").font(.system(size: 520)).foregroundColor(.green.opacity(0.10)).rotationEffect(.degrees(-25)).offset(x: 360, y: 80)
        case .persepolisStone:
            Image(systemName: "arrow.up.right.square.fill").font(.system(size: 460)).foregroundColor(.orange.opacity(0.08)).rotationEffect(.degrees(-12)).offset(x: 350, y: 80)
        }
    }
}

// MARK: - Broadcast Header
public struct BroadcastTitle: View {
    public let compact: Bool
    public init(compact: Bool = false) { self.compact = compact }

    public var body: some View {
        VStack(spacing: compact ? 2 : 6) {
            HStack(spacing: 8) {
                Rectangle().fill(ArchivalTheme.gold24k).frame(width: compact ? 16 : 30, height: 2)
                Text("مسابقه بزرگ تاریخ ایران")
                    .font(ArchivalTheme.serifFont(size: compact ? 11 : 16, weight: .semibold))
                    .foregroundColor(ArchivalTheme.gold24k)
                Rectangle().fill(ArchivalTheme.gold24k).frame(width: compact ? 16 : 30, height: 2)
            }

            HStack(spacing: compact ? 5 : 6) {
                Text("JE")
                    .font(ArchivalTheme.sansFont(size: compact ? 21 : 36, weight: .black))
                    .tracking(compact ? -0.5 : 1)
                    .foregroundColor(ArchivalTheme.textParchment)
                if let emblem = StageAssets.image("iranian_emblem") {
                    LinearGradient(colors: [Color(red: 0.18, green: 0.65, blue: 0.30), .white, Color(red: 0.85, green: 0.18, blue: 0.18)], startPoint: .top, endPoint: .bottom)
                        .frame(width: compact ? 27 : 42, height: compact ? 30 : 48)
                        .mask(Image(nsImage: emblem).resizable().scaledToFit())
                } else {
                    Text("O").font(ArchivalTheme.serifFont(size: compact ? 16 : 32, weight: .black)).foregroundColor(ArchivalTheme.textParchment)
                }
                Text("PARDY!")
                    .font(ArchivalTheme.sansFont(size: compact ? 21 : 36, weight: .black))
                    .tracking(compact ? -0.5 : 1)
                    .foregroundColor(ArchivalTheme.textParchment)

                Text("IRANIAN EDITION")
                    .font(ArchivalTheme.serifFont(size: compact ? 16 : 32, weight: .bold))
                    .tracking(compact ? 2 : 4)
                    .foregroundColor(ArchivalTheme.gold24k)
            }
            .shadow(color: ArchivalTheme.gold24k.opacity(0.3), radius: 8, x: 0, y: 2)

            if !compact {
                Text("HISTORY • MEMORY • SOVEREIGNTY")
                    .font(ArchivalTheme.sansFont(size: 10, weight: .bold))
                    .tracking(4)
                    .foregroundColor(ArchivalTheme.textMuted)
            }
        }
    }
}

public struct ArchivalPanel: ViewModifier {
    public var stroke: Color = ArchivalTheme.cardBorder
    public func body(content: Content) -> some View {
        content
            .background(ArchivalTheme.cardSurface.opacity(0.92))
            .overlay(
                RoundedRectangle(cornerRadius: 10)
                    .stroke(
                        LinearGradient(
                            colors: [stroke.opacity(0.9), stroke.opacity(0.4)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 1.5
                    )
            )
            .shadow(color: .black.opacity(0.4), radius: 18, y: 8)
    }
}

public extension View {
    func archivalPanel(stroke: Color = ArchivalTheme.cardBorder) -> some View {
        modifier(ArchivalPanel(stroke: stroke))
    }
}

public struct CategoryBadgeView: View {
    public let category: String
    public init(category: String) { self.category = category }

    public var body: some View {
        let badgeName = category.uppercased().contains("QAJAR") || category.uppercased().contains("CONCESSIONS") ? "archive_qajar" : badgeFilename(for: category)
        if let img = StageAssets.image(badgeName) {
            Image(nsImage: img)
                .resizable()
                .frame(width: 24, height: 24)
                .clipShape(Circle())
                .overlay(Circle().stroke(ArchivalTheme.gold24k.opacity(0.75), lineWidth: 1.2))
        } else {
            Circle()
                .fill(ArchivalTheme.gold24k.opacity(0.25))
                .frame(width: 24, height: 24)
                .overlay(
                    Image(systemName: "crown.fill")
                        .font(.system(size: 11))
                        .foregroundColor(ArchivalTheme.gold24k)
                )
        }
    }

    private func badgeFilename(for cat: String) -> String {
        let c = cat.uppercased()
        if c.contains("SAFAVID") || c.contains("ISFAHAN") { return "badge_safavid" }
        if c.contains("QAJAR") || c.contains("CONCESSIONS") { return "badge_qajar" }
        if c.contains("CONSTITUTION") || c.contains("MASHRUTEH") { return "badge_mashruteh" }
        if c.contains("PAHLAVI") || c.contains("COSSACK") || c.contains("SHAH") { return "badge_pahlavi" }
        if c.contains("OIL") { return "badge_oil" }
        if c.contains("CINEMA") || c.contains("LALEZAR") { return "badge_cinema" }
        if c.contains("WAR") || c.contains("DEFENSE") { return "badge_war" }
        return "badge_culture"
    }

    private func resolveBadgeURL(named: String) -> URL? {
        if let resURL = Bundle.main.resourceURL?.appendingPathComponent("\(named).png"),
           FileManager.default.fileExists(atPath: resURL.path) {
            return resURL
        }
        if let url = Bundle.main.url(forResource: named, withExtension: "png") {
            return url
        }
        let candidatePaths = [
            "/Users/Morad/Desktop/Jeopardy - Iranian Edition/App/Resources/\(named).png",
            "App/Resources/\(named).png",
            "../App/Resources/\(named).png"
        ]
        for path in candidatePaths {
            if FileManager.default.fileExists(atPath: path) {
                return URL(fileURLWithPath: path)
            }
        }
        return nil
    }
}
