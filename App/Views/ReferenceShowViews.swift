import SwiftUI
import AppKit
import JeopardyGameEngine

private let referenceSize = CGSize(width: 1672, height: 941)

private struct ReferencePlate: View {
    let asset: String

    var body: some View {
        GeometryReader { proxy in
            ZStack {
                Color.black
                if let image = StageAssets.image(asset) {
                    Image(nsImage: image)
                        .resizable()
                        .scaledToFit()
                        .frame(width: proxy.size.width, height: proxy.size.height)
                }
            }
        }
        .ignoresSafeArea()
    }
}

struct ReferenceOutlineButtonStyle: ButtonStyle {
    var prominent = false

    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(.system(size: 13, weight: .semibold))
            .tracking(3)
            .foregroundColor(.white)
            .frame(maxWidth: .infinity)
            .frame(height: 52)
            .background(Color.black.opacity(configuration.isPressed ? 0.92 : 0.72))
            .overlay(
                RoundedRectangle(cornerRadius: 6)
                    .stroke(
                        prominent
                            ? LinearGradient(colors: [.green, .white.opacity(0.75), .red], startPoint: .leading, endPoint: .trailing)
                            : LinearGradient(colors: [.white.opacity(0.6), .white.opacity(0.22)], startPoint: .top, endPoint: .bottom),
                        lineWidth: prominent ? 1.7 : 1
                    )
            )
            .shadow(color: prominent ? .red.opacity(0.18) : .clear, radius: 12)
            .scaleEffect(configuration.isPressed ? 0.985 : 1)
    }
}

public struct ReferenceLobbyView: View {
    @ObservedObject var gameState: GameState
    @ObservedObject private var theatre = TheatreDirector.shared
    @ObservedObject private var controllers = ControllerManager.shared
    @StateObject private var ui = ReferenceLobbyState()

    public init(gameState: GameState) { self.gameState = gameState }

    public var body: some View {
        ZStack {
            ReferencePlate(asset: "lobby_reference")

            GeometryReader { proxy in
                let scale = min(proxy.size.width / referenceSize.width, proxy.size.height / referenceSize.height)
                let originX = (proxy.size.width - referenceSize.width * scale) / 2
                let originY = (proxy.size.height - referenceSize.height * scale) / 2

                invisibleMenuButton("Start Game", x: 626, y: 494, width: 420, height: 70, scale: scale, originX: originX, originY: originY) {
                    ui.showSetup = true
                }
                .keyboardShortcut(.defaultAction)

                invisibleMenuButton("Settings", x: 626, y: 580, width: 420, height: 56, scale: scale, originX: originX, originY: originY) {
                    ui.showSettings = true
                }

                invisibleMenuButton("How to Play", x: 626, y: 644, width: 420, height: 56, scale: scale, originX: originX, originY: originY) {
                    ui.showHowTo = true
                }

                invisibleMenuButton("Quit", x: 626, y: 708, width: 420, height: 56, scale: scale, originX: originX, originY: originY) {
                    NSApplication.shared.terminate(nil)
                }
            }

            if ui.showSettings { settingsOverlay }
            if ui.showHowTo { howToOverlay }
            if ui.showSetup { setupOverlay }
        }
        .frame(minWidth: 1100, minHeight: 620)
        .onAppear {
            theatre.startMenuMusic()
        }
    }

    private var setupOverlay: some View {
        ZStack {
            Color.black.opacity(0.82).ignoresSafeArea()
            VStack(alignment: .leading, spacing: 18) {
                HStack {
                    VStack(alignment: .leading, spacing: 5) {
                        Text("THE GREEN ROOM").font(.system(size: 13, weight: .bold)).tracking(4)
                        Text("Hosted by Bibi Zangzadeh").font(.system(size: 18, weight: .semibold, design: .serif))
                        Text("Born of the buzzer. Raised without mercy.").font(.system(size: 12)).foregroundColor(.white.opacity(0.58))
                    }
                    Spacer()
                    Button("CLOSE") { ui.showSetup = false }.buttonStyle(.plain).foregroundColor(.white.opacity(0.72))
                }

                Rectangle().fill(LinearGradient(colors: [.green, .white, .red], startPoint: .leading, endPoint: .trailing)).frame(height: 2)

                Text("HOW SHOULD ANSWERS WORK?").font(.system(size: 11, weight: .bold)).tracking(3).foregroundColor(.white.opacity(0.65))
                HStack(spacing: 10) {
                    modeButton("TYPE / SPEAK RESPONSE", mode: .classic)
                    modeButton("MULTIPLE CHOICE", mode: .multipleChoice)
                }

                Text("CONTESTANTS").font(.system(size: 11, weight: .bold)).tracking(3).foregroundColor(.white.opacity(0.65))
                ForEach(Array(gameState.players.enumerated()), id: \.element.id) { index, player in
                    HStack(spacing: 10) {
                        Text("\(index + 1)").font(.system(size: 12, weight: .bold)).foregroundColor(index == 0 ? .green : .red).frame(width: 18)
                        TextField("Contestant name", text: $gameState.players[index].name)
                            .textFieldStyle(.plain).padding(11).background(.white.opacity(0.08))
                        Button(player.isBot ? "BOT" : "HUMAN") { gameState.setBot(player.id, enabled: !player.isBot) }
                            .buttonStyle(.bordered)
                        if gameState.players.count > 1 {
                            Button("REMOVE") { gameState.players.remove(at: index) }.buttonStyle(.plain).foregroundColor(.red)
                        }
                    }
                }

                if gameState.players.count < 6 {
                    Button("+ ADD CONTESTANT") {
                        gameState.players.append(Player(name: "Player \(gameState.players.count + 1)"))
                    }
                    .buttonStyle(.plain).foregroundColor(.white.opacity(0.72))
                }

                if !controllers.assignedPlayers.isEmpty {
                    VStack(alignment: .leading, spacing: 5) {
                        Text("CONNECTED CONTROLLERS").font(.system(size: 10, weight: .bold)).tracking(2.5).foregroundColor(.white.opacity(0.55))
                        ForEach(controllers.assignedPlayers.keys.sorted(), id: \.self) { index in
                            if let glyphs = controllers.glyphs(forPlayerIndex: index) {
                                Text("PLAYER \(index + 1)  ·  \(controllers.deviceName(forPlayerIndex: index) ?? "GAMEPAD")  ·  \(glyphs.buzz) BUZZ")
                                    .font(.system(size: 11, weight: .medium)).foregroundColor(.white.opacity(0.72))
                            }
                        }
                    }
                }

                HStack(spacing: 12) {
                    if gameState.hasSavedGame {
                        Button("CONTINUE SAVED GAME") {
                            ui.showSetup = false
                            theatre.playOpeningChallenge()
                            gameState.restoreSavedGame()
                        }
                        .buttonStyle(ReferenceOutlineButtonStyle())
                    }
                    Button("START NEW GAME") {
                        ui.showSetup = false
                        theatre.playOpeningChallenge()
                        gameState.startNewGame()
                    }
                    .buttonStyle(ReferenceOutlineButtonStyle(prominent: true))
                    .keyboardShortcut(.defaultAction)
                }
            }
            .padding(30)
            .frame(width: 720)
            .background(Color(red: 0.025, green: 0.03, blue: 0.034).opacity(0.985))
            .overlay(RoundedRectangle(cornerRadius: 8).stroke(.white.opacity(0.38), lineWidth: 1))
            .foregroundColor(.white)
        }
    }

    private func modeButton(_ label: String, mode: GameMode) -> some View {
        let selected = gameState.configuration.mode == mode
        return Button(label) { gameState.configuration.mode = mode }
            .font(.system(size: 11, weight: .bold)).tracking(1.6)
            .foregroundColor(.white)
            .frame(maxWidth: .infinity).frame(height: 44)
            .background(selected ? Color.white.opacity(0.14) : Color.black.opacity(0.72))
            .overlay(
                RoundedRectangle(cornerRadius: 5)
                    .stroke(selected ? LinearGradient(colors: [.green, .white, .red], startPoint: .leading, endPoint: .trailing) : LinearGradient(colors: [.white.opacity(0.28)], startPoint: .leading, endPoint: .trailing), lineWidth: selected ? 1.7 : 1)
            )
            .buttonStyle(.plain)
    }

    private func invisibleMenuButton(
        _ label: String,
        x: CGFloat,
        y: CGFloat,
        width: CGFloat,
        height: CGFloat,
        scale: CGFloat,
        originX: CGFloat,
        originY: CGFloat,
        action: @escaping () -> Void
    ) -> some View {
        Button(action: action) { Color.white.opacity(0.001) }
            .buttonStyle(.plain)
            .frame(width: width * scale, height: height * scale)
            .position(
                x: originX + (x + width / 2) * scale,
                y: originY + (y + height / 2) * scale
            )
            .accessibilityLabel(label)
    }

    private var settingsOverlay: some View {
        ZStack {
            Color.black.opacity(0.78).ignoresSafeArea()
            VStack(alignment: .leading, spacing: 22) {
                HStack {
                    Text("MATCH SETTINGS")
                        .font(.system(size: 13, weight: .bold))
                        .tracking(4)
                    Spacer()
                    Button("CLOSE") { ui.showSettings = false }
                        .buttonStyle(.plain)
                        .foregroundColor(.white.opacity(0.75))
                }

                Rectangle()
                    .fill(LinearGradient(colors: [.green, .white, .red], startPoint: .leading, endPoint: .trailing))
                    .frame(height: 2)

                Picker("Response mode", selection: $gameState.configuration.mode) {
                    ForEach(GameMode.allCases, id: \.self) { Text($0.rawValue.uppercased()).tag($0) }
                }
                .pickerStyle(.segmented)

                Picker("Language", selection: $gameState.configuration.language) {
                    Text("English").tag(GameLanguage.english)
                    Text("فارسی — UNDER CONSTRUCTION").tag(GameLanguage.persian)
                }
                .pickerStyle(.segmented)

                if gameState.configuration.language == .persian {
                    Text("نسخهٔ فارسی در دست ساخت است · PERSIAN EDITION UNDER CONSTRUCTION")
                        .font(.system(size: 11, weight: .bold))
                        .foregroundColor(.yellow.opacity(0.88))
                }

                Text("CONTESTANTS")
                    .font(.system(size: 11, weight: .bold))
                    .tracking(3)
                    .foregroundColor(.white.opacity(0.65))

                ForEach(Array(gameState.players.enumerated()), id: \.element.id) { index, player in
                    HStack {
                        Text(String(format: "%02d", index + 1)).foregroundColor(index == 0 ? .green : .red)
                        Text(player.name).font(.system(size: 17, weight: .semibold))
                        Spacer()
                        Button(player.isBot ? "BOT" : "HUMAN") {
                            gameState.setBot(player.id, enabled: !player.isBot)
                        }
                        .buttonStyle(.bordered)
                        if gameState.players.count > 1 {
                            Button("REMOVE") { gameState.players.remove(at: index) }
                                .buttonStyle(.plain)
                                .foregroundColor(.red)
                        }
                    }
                    .padding(.vertical, 6)
                }

                if gameState.players.count < 6 {
                    HStack {
                        TextField("Contestant name", text: $gameState.newPlayerNameInput)
                            .textFieldStyle(.plain)
                            .padding(10)
                            .background(.white.opacity(0.08))
                        Button("ADD") {
                            let name = gameState.newPlayerNameInput.trimmingCharacters(in: .whitespacesAndNewlines)
                            gameState.players.append(Player(name: name.isEmpty ? "Player \(gameState.players.count + 1)" : name))
                            gameState.newPlayerNameInput = ""
                        }
                        .buttonStyle(.borderedProminent)
                    }
                }

                Button("DONE") { ui.showSettings = false }
                    .buttonStyle(ReferenceOutlineButtonStyle(prominent: true))
            }
            .padding(32)
            .frame(width: 650)
            .background(Color(red: 0.035, green: 0.04, blue: 0.045).opacity(0.98))
            .overlay(RoundedRectangle(cornerRadius: 8).stroke(.white.opacity(0.35), lineWidth: 1))
            .foregroundColor(.white)
        }
    }

    private var howToOverlay: some View {
        ZStack {
            Color.black.opacity(0.78).ignoresSafeArea()
            VStack(alignment: .leading, spacing: 22) {
                Text("HOW TO PLAY").font(.system(size: 13, weight: .bold)).tracking(4)
                Rectangle().fill(LinearGradient(colors: [.green, .white, .red], startPoint: .leading, endPoint: .trailing)).frame(height: 2)
                Text("Choose a category and value. Read the clue, wait for the stage light, then buzz. A correct response wins the value; a wrong response loses it and opens the floor to rivals.")
                    .font(.system(size: 22, weight: .regular))
                    .lineSpacing(7)
                Text("KEYBOARD  ·  Arrows move  ·  Return opens  ·  Space buzzes for Player 1  ·  Return buzzes for Player 2\nCONTROLLER  ·  D-pad moves  ·  A selects  ·  Right trigger buzzes")
                    .font(.system(size: 12, weight: .medium))
                    .tracking(1.2)
                    .foregroundColor(.white.opacity(0.7))
                    .lineSpacing(6)
                Button("BACK") { ui.showHowTo = false }
                    .buttonStyle(ReferenceOutlineButtonStyle(prominent: true))
            }
            .padding(36)
            .frame(width: 720)
            .background(Color(red: 0.035, green: 0.04, blue: 0.045).opacity(0.98))
            .overlay(RoundedRectangle(cornerRadius: 8).stroke(.white.opacity(0.35), lineWidth: 1))
            .foregroundColor(.white)
        }
    }
}

private final class ReferenceLobbyState: ObservableObject {
    @Published var showSettings = false
    @Published var showHowTo = false
    @Published var showSetup = false
}

public struct ReferenceBoardView: View {
    @ObservedObject var gameState: GameState

    public init(gameState: GameState) { self.gameState = gameState }

    public var body: some View {
        ZStack {
            ReferencePlate(asset: "board_reference")
            GeometryReader { proxy in
                let scale = min(proxy.size.width / referenceSize.width, proxy.size.height / referenceSize.height)
                let originX = (proxy.size.width - referenceSize.width * scale) / 2
                let originY = (proxy.size.height - referenceSize.height * scale) / 2

                roundTabs(scale: scale)
                    .frame(width: 820 * scale, height: 46 * scale)
                    .position(x: originX + 836 * scale, y: originY + 124 * scale)

                liveBoard(scale: scale)
                    .frame(width: 1200 * scale, height: 510 * scale)
                    .position(x: originX + 836 * scale, y: originY + 428 * scale)

                podiums(scale: scale)
                    .frame(width: 1050 * scale, height: 112 * scale)
                    .position(x: originX + 836 * scale, y: originY + 797 * scale)
            }
        }
        .frame(minWidth: 1100, minHeight: 620)
    }

    private func roundTabs(scale: CGFloat) -> some View {
        HStack(spacing: 0) {
            tab("ROUND ONE", number: "01", active: gameState.round == .single)
            separator
            tab("DOUBLE", number: "02", active: gameState.round == .double)
            separator
            tab("FINAL", number: "03", active: gameState.round == .final)
        }
        .padding(.horizontal, 8 * scale)
        .background(Color(red: 0.035, green: 0.035, blue: 0.038).opacity(0.98))
        .clipShape(RoundedRectangle(cornerRadius: 23 * scale, style: .continuous))
        .overlay(
            RoundedRectangle(cornerRadius: 23 * scale, style: .continuous)
                .stroke(.white.opacity(0.16), lineWidth: 0.8)
        )
        .shadow(color: .black.opacity(0.32), radius: 12 * scale, y: 5 * scale)
    }

    private var separator: some View {
        Rectangle()
            .fill(Color.white.opacity(0.12))
            .frame(width: 1, height: 18)
    }

    private func tab(_ label: String, number: String, active: Bool) -> some View {
        HStack(spacing: 9) {
            ZStack {
                Circle()
                    .fill(active ? Color.white.opacity(0.14) : Color.clear)
                    .frame(width: 25, height: 25)
                Text(number)
                    .font(.system(size: 9, weight: .bold, design: .monospaced))
                    .foregroundColor(active ? .white : .white.opacity(0.32))
            }
            Text(label)
                .font(.system(size: 11, weight: active ? .bold : .medium))
                .tracking(1.8)
                .foregroundColor(active ? .white : .white.opacity(0.38))
            if active {
                Capsule()
                    .fill(LinearGradient(colors: [.green, .white, .red], startPoint: .top, endPoint: .bottom))
                    .frame(width: 3, height: 18)
                    .shadow(color: .white.opacity(0.24), radius: 4)
            }
        }
        .frame(maxWidth: .infinity, maxHeight: .infinity)
        .contentShape(Rectangle())
    }

    private func liveBoard(scale: CGFloat) -> some View {
        HStack(spacing: 10 * scale) {
            ForEach(0..<6, id: \.self) { col in
                VStack(spacing: 5 * scale) {
                    categoryHeader(col: col, scale: scale)
                    ForEach(0..<5, id: \.self) { row in
                        tile(col: col, row: row, scale: scale)
                    }
                }
            }
        }
        .padding(2 * scale)
        .background(Color.black.opacity(0.88))
    }

    private func categoryHeader(col: Int, scale: CGFloat) -> some View {
        let raw = col < gameState.board.categories.count ? gameState.board.categories[col] : "CATEGORY"
        let english = PlayerCopy.category(raw, language: .english)
        let localized = PlayerCopy.category(raw, language: .persian)
        let persian = localized.contains("موضوع:") || localized.caseInsensitiveCompare(english) == .orderedSame ? "تاریخ و فرهنگ ایران" : localized
        return VStack(spacing: 8 * scale) {
            Text(english.uppercased())
                .font(.system(size: 13 * scale, weight: .semibold))
                .multilineTextAlignment(.center)
                .lineLimit(2)
                .minimumScaleFactor(0.7)
            Text(persian)
                .font(.system(size: 12 * scale, weight: .regular))
                .foregroundColor(.white.opacity(0.72))
                .lineLimit(1)
                .minimumScaleFactor(0.65)
        }
        .foregroundColor(.white)
        .frame(maxWidth: .infinity)
        .frame(height: 118 * scale)
        .background(Color(red: 0.025, green: 0.03, blue: 0.032).opacity(0.98))
        .overlay(RoundedRectangle(cornerRadius: 5 * scale).stroke(.white.opacity(0.24), lineWidth: 1))
        .clipShape(RoundedRectangle(cornerRadius: 5 * scale))
    }

    private func tile(col: Int, row: Int, scale: CGFloat) -> some View {
        let slot = gameState.board.slot(at: col, valueIndex: row)
        let selected = gameState.selectedBoardColumn == col && gameState.selectedBoardRow == row
        return Button {
            guard let slot, !slot.isSolved else { return }
            TheatreDirector.shared.play(.select)
            gameState.selectSlot(categoryIndex: col, valueIndex: row)
        } label: {
            ZStack {
                Color(red: 0.018, green: 0.021, blue: 0.024)
                if let slot, !slot.isSolved {
                    VStack(spacing: 2) {
                        Text(compactValue(slot.value))
                            .font(.system(size: 25 * scale, weight: .semibold, design: .rounded))
                        Text("تومان")
                            .font(.system(size: 8 * scale, weight: .medium))
                            .tracking(1)
                            .foregroundColor(.white.opacity(0.5))
                    }
                }
            }
            .foregroundColor(.white.opacity(0.76))
            .frame(maxWidth: .infinity)
            .frame(height: 72 * scale)
            .overlay(
                RoundedRectangle(cornerRadius: 5 * scale)
                    .stroke(selected ? Color.red : .white.opacity(0.22), lineWidth: selected ? 2 : 1)
                    .shadow(color: selected ? .red : .clear, radius: 10)
            )
            .clipShape(RoundedRectangle(cornerRadius: 5 * scale))
        }
        .buttonStyle(.plain)
        .disabled(slot?.isSolved ?? true)
    }

    private func podiums(scale: CGFloat) -> some View {
        HStack(spacing: 92 * scale) {
            ForEach(Array(gameState.players.prefix(3).enumerated()), id: \.element.id) { index, player in
                VStack(spacing: 8 * scale) {
                    Rectangle()
                        .fill(index == 0 ? Color.green : (index == 1 ? Color.red : Color.white))
                        .frame(height: 3 * scale)
                    Text(player.name.uppercased())
                        .font(.system(size: 12 * scale, weight: .medium))
                        .tracking(1.4)
                    Text(compactScore(player.score))
                        .font(.system(size: 28 * scale, weight: .semibold, design: .rounded))
                        .foregroundColor(index == 0 ? .green : (index == 1 ? .red : .white.opacity(0.8)))
                }
                .frame(maxWidth: .infinity)
                .frame(height: 105 * scale)
                .background(Color.black.opacity(0.96))
                .overlay(RoundedRectangle(cornerRadius: 5 * scale).stroke(.white.opacity(0.30), lineWidth: 1))
                .clipShape(RoundedRectangle(cornerRadius: 5 * scale))
            }
        }
        .padding(.horizontal, 2)
        .background(Color.black)
        .foregroundColor(.white)
    }

    private func compactValue(_ value: Int) -> String { "\(value / 1_000_000)M" }
    private func compactScore(_ score: Int) -> String {
        let sign = score < 0 ? "−" : ""
        return "\(sign)\(abs(score) / 1_000_000)M"
    }
}

public struct ReferenceClueView: View {
    @ObservedObject var gameState: GameState
    @ObservedObject private var controllers = ControllerManager.shared

    public init(gameState: GameState) { self.gameState = gameState }

    public var body: some View {
        ZStack {
            ReferencePlate(asset: "lobby_reference")
            Color.black.opacity(0.38).ignoresSafeArea()

            if let slot = gameState.activeSlot {
                VStack(spacing: 18) {
                    HStack {
                        Text(PlayerCopy.category(slot.clue.category, language: gameState.configuration.language).uppercased())
                            .font(.system(size: 12, weight: .bold)).tracking(3)
                        Spacer()
                        Text(slot.value > 0 ? "\(slot.value / 1_000_000)M تومان" : "FINAL JEOPARDY")
                            .font(.system(size: 14, weight: .semibold)).tracking(2)
                        Button("EXIT") { gameState.leaveMatch() }.buttonStyle(.plain).foregroundColor(.white.opacity(0.55))
                    }

                    Rectangle().fill(LinearGradient(colors: [.green, .white, .red], startPoint: .leading, endPoint: .trailing)).frame(height: 2)

                    phaseContent(clue: slot.clue)

                    if !gameState.hostRulingMessage.isEmpty {
                        hostRulingCard
                    }

                    interaction(clue: slot.clue)
                }
                .padding(34)
                .frame(maxWidth: 980, maxHeight: 690)
                .background(Color(red: 0.025, green: 0.028, blue: 0.03).opacity(0.96))
                .overlay(RoundedRectangle(cornerRadius: 8).stroke(.white.opacity(0.35), lineWidth: 1))
                .foregroundColor(.white)
            }

            if case .finalReveal = gameState.phase { ConfettiFountainView() }
        }
        .frame(minWidth: 1100, minHeight: 620)
    }

    private var hostRulingCard: some View {
        HStack(spacing: 13) {
            Text("BZ")
                .font(.system(size: 11, weight: .black))
                .foregroundColor(.black)
                .frame(width: 34, height: 34)
                .background(gameState.hostRulingIsCorrect == true ? Color.green : Color.red)
                .clipShape(Circle())
            VStack(alignment: .leading, spacing: 3) {
                Text("BIBI ZANGZADEH")
                    .font(.system(size: 10, weight: .bold)).tracking(2.2)
                    .foregroundColor(gameState.hostRulingIsCorrect == true ? .green : .red)
                Text(gameState.hostRulingMessage)
                    .font(.system(size: 15, weight: .medium, design: .serif))
                    .lineLimit(2)
            }
            Spacer()
        }
        .padding(13)
        .background(Color.white.opacity(0.055))
        .overlay(RoundedRectangle(cornerRadius: 6).stroke((gameState.hostRulingIsCorrect == true ? Color.green : Color.red).opacity(0.55), lineWidth: 1))
    }

    @ViewBuilder
    private func phaseContent(clue: Clue) -> some View {
        switch gameState.phase {
        case .specialWager(let player, _):
            VStack(spacing: 18) {
                Text("DAILY DOUBLE").font(.system(size: 42, weight: .black)).tracking(5).foregroundColor(.red)
                Text("\(player.name), name your wager.").font(.system(size: 22))
                TextField("Wager", value: $gameState.activeSpecialWager, format: .number)
                    .textFieldStyle(.plain).font(.system(size: 32, weight: .semibold)).multilineTextAlignment(.center)
                    .padding().background(.white.opacity(0.08))
            }

        case .finalWager:
            finalWagers

        case .finalReveal(_, let winner):
            VStack(spacing: 18) {
                Text("CHAMPION").font(.system(size: 13, weight: .bold)).tracking(5).foregroundColor(.white.opacity(0.65))
                Text(winner?.name.uppercased() ?? "TIE GAME").font(.system(size: 54, weight: .black)).tracking(3)
                ForEach(gameState.players) { player in
                    Text("\(player.name)  ·  \(player.score / 1_000_000)M تومان").font(.system(size: 18, weight: .medium))
                }
            }

        default:
            VStack(spacing: 20) {
                if case .finalClue(let category, _) = gameState.phase {
                    Text(category.uppercased()).font(.system(size: 13, weight: .bold)).tracking(4).foregroundColor(.red)
                    Text("\(gameState.finalRemaining)").font(.system(size: 20, weight: .bold, design: .monospaced))
                }
                Text(clue.clueText)
                    .font(.system(size: 34, weight: .regular, design: .serif))
                    .multilineTextAlignment(.center)
                    .lineSpacing(8)
                    .minimumScaleFactor(0.68)
                if case .clueResolved = gameState.phase {
                    Text(clue.canonicalAnswer)
                        .font(.system(size: 26, weight: .semibold))
                        .foregroundColor(.green)
                    Text(clue.explanation)
                        .font(.system(size: 15))
                        .foregroundColor(.white.opacity(0.68))
                        .multilineTextAlignment(.center)
                        .lineLimit(4)
                }
            }
        }
    }

    @ViewBuilder
    private func interaction(clue: Clue) -> some View {
        switch gameState.phase {
        case .specialWager:
            Button("LOCK WAGER & REVEAL") { gameState.revealSpecialWager(amount: gameState.activeSpecialWager) }
                .buttonStyle(ReferenceOutlineButtonStyle(prominent: true))

        case .clueReading, .buzzerArmed:
            HStack(spacing: 12) {
                ForEach(Array(gameState.players.enumerated()), id: \.element.id) { index, player in
                    Button {
                        gameState.handleBuzz(playerIndex: index)
                    } label: {
                        HStack(spacing: 9) {
                            if let glyphs = controllers.glyphs(forPlayerIndex: index) {
                                Text(glyphs.buzz).font(.system(size: 20, weight: .bold)).frame(width: 28, height: 28)
                                    .overlay(Circle().stroke(.white.opacity(0.65), lineWidth: 1))
                            }
                            Text("BUZZ  ·  \(player.name.uppercased())")
                        }
                    }
                    .buttonStyle(ReferenceOutlineButtonStyle(prominent: index == 0))
                }
                Button("PASS") { gameState.passClue() }.buttonStyle(ReferenceOutlineButtonStyle())
            }

        case .answering(let player, _, _):
            if gameState.configuration.mode == .multipleChoice {
                controllerChoiceDiamond(clue: clue, player: player)
            } else {
                VStack(alignment: .leading, spacing: 9) {
                    HStack(spacing: 10) {
                        Text(player.name.uppercased()).font(.system(size: 12, weight: .bold)).tracking(2)
                        TextField("Type your response…", text: $gameState.manualAnswerInput)
                            .textFieldStyle(.plain).padding(14).background(.white.opacity(0.08))
                            .onSubmit { gameState.submitManualOrSimulatedAnswer(gameState.manualAnswerInput) }
                        Button {
                            gameState.toggleVoiceAnswer()
                        } label: {
                            Label(gameState.speechListening ? "STOP" : "SPEAK", systemImage: gameState.speechListening ? "stop.fill" : "mic.fill")
                        }
                        .buttonStyle(ReferenceOutlineButtonStyle())
                        .frame(width: 145)
                        Button("LOCK RESPONSE") { gameState.submitManualOrSimulatedAnswer(gameState.manualAnswerInput) }
                            .buttonStyle(ReferenceOutlineButtonStyle(prominent: true)).frame(width: 220)
                    }
                    if gameState.speechListening {
                        Text(gameState.liveTranscript.isEmpty ? "LISTENING…" : "LISTENING  ·  \(gameState.liveTranscript)")
                            .font(.system(size: 10, weight: .bold)).tracking(1.7).foregroundColor(.green)
                    } else if !gameState.speechErrorMessage.isEmpty {
                        Text(gameState.speechErrorMessage)
                            .font(.system(size: 10, weight: .medium)).foregroundColor(.red)
                    }
                }
            }

        case .clueResolved:
            Button("NEXT CLUE") { gameState.returnToBoard() }
                .buttonStyle(ReferenceOutlineButtonStyle(prominent: true))
                .keyboardShortcut(.defaultAction)

        case .finalWager:
            Button("REVEAL FINAL CLUE") { gameState.revealFinalClue() }
                .buttonStyle(ReferenceOutlineButtonStyle(prominent: true))

        case .finalClue:
            VStack(spacing: 10) {
                ForEach(gameState.players.filter { !$0.isBot }) { player in
                    HStack {
                        Text(player.name.uppercased()).frame(width: 140, alignment: .leading)
                        SecureField("Final response", text: finalDraft(player.id))
                            .textFieldStyle(.plain).padding(12).background(.white.opacity(0.08))
                        Button(gameState.finalResponses.contains(player.id) ? "LOCKED" : "SUBMIT") {
                            gameState.submitFinalAnswer(playerID: player.id, text: gameState.finalDrafts[player.id] ?? "")
                        }
                        .disabled(gameState.finalResponses.contains(player.id))
                        .buttonStyle(.bordered)
                    }
                }
            }

        case .finalReveal:
            HStack {
                Button("PLAY AGAIN") { gameState.startNewGame() }.buttonStyle(ReferenceOutlineButtonStyle(prominent: true))
                Button("MAIN MENU") { gameState.leaveMatch() }.buttonStyle(ReferenceOutlineButtonStyle())
            }

        default:
            EmptyView()
        }
    }

    private func controllerChoiceDiamond(clue: Clue, player: Player) -> some View {
        let playerIndex = gameState.players.firstIndex(where: { $0.id == player.id }) ?? gameState.currentTurnPlayerIndex
        let glyphs = controllers.glyphs(forPlayerIndex: playerIndex)
        return VStack(spacing: 9) {
            choiceButton(clue: clue, option: 3, glyph: glyphs?.top, playerIndex: playerIndex)
                .frame(maxWidth: 560)
            HStack(spacing: 12) {
                choiceButton(clue: clue, option: 2, glyph: glyphs?.left, playerIndex: playerIndex)
                choiceButton(clue: clue, option: 1, glyph: glyphs?.right, playerIndex: playerIndex)
            }
            choiceButton(clue: clue, option: 0, glyph: glyphs?.bottom, playerIndex: playerIndex)
                .frame(maxWidth: 560)
            if let device = controllers.deviceName(forPlayerIndex: playerIndex) {
                Text("\(device.uppercased())  ·  HOLD THE SHOWN BUTTON TO LOCK IN")
                    .font(.system(size: 9, weight: .bold)).tracking(1.5).foregroundColor(.white.opacity(0.5))
            }
        }
    }

    private func choiceButton(clue: Clue, option: Int, glyph: String?, playerIndex: Int) -> some View {
        let available = clue.options.indices.contains(option)
        return Button {
            guard available else { return }
            gameState.handleMultipleChoice(playerIndex: playerIndex, optionIndex: option)
        } label: {
            HStack(spacing: 12) {
                Text(glyph ?? "\(option + 1)")
                    .font(.system(size: glyph == nil ? 12 : 20, weight: .bold))
                    .frame(width: 30, height: 30)
                    .overlay(Circle().stroke(.white.opacity(0.55), lineWidth: 1))
                Text(available ? clue.options[option] : "")
                    .font(.system(size: 13, weight: .semibold))
                    .lineLimit(2).minimumScaleFactor(0.75)
                Spacer()
            }
            .padding(.horizontal, 16)
        }
        .buttonStyle(ReferenceOutlineButtonStyle(prominent: false))
        .disabled(!available)
    }

    private var finalWagers: some View {
        VStack(spacing: 18) {
            Text("FINAL JEOPARDY").font(.system(size: 42, weight: .black)).tracking(5)
            Text("Enter private wagers. Maximum: each contestant’s current score.").foregroundColor(.white.opacity(0.65))
            ForEach(gameState.players) { player in
                HStack {
                    Text(player.name.uppercased()).frame(width: 180, alignment: .leading)
                    if player.isBot {
                        Text("WAGER LOCKED").foregroundColor(.white.opacity(0.5))
                    } else {
                        TextField("0", value: wager(player.id), format: .number)
                            .textFieldStyle(.plain).padding(12).background(.white.opacity(0.08))
                    }
                }
            }
        }
    }

    private func wager(_ id: UUID) -> Binding<Int> {
        Binding(get: { gameState.wagers[id] ?? 0 }, set: { gameState.setWager(for: id, amount: $0) })
    }

    private func finalDraft(_ id: UUID) -> Binding<String> {
        Binding(get: { gameState.finalDrafts[id] ?? "" }, set: { gameState.finalDrafts[id] = $0 })
    }
}
