import SwiftUI
import JeopardyGameEngine

public struct LobbyView: View {
    @ObservedObject var gameState: GameState
    @ObservedObject var hostPlayer = HostAudioPlayer.shared
    @ObservedObject var theatre = TheatreDirector.shared

    public init(gameState: GameState) {
        self.gameState = gameState
    }

    @StateObject private var presentation = LobbyPresentationState()
    public var body: some View {
        ZStack {
            ArchivalBackdrop()
            if presentation.showSettings {
                settingsPage
            } else {
              ScrollView {
                VStack(alignment: .leading, spacing: 22) {
                    HStack {
                        Text(PlayerCopy.text("THE IRANIAN EDITION", "نسخهٔ ایرانی", language: gameState.configuration.language)).tracking(3).font(.system(size: 11, weight: .bold))
                        Spacer()
                        Button("Sound & match settings") { presentation.showSettings = true }
                            .buttonStyle(QuietButtonStyle())
                    }.foregroundColor(ArchivalTheme.gold24k)
                    HStack(alignment: .center) {
                        VStack(alignment: .leading, spacing: 18) {
                            Text("تاریخ روی صحنه").font(.system(size: 25, weight: .medium)).foregroundColor(ArchivalTheme.gold24k)
                            BroadcastTitle(compact: false)
                                .padding(.horizontal, 24)
                                .padding(.vertical, 18)
                                .background(ArchivalTheme.ink.opacity(0.72))
                                .overlay(RoundedRectangle(cornerRadius: 16).stroke(ArchivalTheme.gold24k.opacity(0.55), lineWidth: 1))
                                .cornerRadius(16)
                            Text("Five centuries.\nThe next move is yours.")
                                .font(.system(size: 30, weight: .regular, design: .serif)).lineSpacing(3)
                            Text("Courts and revolutions. Poetry and petroleum.\nA contest of knowledge, nerve, and timing.")
                                .font(.system(size: 15)).lineSpacing(5).foregroundColor(ArchivalTheme.textMuted)
                            HStack(spacing: 16) {
                                Button { theatre.stopMusic(); gameState.startNewGame() } label: {
                                    HStack(spacing: 24) { Text("TAKE THE STAGE").tracking(2); Image(systemName: "arrow.right") }
                                }
                                .buttonStyle(PrimaryShowButtonStyle())
                                .keyboardShortcut(.defaultAction)
                                .accessibilityIdentifier("start-match")
                                Button("Resume match") { gameState.restoreSavedGame() }.buttonStyle(QuietButtonStyle())
                            }.padding(.top, 12)
                        }
                        Spacer(minLength: 260)
                    }.frame(minHeight: 360).opacity(presentation.entered ? 1 : 0).offset(y: presentation.entered ? 0 : 16)
                    HStack(spacing: 32) {
                        Label(PlayerCopy.text("1,000 historical clues", "۱٬۰۰۰ سرنخ تاریخی", language: gameState.configuration.language), systemImage: "books.vertical")
                        Label("1–6 contestants", systemImage: "person.2")
                        Label("Two rounds & Final", systemImage: "trophy")
                        Spacer()
                    }.font(.system(size: 12, weight: .medium)).foregroundColor(ArchivalTheme.gold24k)
                    HStack(alignment: .top, spacing: 24) {
                        VStack(alignment: .leading, spacing: 16) {
                            Text("FROM THE ARCHIVE").font(.system(size: 10, weight: .bold)).tracking(3).foregroundColor(ArchivalTheme.gold24k)
                            HStack(spacing: 12) {
                                archiveCard("archive_qajar", title: "THE QAJAR COURT", caption: "Ahmad Shah · Bain Collection")
                                archiveCard("archive_tehran", title: "LIFE IN TEHRAN", caption: "Photochrom · circa 1890–1900")
                            }
                            Text("Choose a clue. Wait for the light. Buzz before your rivals. Correct answers win the value; wrong answers cost it.")
                                .font(.system(size: 13)).lineSpacing(3).foregroundColor(ArchivalTheme.textMuted)
                            Text("Arrow keys select a tile · Return opens it · Space buzzes for Player 1")
                                .font(.system(size: 11, weight: .medium)).foregroundColor(ArchivalTheme.gold24k)
                        }.frame(maxWidth: .infinity, alignment: .leading)
                        contestantsPanel
                    }
                    Text("Original stage illustration · Archival photographs: Library of Congress · Original instrumental score")
                        .font(.system(size: 10)).foregroundColor(ArchivalTheme.textMuted)
                }.padding(40)
              }
            }
        }.foregroundColor(ArchivalTheme.textParchment)
        .frame(minWidth: 1100, minHeight: 760)
        .onAppear {
            withAnimation(.easeOut(duration: 0.6)) { presentation.entered = true }
            theatre.startMenuMusic()
            theatre.playHost("welcome")
        }
    }

    private var settingsPage: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 22) {
                HStack {
                    Button { presentation.showSettings = false } label: {
                        Label("Back to lobby", systemImage: "chevron.left")
                    }.buttonStyle(QuietButtonStyle())
                    Spacer()
                    Text("MATCH SETTINGS").font(.system(size: 12, weight: .bold)).tracking(3).foregroundColor(ArchivalTheme.gold24k)
                }
                Text("Tune the broadcast before you take the stage.")
                    .font(.system(size: 34, design: .serif)).foregroundColor(ArchivalTheme.textParchment)
                Text("These choices apply to the next clue and can be changed without leaving the match setup.")
                    .font(.system(size: 14)).foregroundColor(ArchivalTheme.textMuted)
                setupPanel
                broadcastAudioControls
                Button { presentation.showSettings = false } label: {
                    HStack { Text("DONE — RETURN TO LOBBY"); Image(systemName: "arrow.right") }
                }.buttonStyle(PrimaryShowButtonStyle())
            }.padding(48).frame(maxWidth: 980, alignment: .leading)
        }
    }

    private func archiveCard(_ name: String, title: String, caption: String) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            if let art = StageAssets.image(name) {
                Image(nsImage: art).resizable().scaledToFill().frame(height: 105).clipped()
            }
            Text(title).font(.system(size: 11, weight: .bold)).tracking(1)
            Text(caption).font(.system(size: 10)).foregroundColor(ArchivalTheme.textMuted)
        }.frame(maxWidth: .infinity, alignment: .leading)
    }

    private var setupPanel: some View {
        VStack(alignment: .leading, spacing: 14) {
            panelHeading("MATCH SETUP", detail: "Configure broadcast presentation and audio rules.")

            settingRow("STAGE VISUAL THEME", icon: "paintpalette.fill") {
                Picker("Theme", selection: Binding(get: { ArchivalTheme.currentTheme }, set: { ArchivalTheme.currentTheme = $0; TheatreDirector.shared.play(.select) })) {
                    ForEach(GameStageTheme.allCases) { theme in
                        Text(theme.rawValue).tag(theme)
                    }
                }
                .pickerStyle(.segmented)
            }

            settingRow("RESPONSE MODE", icon: "mic.fill") {
                Picker("Response", selection: $gameState.configuration.mode) {
                    ForEach(GameMode.allCases, id: \.self) { mode in
                        Text(mode == .classic ? "CLASSIC (VOICE & BUZZ)" : "MULTIPLE CHOICE (4 OPTIONS)").tag(mode)
                    }
                }
                .pickerStyle(.segmented)
            }

            settingRow("HOST AUDIO & SPEECH", icon: "person.wave.2.fill") {
                VStack(alignment: .leading, spacing: 8) {
                    Toggle("Read clues aloud (disabled in written mode)", isOn: $gameState.configuration.audioSpeechEnabled)
                        .disabled(true)
                        .font(ArchivalTheme.sansFont(size: 11, weight: .semibold))
                        .foregroundColor(ArchivalTheme.textParchment)

                    if gameState.configuration.audioSpeechEnabled {
                        HStack(spacing: 12) {
                            Picker("Voice", selection: $hostPlayer.selectedVoice) {
                                ForEach(HostVoiceSelection.allCases, id: \.self) { voice in
                                    Text(voice.rawValue).tag(voice)
                                }
                            }
                            .pickerStyle(.menu)
                            .frame(maxWidth: 180)

                            Button("Preview Voice") {
                                hostPlayer.speak(text: "Welcome to Jeopardy: Iranian Edition.")
                            }
                            .buttonStyle(.bordered)
                            .controlSize(.small)
                        }

                        Text("Clue narration uses installed macOS voices. The opening host is a separate recorded performance.")
                            .font(ArchivalTheme.sansFont(size: 10))
                            .foregroundColor(ArchivalTheme.textMuted)
                            .lineSpacing(2)
                    } else {
                        Text("Studio Broadcast Mode active: TV theme, buzzers, and audience cheering enabled with fast visual clue reading.")
                            .font(ArchivalTheme.sansFont(size: 11))
                            .foregroundColor(ArchivalTheme.gold24k.opacity(0.9))
                    }
                }
            }

            settingRow("SPOKEN ANSWER LANGUAGE", icon: "character.book.closed.fill") {
                Picker("Language", selection: $gameState.configuration.language) {
                    ForEach(GameLanguage.allCases, id: \.self) { lang in
                        Text(lang == .english ? "ENGLISH" : "فارسی (PERSIAN)").tag(lang)
                    }
                }
                .pickerStyle(.segmented)
            }

            VStack(alignment: .leading, spacing: 5) {
                HStack(spacing: 8) {
                    Image(systemName: "keyboard.fill")
                        .foregroundColor(ArchivalTheme.gold24k)
                    Text("KEYBOARD & CONTROLLER CONTROLS:")
                        .font(ArchivalTheme.sansFont(size: 10, weight: .bold))
                        .tracking(1)
                        .foregroundColor(ArchivalTheme.textParchment)
                }
                Text("• Buzzers: [SPACE] for Player 1, [RETURN] for Player 2, [Z] for Player 3, [M] for Player 4\n• Multiple Choice: Keys [1], [2], [3], [4] or Gamepad [A, B, X, Y]\n• Classic Mode: Speech audio recognition with live typed fallback")
                    .font(ArchivalTheme.sansFont(size: 11))
                    .foregroundColor(ArchivalTheme.textMuted)
                    .lineSpacing(2.5)
            }
            .padding(10)
            .background(ArchivalTheme.ink.opacity(0.6))
            .cornerRadius(8)
        }
        .padding(20)
        .frame(maxWidth: .infinity, alignment: .leading)
        .archivalPanel(stroke: ArchivalTheme.cardBorder)
    }

    private var contestantsPanel: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack {
                panelHeading("CONTESTANTS", detail: "Illuminated stage podiums (1 to 6 players)")
                Spacer()
                Text("\(gameState.players.count) / 6")
                    .font(ArchivalTheme.sansFont(size: 16, weight: .black))
                    .foregroundColor(ArchivalTheme.gold24k)
            }

            ForEach(Array(gameState.players.enumerated()), id: \.element.id) { index, player in
                HStack(spacing: 12) {
                    Circle()
                        .fill(ArchivalTheme.playerColors[index % ArchivalTheme.playerColors.count])
                        .frame(width: 32, height: 32)
                        .overlay(Text("\(index + 1)").font(.caption.bold()).foregroundColor(.white))

                    VStack(alignment: .leading, spacing: 2) {
                        Text(player.name)
                            .font(ArchivalTheme.serifFont(size: 16, weight: .semibold))
                            .foregroundColor(ArchivalTheme.textParchment)

                        Text(player.isBot ? "BOT • \(botLabel(index))" : "HUMAN • \(inputLabel(index))")
                            .font(ArchivalTheme.sansFont(size: 10, weight: .bold))
                            .tracking(1)
                            .foregroundColor(player.isBot ? ArchivalTheme.gold24k : ArchivalTheme.textMuted)
                    }

                    Spacer()

                    Button(player.isBot ? "BOT" : "HUMAN") {
                        gameState.setBot(player.id, enabled: !player.isBot)
                    }
                    .buttonStyle(PillButtonStyle(active: player.isBot))

                    if gameState.players.count > 1 {
                        Button {
                            gameState.players.remove(at: index)
                        } label: {
                            Image(systemName: "minus.circle.fill")
                                .foregroundColor(ArchivalTheme.wrongRed.opacity(0.8))
                        }
                        .buttonStyle(.plain)
                    }
                }
                .padding(10)
                .background(ArchivalTheme.ink.opacity(0.65))
                .cornerRadius(8)
                .overlay(RoundedRectangle(cornerRadius: 8).stroke(ArchivalTheme.cardBorder, lineWidth: 1))
            }

            if gameState.players.count < 6 {
                HStack {
                    TextField("Contestant name", text: $gameState.newPlayerNameInput)
                        .textFieldStyle(.plain)
                        .padding(8)
                        .background(ArchivalTheme.ink.opacity(0.6))
                        .cornerRadius(6)

                    Button {
                        let name = gameState.newPlayerNameInput.trimmingCharacters(in: .whitespacesAndNewlines)
                        gameState.players.append(Player(name: name.isEmpty ? "Player \(gameState.players.count + 1)" : name))
                        gameState.newPlayerNameInput = ""
                    } label: {
                        HStack(spacing: 4) {
                            Image(systemName: "plus")
                            Text("ADD")
                        }
                    }
                    .buttonStyle(PillButtonStyle(active: true))
                }
            }
        }
        .padding(20)
        .frame(width: 480, alignment: .leading)
        .archivalPanel(stroke: ArchivalTheme.cardBorder)
    }

    private var broadcastAudioControls: some View {
        HStack(spacing: 16) {
            Image(systemName: "speaker.wave.3.fill")
                .foregroundColor(ArchivalTheme.gold24k)
                .font(.title3)

            VStack(alignment: .leading, spacing: 2) {
                Text("TELEVISION BROADCAST AUDIO")
                    .font(ArchivalTheme.sansFont(size: 10, weight: .bold))
                    .tracking(2)
                    .foregroundColor(ArchivalTheme.gold24k)

                Text("Original instrumental score, restrained cues, and a recorded opening host")
                    .font(ArchivalTheme.sansFont(size: 11))
                    .foregroundColor(ArchivalTheme.textMuted)
            }

            Spacer()

            HStack(spacing: 8) {
                audioPreviewButton(label: "▶ Main Theme", action: {
                    theatre.stopMusic()
                    theatre.startMenuMusic()
                })
                audioPreviewButton(label: "⏱️ 30s Think Music", action: {
                    theatre.startFinalThinkMusic()
                })
                audioPreviewButton(label: "🔔 Daily Double Sting", action: {
                    theatre.play(.wager)
                })
                audioPreviewButton(label: "⏹️ Stop", action: {
                    theatre.stopMusic()
                })
            }
        }
        .padding(14)
        .background(ArchivalTheme.cardSurface.opacity(0.92))
        .cornerRadius(10)
        .overlay(RoundedRectangle(cornerRadius: 10).stroke(ArchivalTheme.cardBorder, lineWidth: 1))
    }

    private func audioPreviewButton(label: String, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Text(label)
                .font(ArchivalTheme.sansFont(size: 10, weight: .bold))
                .foregroundColor(ArchivalTheme.textParchment)
                .padding(.horizontal, 10)
                .padding(.vertical, 6)
                .background(ArchivalTheme.ink.opacity(0.8))
                .cornerRadius(6)
                .overlay(RoundedRectangle(cornerRadius: 6).stroke(ArchivalTheme.gold24k.opacity(0.5), lineWidth: 1))
        }
        .buttonStyle(.plain)
    }

    private func panelHeading(_ title: String, detail: String) -> some View {
        VStack(alignment: .leading, spacing: 3) {
            Text(title)
                .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
                .tracking(2.5)
                .foregroundColor(ArchivalTheme.gold24k)
            Text(detail)
                .font(ArchivalTheme.serifFont(size: 13))
                .foregroundColor(ArchivalTheme.textMuted)
        }
    }

    private func settingRow<Content: View>(_ title: String, icon: String, @ViewBuilder content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Label(title, systemImage: icon)
                .font(ArchivalTheme.sansFont(size: 10, weight: .bold))
                .tracking(1.5)
                .foregroundColor(ArchivalTheme.textMuted)
            content()
        }
    }

    private func inputLabel(_ i: Int) -> String {
        gameState.controllerManager.assignedPlayers[i] == nil ? "KEYBOARD" : "GAMEPAD \(i + 1)"
    }

    private func botLabel(_ i: Int) -> String {
        ["NOVICE", "COMPETENT", "EXPERT", "HISTORIAN"][i % 4]
    }
}

private struct PillButtonStyle: ButtonStyle {
    let active: Bool
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .font(ArchivalTheme.sansFont(size: 10, weight: .bold))
            .foregroundColor(active ? ArchivalTheme.ink : ArchivalTheme.textMuted)
            .padding(.horizontal, 10)
            .padding(.vertical, 5)
            .background(active ? ArchivalTheme.gold24k : ArchivalTheme.cardSurface)
            .clipShape(Capsule())
            .scaleEffect(configuration.isPressed ? 0.95 : 1)
    }
}

private final class LobbyPresentationState: ObservableObject {
    @Published var showSettings = false
    @Published var entered = false
}
