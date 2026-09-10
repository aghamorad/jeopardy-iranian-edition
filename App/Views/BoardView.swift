import SwiftUI
import JeopardyGameEngine

public struct BoardView: View {
    @ObservedObject var gameState: GameState
    @ObservedObject private var theatre = TheatreDirector.shared

    public init(gameState: GameState) {
        self.gameState = gameState
    }

    public var body: some View {
        ZStack {
            ArchivalBackdrop()

            VStack(spacing: 0) {
                // Top Television Header Bar with Theme Switcher
                topHeaderBar

                // Host Broadcast HUD (Ostad Dariush Fani with Live Waveforms & Attitude)
                HostBroadcastHUD()
                    .padding(.horizontal, 28)
                    .padding(.top, 8)
                    .padding(.bottom, 6)

                // Main Game Show Board Grid (6 columns x 5 values)
                mainBoardGrid
                    .padding(.horizontal, 28)
                    .padding(.top, 10)
                    .padding(.bottom, 12)

                Spacer()

                // Bottom Illuminated Contestant Podiums
                bottomPodiumsBar
            }
        }
        .onAppear {
            // Keep the round bumper/music bed alive beneath clue presentation.
        }
        .frame(minWidth: 1100, minHeight: 760)
    }

    private var topHeaderBar: some View {
        HStack(spacing: 20) {
            HStack(spacing: 14) {
                BroadcastTitle(compact: true)

                VStack(alignment: .leading, spacing: 2) {
                    HStack(spacing: 6) {
                        Circle()
                            .fill(gameState.round == .double ? ArchivalTheme.wrongRed : ArchivalTheme.gold24k)
                            .frame(width: 8, height: 8)

                        Text(gameState.configuration.language == .persian
                             ? (gameState.round == .single ? "دور اول: ژوپاردی" : "دور دوم: ژوپاردی دوبرابر")
                             : (gameState.round == .single ? "ROUND I: JEOPARDY" : "ROUND II: DOUBLE JEOPARDY"))
                            .font(ArchivalTheme.sansFont(size: 13, weight: .black))
                            .tracking(2)
                            .foregroundColor(gameState.round == .double ? ArchivalTheme.gold24k : ArchivalTheme.textParchment)
                    }

                        Text(gameState.round == .single ? "VALUES: 10,000,000 – 200,000,000 تومان" : "VALUES: 20,000,000 – 200,000,000 تومان")
                        .font(ArchivalTheme.sansFont(size: 10, weight: .bold))
                        .foregroundColor(ArchivalTheme.textMuted)
                }
                .padding(.horizontal, 12)
                .padding(.vertical, 6)
                .background(ArchivalTheme.cardSurface.opacity(0.85))
                .cornerRadius(6)
                .overlay(RoundedRectangle(cornerRadius: 6).stroke(ArchivalTheme.cardBorder, lineWidth: 1))
            }

            Spacer()

            // Theme Switcher & Match Progress
            HStack(spacing: 12) {
                // Theme Picker
                Picker("Theme", selection: Binding(get: { ArchivalTheme.currentTheme }, set: { ArchivalTheme.currentTheme = $0; TheatreDirector.shared.play(.select) })) {
                    ForEach(GameStageTheme.allCases) { theme in
                        Text(theme.rawValue).tag(theme)
                    }
                }
                .pickerStyle(.menu)
                .frame(width: 220)


                let solvedCount = gameState.board.slots.filter { $0.isSolved }.count
                HStack(spacing: 6) {
                    Image(systemName: "checkmark.circle.fill")
                        .foregroundColor(ArchivalTheme.gold24k)
                    Text("\(solvedCount) / 30 CLUES")
                        .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
                        .foregroundColor(ArchivalTheme.textParchment)
                }
                .padding(.horizontal, 10)
                .padding(.vertical, 5)
                .background(ArchivalTheme.cardSurface)
                .cornerRadius(6)

                Button {
                    gameState.leaveMatch()
                } label: {
                    Image(systemName: "xmark.circle")
                        .font(.system(size: 16))
                        .foregroundColor(ArchivalTheme.textMuted)
                }
                .buttonStyle(.plain)
            }
        }
        .padding(.horizontal, 28)
        .padding(.vertical, 10)
                .background(Color.black.opacity(0.82))
        .overlay(
            Rectangle()
                .fill(
                    LinearGradient(
                    colors: [Color(red: 0.0, green: 0.78, blue: 0.38).opacity(0.7), Color.white.opacity(0.55), Color(red: 0.95, green: 0.10, blue: 0.14).opacity(0.7)],
                        startPoint: .leading,
                        endPoint: .trailing
                    )
                )
                .frame(height: 2),
            alignment: .bottom
        )
    }

    private var mainBoardGrid: some View {
        HStack(alignment: .top, spacing: 10) {
            ForEach(Array(0..<6), id: \.self) { (colIndex: Int) in
                VStack(spacing: 8) {
                    // Column Category Header
                    categoryHeader(at: colIndex)

                    // 5 Value Tiles
                    ForEach(Array(0..<5), id: \.self) { (rowIndex: Int) in
                        let slotIndex = colIndex * 5 + rowIndex
                        let slot = slotIndex < gameState.board.slots.count ? gameState.board.slots[slotIndex] : nil
                        ClueCardView(
                            slot: slot,
                            round: gameState.round,
                            onSelect: {
                                if let slot = slot, !slot.isSolved {
                                    TheatreDirector.shared.play(.select)
                                    gameState.selectSlot(categoryIndex: colIndex, valueIndex: rowIndex)
                                }
                            }
                        )
                        .overlay(RoundedRectangle(cornerRadius: 8).stroke(gameState.selectedBoardColumn == colIndex && gameState.selectedBoardRow == rowIndex ? ArchivalTheme.gold24k : Color.clear, lineWidth: 3))
                    }
                }
                .frame(maxWidth: .infinity)
            }
        }
    }

    private func categoryHeader(at colIndex: Int) -> some View {
        let rawCategory = colIndex < gameState.board.categories.count ? gameState.board.categories[colIndex] : "CATEGORY"
        let categoryName = PlayerCopy.category(rawCategory, language: gameState.configuration.language)
        return VStack(spacing: 5) {
            CategoryBadgeView(category: categoryName)

            Text(categoryName)
                .font(ArchivalTheme.sansFont(size: 11, weight: .black))
                .tracking(1)
                .multilineTextAlignment(.center)
                .foregroundColor(ArchivalTheme.textParchment)
                .lineLimit(2)
                .minimumScaleFactor(0.7)
                .frame(height: 36)
        }
        .padding(.horizontal, 6)
        .padding(.vertical, 8)
        .frame(maxWidth: .infinity)
        .frame(height: 84)
        .background(
            LinearGradient(
                colors: [
                    ArchivalTheme.cardSurface.opacity(0.98),
                    ArchivalTheme.cardSurface.opacity(0.85)
                ],
                startPoint: .top,
                endPoint: .bottom
            )
        )
        .cornerRadius(8)
        .overlay(
            RoundedRectangle(cornerRadius: 8)
                .stroke(
                    LinearGradient(
                    colors: [Color.white.opacity(0.38), ArchivalTheme.cardBorder.opacity(0.75)],
                        startPoint: .top,
                        endPoint: .bottom
                    ),
                    lineWidth: 1.2
                )
        )
        .shadow(color: .black.opacity(0.35), radius: 6, y: 3)
    }

    private var bottomPodiumsBar: some View {
        HStack(spacing: 16) {
            let maxScore = gameState.players.map { $0.score }.max() ?? 0
            ForEach(Array(gameState.players.enumerated()), id: \.element.id) { index, player in
                let isTurn = index == gameState.currentTurnPlayerIndex
                let isLeader = player.score == maxScore && player.score > 0
                let playerColor = ArchivalTheme.playerColors[index % ArchivalTheme.playerColors.count]

                HStack(spacing: 12) {
                    // Player Avatar with Crown if Leading
                    ZStack {
                        Circle()
                            .fill(playerColor)
                            .frame(width: 38, height: 38)
                            .overlay(
                                Text("\(index + 1)")
                                    .font(ArchivalTheme.sansFont(size: 14, weight: .black))
                                    .foregroundColor(.white)
                            )
                            .shadow(color: playerColor.opacity(0.6), radius: isTurn ? 8 : 2)

                        if isLeader {
                            Image(systemName: "crown.fill")
                                .font(.system(size: 13))
                                .foregroundColor(ArchivalTheme.gold24k)
                                .offset(y: -22)
                                .shadow(color: ArchivalTheme.gold24k, radius: 4)
                        }
                    }

                    VStack(alignment: .leading, spacing: 3) {
                        HStack(spacing: 6) {
                            Text(player.name)
                                .font(ArchivalTheme.serifFont(size: 14, weight: .bold))
                                .foregroundColor(ArchivalTheme.textParchment)
                                .lineLimit(1)

                            if player.isBot {
                                Text("BOT")
                                    .font(ArchivalTheme.sansFont(size: 8, weight: .black))
                                    .foregroundColor(ArchivalTheme.ink)
                                    .padding(.horizontal, 4)
                                    .padding(.vertical, 1)
                                    .background(ArchivalTheme.gold24k)
                                    .cornerRadius(3)
                            }
                        }

                        // Digital LED Glowing Score Meter
                        DigitalLEDScoreMeter(score: player.score, color: playerColor)
                    }

                    Spacer(minLength: 0)

                    // Buzzer Ready Indicator Lamp
                    Circle()
                        .fill(isTurn ? ArchivalTheme.correctGreen : ArchivalTheme.gold24k.opacity(0.3))
                        .frame(width: 10, height: 10)
                        .overlay(Circle().stroke(Color.white.opacity(0.4), lineWidth: 1))
                        .shadow(color: isTurn ? ArchivalTheme.correctGreen : Color.clear, radius: 6)
                }
                .padding(.horizontal, 14)
                .padding(.vertical, 10)
                .frame(maxWidth: .infinity)
                .background(
                    RoundedRectangle(cornerRadius: 10)
                        .fill(ArchivalTheme.cardSurface.opacity(0.92))
                        .overlay(
                            RoundedRectangle(cornerRadius: 10)
                                .stroke(
                                    isTurn ? playerColor : ArchivalTheme.cardBorder,
                                    lineWidth: isTurn ? 2 : 1
                                )
                        )
                )
                .shadow(color: isTurn ? playerColor.opacity(0.3) : Color.clear, radius: 8)
            }
        }
        .padding(.horizontal, 28)
        .padding(.vertical, 14)
        .background(ArchivalTheme.studioDark.opacity(0.95))
        .overlay(
            Rectangle()
                .fill(ArchivalTheme.cardBorder)
                .frame(height: 1),
            alignment: .top
        )
    }
}

// MARK: - Clue Card Matrix Tile
public struct ClueCardView: View {
    public let slot: BoardSlot?
    public let round: GameRound
    public let onSelect: () -> Void

    public init(slot: BoardSlot?, round: GameRound, onSelect: @escaping () -> Void) {
        self.slot = slot
        self.round = round
        self.onSelect = onSelect
    }

    public var body: some View {
        Button(action: onSelect) {
            ZStack {
                // Card Background
                RoundedRectangle(cornerRadius: 8)
                    .fill(
                        slot?.isSolved == true
                            ? AnyShapeStyle(ArchivalTheme.ink.opacity(0.4))
                            : AnyShapeStyle(
                                LinearGradient(
                                    colors: [
                                    Color.black.opacity(0.88),
                                    Color(red: 0.035, green: 0.045, blue: 0.07).opacity(0.96)
                                    ],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                    )

                // Bevel border
                RoundedRectangle(cornerRadius: 8)
                    .stroke(
                        slot?.isSolved == true
                            ? AnyShapeStyle(ArchivalTheme.cardBorder.opacity(0.2))
                            : AnyShapeStyle(
                                LinearGradient(
                                    colors: [
                                        Color.white.opacity(0.34),
                                        Color.white.opacity(0.10)
                                    ],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            ),
                        lineWidth: 1.2
                    )

                if let slot = slot, !slot.isSolved {
                    VStack(spacing: 0) {
                        Text(ArchivalTheme.toman(slot.value))
                            .font(ArchivalTheme.monoFont(size: 18, weight: .black))
                            .tracking(0)
                            .foregroundColor(ArchivalTheme.textParchment)
                            .shadow(color: .white.opacity(0.18), radius: 4, x: 0, y: 1)
                    }
                }
            }
            .frame(maxWidth: .infinity)
            .frame(height: 78)
            .shadow(color: slot?.isSolved == true ? Color.clear : .black.opacity(0.4), radius: 6, y: 3)
        }
        .buttonStyle(ClueTileButtonStyle())
        .disabled(slot?.isSolved ?? true)
    }

    private func persianCurrency(_ val: Int) -> String {
        switch val {
        default: return ArchivalTheme.toman(val)
        }
    }
}
