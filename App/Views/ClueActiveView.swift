import SwiftUI
import JeopardyGameEngine

public struct ClueActiveView: View {
    @ObservedObject var gameState: GameState
    @ObservedObject var hostEngine = OstadFaniEngine.shared

    public init(gameState: GameState) {
        self.gameState = gameState
    }

    public var body: some View {
        ZStack {
            ArchivalBackdrop()

            if let slot = gameState.activeSlot {
                let clue = slot.clue

                VStack(spacing: 0) {
                    // Top Bar (Category Badge, Value, Close)
                    clueTopBar(clue: clue)

                    // Ostad Dariush Fani's Live Broadcast Box
                    HostBroadcastHUD()
                        .padding(.horizontal, 40)
                        .padding(.top, 6)
                        .padding(.bottom, 12)

                    Spacer(minLength: 18)
                    // Center Clue Centerpiece / Stage
                    ZStack {
                        switch gameState.phase {
                        case .specialWager(let player, let clue):
                            sealedWagerStage(player: player, clue: clue)

                        case .clueReading, .buzzerArmed, .answering, .evaluating, .clueResolved:
                            clueDisplayStage(clue: clue)

                        case .finalWager:
                            finalWageringStage()

                        case .finalClue(let category, let clue):
                            finalClueStage(category: category, clue: clue)

                        case .finalAnswering(let player, let clue):
                            finalAnsweringStage(player: player, clue: clue)

                        case .finalReveal(let clue, let winner):
                            finalWinnerCeremonyStage(clue: clue, winner: winner)

                        default:
                            clueDisplayStage(clue: clue)
                        }
                    }

                    Spacer()

                    // Bottom Interaction Zone (Buzzer, Options, or Next Action)
                    bottomInteractionArea(clue: clue)
                }
                .padding(.horizontal, 40)
                .padding(.vertical, 16)
            }

            // Confetti Shower on Victory
            if case .finalReveal = gameState.phase {
                ConfettiFountainView()
            }
        }
        .onAppear {
            if case .finalClue = gameState.phase {
                TheatreDirector.shared.startFinalThinkMusic()
                hostEngine.sayFinalJeopardy()
            }
        }
    }

    // MARK: - Top Bar
    private func clueTopBar(clue: Clue) -> some View {
        let displayCategory = PlayerCopy.category(clue.category, language: gameState.configuration.language)
        return HStack {
            HStack(spacing: 12) {
                CategoryBadgeView(category: displayCategory)

                VStack(alignment: .leading, spacing: 2) {
                    Text(displayCategory.uppercased())
                        .font(ArchivalTheme.sansFont(size: 13, weight: .bold))
                        .foregroundColor(ArchivalTheme.gold24k)
                        .tracking(2)

                    Text("\(clue.historicalPeriod) • \(clue.theme)")
                        .font(ArchivalTheme.sansFont(size: 11, weight: .medium))
                        .foregroundColor(ArchivalTheme.textMuted)
                }
            }

            Spacer()

            let displayValue = gameState.activeSlot?.value ?? clue.value
            if displayValue > 0 {
                Text(ArchivalTheme.toman(displayValue))
                    .font(ArchivalTheme.monoFont(size: 20, weight: .black))
                    .tracking(0.5)
                    .foregroundColor(ArchivalTheme.gold24k)
                    .shadow(color: ArchivalTheme.gold24k.opacity(0.55), radius: 8)
            } else {
                Text("FINAL JEOPARDY")
                    .font(ArchivalTheme.sansFont(size: 14, weight: .black))
                    .tracking(3)
                    .foregroundColor(ArchivalTheme.gold24k)
            }

            Spacer()

            Button {
                gameState.returnToBoard()
            } label: {
                Image(systemName: "xmark.circle.fill")
                    .font(.system(size: 22))
                    .foregroundColor(ArchivalTheme.textMuted)
            }
            .buttonStyle(.plain)
        }
        .padding(.horizontal, 40)
        .padding(.top, 12)
        .padding(.bottom, 6)
    }

    // MARK: - Clue Display Stage
    private func clueDisplayStage(clue: Clue) -> some View {
        VStack(spacing: 20) {
            // Main Illuminated Clue Card
            VStack(spacing: 16) {
                Text(clue.clueText)
                    .font(ArchivalTheme.serifFont(size: 24, weight: .medium))
                    .foregroundColor(ArchivalTheme.textParchment)
                    .multilineTextAlignment(.center)
                    .lineSpacing(8)
                    .padding(.horizontal, 32)
                    .padding(.vertical, 28)
                    .frame(maxWidth: 900)
            }
            .background(
                RoundedRectangle(cornerRadius: 14)
                    .fill(
                        LinearGradient(
                            colors: [
                                ArchivalTheme.cardSurface.opacity(0.98),
                                ArchivalTheme.cardSurface.opacity(0.92)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
            )
            .overlay(
                RoundedRectangle(cornerRadius: 14)
                    .stroke(
                        LinearGradient(
                            colors: [ArchivalTheme.gold24k.opacity(0.85), ArchivalTheme.cardBorder],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        ),
                        lineWidth: 1.8
                    )
            )
            .shadow(color: .black.opacity(0.5), radius: 20, y: 10)

            // Dynamic Status Banner
            statusBanner(clue: clue)
        }
    }

    // MARK: - Status Banner
    @ViewBuilder
    private func statusBanner(clue: Clue) -> some View {
        switch gameState.phase {
        case .clueReading:
            HStack(spacing: 8) {
                ProgressView().controlSize(.small)
                Text("HOST IS READING THE CLUE • BUZZERS ARMED SHORTLY")
                    .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
                    .tracking(2)
                    .foregroundColor(ArchivalTheme.gold24k)
            }
            .padding(.horizontal, 16)
            .padding(.vertical, 6)
            .background(ArchivalTheme.cardSurface)
            .cornerRadius(20)

        case .buzzerArmed:
            HStack(spacing: 8) {
                Circle().fill(ArchivalTheme.buzzerArmedGlow).frame(width: 10, height: 10)
                    .shadow(color: ArchivalTheme.buzzerArmedGlow, radius: 4)
                Text("BUZZERS ARMED! PRESS SPACE OR CONTROLLER TO BUZZ")
                    .font(ArchivalTheme.sansFont(size: 12, weight: .black))
                    .tracking(2)
                    .foregroundColor(ArchivalTheme.ink)
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 8)
            .background(ArchivalTheme.buzzerArmedGlow)
            .cornerRadius(20)
            .shadow(color: ArchivalTheme.buzzerArmedGlow.opacity(0.5), radius: 10)

        case .answering(let player, _, let remaining):
            HStack(spacing: 12) {
                Text("\(player.name.uppercased()) HAS THE FLOOR")
                    .font(ArchivalTheme.sansFont(size: 12, weight: .black))
                    .tracking(2)
                    .foregroundColor(ArchivalTheme.gold24k)

                // Animated countdown timer ring & bar
                HStack(spacing: 4) {
                    Image(systemName: "timer")
                        .foregroundColor(remaining < 3 ? ArchivalTheme.wrongRed : ArchivalTheme.gold24k)

                    Text(String(format: "%.1fs", remaining))
                        .font(ArchivalTheme.monoFont(size: 14, weight: .black))
                        .foregroundColor(remaining < 3 ? ArchivalTheme.wrongRed : ArchivalTheme.textParchment)
                }
                .padding(.horizontal, 8)
                .padding(.vertical, 2)
                .background(Color.black.opacity(0.6))
                .cornerRadius(4)
            }
            .padding(.horizontal, 18)
            .padding(.vertical, 6)
            .background(ArchivalTheme.cardSurface)
            .cornerRadius(20)

        case .clueResolved(_, let winner, let remark, _):
            HStack(spacing: 10) {
                Image(systemName: winner != nil ? "checkmark.seal.fill" : "xmark.seal.fill")
                    .foregroundColor(winner != nil ? ArchivalTheme.correctGreen : ArchivalTheme.wrongRed)

                Text(winner != nil ? "\(winner!.name): \(remark)" : "NO CORRECT ANSWER • \(remark)")
                    .font(ArchivalTheme.serifFont(size: 14, weight: .bold))
                    .foregroundColor(winner != nil ? ArchivalTheme.correctGreen : ArchivalTheme.wrongRed)
            }
            .padding(.horizontal, 18)
            .padding(.vertical, 8)
            .background(ArchivalTheme.cardSurface)
            .cornerRadius(20)

        default:
            EmptyView()
        }
    }

    // MARK: - Sealed Wager / Daily Double Stage
    private func sealedWagerStage(player: Player, clue: Clue) -> some View {
        VStack(spacing: 20) {
            // Imperial Wax Seal Card
            ZStack {
                RoundedRectangle(cornerRadius: 16)
                    .fill(
                        LinearGradient(
                            colors: [
                                Color(red: 0.22, green: 0.16, blue: 0.12),
                                Color(red: 0.12, green: 0.08, blue: 0.06)
                            ],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .frame(width: 540, height: 260)
                    .overlay(
                        RoundedRectangle(cornerRadius: 16)
                            .stroke(ArchivalTheme.gold24k, lineWidth: 2)
                    )
                    .shadow(color: ArchivalTheme.redSeal.opacity(0.4), radius: 24, y: 10)

                VStack(spacing: 12) {
                    Circle()
                        .fill(ArchivalTheme.redSeal)
                        .frame(width: 64, height: 64)
                        .overlay(
                            Image(systemName: "seal.fill")
                                .font(.system(size: 32))
                                .foregroundColor(ArchivalTheme.gold24k)
                        )
                        .shadow(color: ArchivalTheme.redSeal, radius: 8)

                    Text("DAILY DOUBLE • حکم مهروموم سلطنتی")
                        .font(ArchivalTheme.sansFont(size: 14, weight: .black))
                        .tracking(3)
                        .foregroundColor(ArchivalTheme.gold24k)

                    Text("\(player.name.uppercased()), CHOOSE YOUR STAKE")
                        .font(ArchivalTheme.serifFont(size: 20, weight: .bold))
                        .foregroundColor(ArchivalTheme.textParchment)

                    Text("Max Wager: \(ArchivalTheme.toman(max(player.score, 200_000_000)))")
                        .font(ArchivalTheme.sansFont(size: 12))
                        .foregroundColor(ArchivalTheme.textMuted)
                }
            }

            // Interactive Quick-Wager Chips
            let maxWager = max(player.score, 200_000_000)
            HStack(spacing: 12) {
                wagerChipButton(label: "۵۰ میلیون", amount: min(50_000_000, maxWager))
                wagerChipButton(label: "۱۰۰ میلیون", amount: min(100_000_000, maxWager))
                if maxWager >= 200_000_000 {
                    wagerChipButton(label: "۲۰۰ میلیون", amount: min(200_000_000, maxWager))
                }
                wagerChipButton(label: "ALL IN / TRUE DD (\(ArchivalTheme.toman(maxWager)))", amount: maxWager, isAllIn: true)
            }

            Button {
                gameState.revealSpecialWager(amount: gameState.activeSpecialWager)
            } label: {
                Text("LOCK IN WAGER: \(ArchivalTheme.toman(gameState.activeSpecialWager))")
                    .font(ArchivalTheme.sansFont(size: 13, weight: .black))
                    .tracking(2)
            }
            .buttonStyle(PrimaryShowButtonStyle())
        }
    }

    private func wagerChipButton(label: String, amount: Int, isAllIn: Bool = false) -> some View {
        Button {
            gameState.activeSpecialWager = amount
        } label: {
            Text(label)
                .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
                .foregroundColor(gameState.activeSpecialWager == amount ? ArchivalTheme.ink : ArchivalTheme.textParchment)
                .padding(.horizontal, 14)
                .padding(.vertical, 8)
                .background(gameState.activeSpecialWager == amount ? ArchivalTheme.gold24k : (isAllIn ? ArchivalTheme.redSeal : ArchivalTheme.cardSurface))
                .cornerRadius(20)
                .overlay(RoundedRectangle(cornerRadius: 20).stroke(ArchivalTheme.gold24k, lineWidth: 1))
        }
        .buttonStyle(.plain)
    }

    // MARK: - Final Wagering Stage
    private func finalWageringStage() -> some View {
        VStack(spacing: 20) {
            Text("FINAL JEOPARDY: SECRET WAGERS")
                .font(ArchivalTheme.sansFont(size: 14, weight: .black))
                .tracking(3)
                .foregroundColor(ArchivalTheme.gold24k)

            ForEach(gameState.players) { player in
                HStack(spacing: 16) {
                    Circle()
                        .fill(ArchivalTheme.playerColors[0])
                        .frame(width: 32, height: 32)
                        .overlay(Text("\(player.name.prefix(1))").font(.caption.bold()).foregroundColor(.white))

                    VStack(alignment: .leading, spacing: 2) {
                        Text(player.name)
                            .font(ArchivalTheme.serifFont(size: 15, weight: .bold))
                            .foregroundColor(ArchivalTheme.textParchment)
                    Text("Current Score: \(ArchivalTheme.toman(player.score))")
                            .font(ArchivalTheme.sansFont(size: 11))
                            .foregroundColor(ArchivalTheme.gold24k)
                    }

                    Spacer()

                    if player.isBot {
                        Text("SECRET BOT WAGER STORED")
                            .font(ArchivalTheme.sansFont(size: 10, weight: .bold))
                            .foregroundColor(ArchivalTheme.textMuted)
                    } else {
                        HStack {
                            Text("تومان")
                                .foregroundColor(ArchivalTheme.gold24k)
                            TextField("0", value: Binding(
                                get: { gameState.wagers[player.id] ?? 0 },
                                set: { gameState.setWager(for: player.id, amount: $0) }
                            ), format: .number)
                            .textFieldStyle(.plain)
                            .frame(width: 80)
                            .padding(6)
                            .background(ArchivalTheme.ink)
                            .cornerRadius(6)
                        }
                    }
                }
                .padding(12)
                .background(ArchivalTheme.cardSurface)
                .cornerRadius(8)
                .frame(maxWidth: 500)
            }

            Button {
                gameState.revealFinalClue()
            } label: {
                Text("LOCK IN WAGERS & REVEAL FINAL CLUE")
                    .font(ArchivalTheme.sansFont(size: 13, weight: .black))
                    .tracking(2)
            }
            .buttonStyle(PrimaryShowButtonStyle())
        }
    }

    // MARK: - Final Clue Stage
    private func finalClueStage(category: String, clue: Clue) -> some View {
        VStack(spacing: 24) {
            Text(category.uppercased())
                .font(ArchivalTheme.sansFont(size: 14, weight: .bold))
                .tracking(3)
                .foregroundColor(ArchivalTheme.gold24k)

            VStack(spacing: 14) {
                Text(clue.clueText)
                    .font(ArchivalTheme.serifFont(size: 26, weight: .semibold))
                    .foregroundColor(ArchivalTheme.textParchment)
                    .multilineTextAlignment(.center)
                    .lineSpacing(8)
                    .padding(32)
            }
            .background(ArchivalTheme.cardSurface)
            .cornerRadius(12)
            .overlay(RoundedRectangle(cornerRadius: 12).stroke(ArchivalTheme.gold24k, lineWidth: 2))
            .frame(maxWidth: 900)

            Text("\(gameState.finalRemaining) SECONDS · WRITE YOUR ANSWERS")
                .font(.system(size: 15, weight: .bold, design: .monospaced)).foregroundColor(ArchivalTheme.gold24k)
            ForEach(gameState.players.filter { !$0.isBot }) { player in
                HStack(spacing: 14) {
                    Text(player.name).frame(width: 100, alignment: .leading)
                    if gameState.finalResponses.contains(player.id) {
                        Label("Answer locked", systemImage: "checkmark.seal.fill").foregroundColor(ArchivalTheme.gold24k)
                    } else {
                        SecureField("Private final answer", text: Binding(get: { gameState.finalDrafts[player.id] ?? "" }, set: { gameState.finalDrafts[player.id] = $0 }))
                            .textFieldStyle(.roundedBorder)
                            .onSubmit { gameState.submitFinalAnswer(playerID: player.id, text: gameState.finalDrafts[player.id] ?? "") }
                        Button("Lock answer") { gameState.submitFinalAnswer(playerID: player.id, text: gameState.finalDrafts[player.id] ?? "") }.buttonStyle(QuietButtonStyle())
                    }
                }.frame(maxWidth: 700)
            }
        }
    }

    // MARK: - Final Answering Stage
    private func finalAnsweringStage(player: Player, clue: Clue) -> some View {
        VStack(spacing: 20) {
            Text("\(player.name) ANSWERING FINAL JEOPARDY")
                .font(ArchivalTheme.sansFont(size: 13, weight: .bold))
                .foregroundColor(ArchivalTheme.gold24k)

            if gameState.configuration.mode == .multipleChoice {
                multipleChoiceGrid(clue: clue, isEnabled: true)
            } else {
                typedAnsweringArea(player: player, clue: clue)
            }
        }
    }

    // MARK: - Winner Presentation Ceremony
    private func finalWinnerCeremonyStage(clue: Clue, winner: Player?) -> some View {
        VStack(spacing: 20) {
            // Crown / Trophy
            VStack(spacing: 8) {
                if let trophyURL = resolveLocalImageURL(named: "trophy_cup"),
                   let trophyImg = PlatformImageLoader.load(contentsOf: trophyURL) {
                    Image(platformImage: trophyImg)
                        .resizable()
                        .aspectRatio(contentMode: .fit)
                        .frame(width: 110, height: 110)
                } else {
                    Image(systemName: "trophy.fill")
                        .font(.system(size: 64))
                        .foregroundColor(ArchivalTheme.gold24k)
                }

                Text("MATCH COMPLETED • قهرمان تاریخ ایران")
                    .font(ArchivalTheme.sansFont(size: 13, weight: .black))
                    .tracking(3)
                    .foregroundColor(ArchivalTheme.gold24k)

                if let winner = winner {
                    Text("\(winner.name) IS THE CHAMPION!")
                        .font(ArchivalTheme.serifFont(size: 32, weight: .heavy))
                        .foregroundColor(ArchivalTheme.textParchment)
                        .shadow(color: ArchivalTheme.gold24k.opacity(0.4), radius: 8)

                    Text("Final Score: \(ArchivalTheme.toman(winner.score))")
                        .font(ArchivalTheme.serifFont(size: 24, weight: .bold))
                        .foregroundColor(ArchivalTheme.gold24k)
                } else {
                    Text("A HARD-FOUGHT DRAW ACROSS THE REALM!")
                        .font(ArchivalTheme.serifFont(size: 26, weight: .bold))
                        .foregroundColor(ArchivalTheme.textParchment)
                }
            }

            // Final Podiums Standing
            HStack(spacing: 14) {
                ForEach(gameState.players.sorted(by: { $0.score > $1.score })) { player in
                    VStack(spacing: 4) {
                        Text(player.name)
                            .font(ArchivalTheme.serifFont(size: 14, weight: .bold))
                            .foregroundColor(ArchivalTheme.textParchment)
                        Text(ArchivalTheme.toman(player.score))
                            .font(ArchivalTheme.monoFont(size: 18, weight: .black))
                            .foregroundColor(ArchivalTheme.gold24k)
                    }
                    .padding(12)
                    .frame(minWidth: 120)
                    .background(ArchivalTheme.cardSurface)
                    .cornerRadius(8)
                    .overlay(RoundedRectangle(cornerRadius: 8).stroke(ArchivalTheme.cardBorder, lineWidth: 1))
                }
            }

            Button {
                gameState.startNewGame()
            } label: {
                Text("PLAY AGAIN WITH NEW CATEGORIES")
                    .font(ArchivalTheme.sansFont(size: 13, weight: .black))
                    .tracking(2)
            }
            .buttonStyle(PrimaryShowButtonStyle())
        }
    }

    // MARK: - Bottom Interaction Area
    @ViewBuilder
    private func bottomInteractionArea(clue: Clue) -> some View {
        switch gameState.phase {
        case .clueReading, .buzzerArmed:
            VStack(spacing: 14) {
                HStack(spacing: 14) {
                    ForEach(Array(gameState.players.enumerated()), id: \.element.id) { index, player in
                        Button { gameState.handleBuzz(playerIndex: index) } label: {
                            VStack(spacing: 7) {
                                Text(player.name.uppercased()).font(.system(size: 12, weight: .bold)).tracking(1)
                                Text(ArchivalTheme.toman(player.score)).font(.system(size: 17, weight: .bold, design: .monospaced))
                                Text(player.isBot ? "BOT" : "BUZZ").font(.system(size: 10, weight: .black)).tracking(2)
                            }.frame(maxWidth: .infinity).padding(20)
                                .background(ArchivalTheme.ink.opacity(0.94))
                                .overlay(RoundedRectangle(cornerRadius: 10).stroke(ArchivalTheme.playerColors[index % ArchivalTheme.playerColors.count], lineWidth: 2))
                        }.buttonStyle(ClueTileButtonStyle()).disabled(player.isBot)
                    }
                }
                Button("No answer · reveal") { gameState.passClue() }.buttonStyle(QuietButtonStyle())
            }

        case .answering(let player, let clue, _):
            if gameState.configuration.mode == .multipleChoice {
                multipleChoiceGrid(clue: clue, isEnabled: true)
            } else {
                typedAnsweringArea(player: player, clue: clue)
            }

        case .evaluating:
            HStack(spacing: 12) {
                ProgressView().controlSize(.small)
                Text("ADJUDICATING HISTORICAL ACCURACY...")
                    .font(ArchivalTheme.sansFont(size: 12, weight: .bold))
                    .tracking(2)
                    .foregroundColor(ArchivalTheme.gold24k)
            }
            .padding(14)

        case .clueResolved(let clue, _, _, let explanation):
            VStack(spacing: 14) {
                // Sourced Academic Provenance Citation
                HStack(spacing: 10) {
                    Image(systemName: "book.closed.fill")
                        .foregroundColor(ArchivalTheme.gold24k)

                    Text("HISTORICAL SOURCE:")
                        .font(ArchivalTheme.sansFont(size: 10, weight: .bold))
                        .foregroundColor(ArchivalTheme.gold24k)

                    Text("\(clue.bookTitle), p. \(clue.page)")
                        .font(ArchivalTheme.serifFont(size: 13, weight: .medium))
                        .foregroundColor(ArchivalTheme.textParchment)

                    Spacer()

                    Text("Correct Answer: \(clue.canonicalAnswer)")
                        .font(ArchivalTheme.serifFont(size: 14, weight: .bold))
                        .foregroundColor(ArchivalTheme.gold24k)
                }
                .padding(.horizontal, 16)
                .padding(.vertical, 8)
                .background(ArchivalTheme.cardSurface)
                .cornerRadius(6)

                Text(explanation)
                    .font(ArchivalTheme.serifFont(size: 13))
                    .foregroundColor(ArchivalTheme.textMuted)
                    .lineLimit(2)
                    .multilineTextAlignment(.center)

                Button {
                    gameState.returnToBoard()
                } label: {
                    Text("CONTINUE TO BOARD")
                        .font(ArchivalTheme.sansFont(size: 12, weight: .black))
                        .tracking(2)
                }
                .buttonStyle(PrimaryShowButtonStyle())
            }
            .frame(maxWidth: 800)

        default:
            EmptyView()
        }
    }

    @ViewBuilder
    private func multipleChoiceGrid(clue: Clue, isEnabled: Bool) -> some View {
        let labels = ["A", "B", "C", "D"]
        let keyHints = ["[1/A]", "[2/B]", "[3/X]", "[4/Y]"]

        LazyVGrid(columns: [GridItem(.flexible()), GridItem(.flexible())], spacing: 14) {
            ForEach(Array(clue.options.indices.prefix(4)), id: \.self) { optIdx in
                let option = clue.options[optIdx]
                Button(action: {
                    if isEnabled {
                        gameState.handleMultipleChoice(playerIndex: gameState.currentTurnPlayerIndex, optionIndex: optIdx)
                    }
                }) {
                    HStack(spacing: 14) {
                        Text(labels[optIdx])
                            .font(ArchivalTheme.sansFont(size: 15, weight: .black))
                            .foregroundColor(ArchivalTheme.gold24k)
                            .frame(width: 32, height: 32)
                            .background(ArchivalTheme.studioDark)
                            .clipShape(Circle())
                            .overlay(Circle().stroke(ArchivalTheme.gold24k.opacity(0.6), lineWidth: 1))

                        Text(option)
                            .font(ArchivalTheme.serifFont(size: 17, weight: .semibold))
                            .foregroundColor(ArchivalTheme.textParchment)

                        Spacer()

                        Text(keyHints[optIdx])
                            .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
                            .foregroundColor(ArchivalTheme.textMuted)
                    }
                    .padding(14)
                    .background(
                        LinearGradient(
                            colors: [ArchivalTheme.cardSurface, ArchivalTheme.cardSurface.opacity(0.8)],
                            startPoint: .topLeading,
                            endPoint: .bottomTrailing
                        )
                    )
                    .cornerRadius(8)
                    .overlay(
                        RoundedRectangle(cornerRadius: 8)
                            .stroke(isEnabled ? ArchivalTheme.gold24k.opacity(0.85) : ArchivalTheme.cardBorder, lineWidth: 1.5)
                    )
                }
                .buttonStyle(ClueTileButtonStyle())
                .disabled(!isEnabled)
            }
        }
        .frame(maxWidth: 900)
    }

    @ViewBuilder
    private func typedAnsweringArea(player: Player, clue: Clue) -> some View {
        VStack(spacing: 10) {
            HStack(spacing: 12) {
                Image(systemName: "keyboard.fill")
                    .foregroundColor(ArchivalTheme.gold24k)
                    .font(.title3)
                    Text(PlayerCopy.text("TYPE YOUR ANSWER", "پاسخ خود را بنویسید", language: gameState.configuration.language))
                    .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
                    .foregroundColor(ArchivalTheme.gold24k)
            }

            HStack {
                TextField(PlayerCopy.text("Type the response…", "پاسخ را وارد کنید…", language: gameState.configuration.language), text: $gameState.manualAnswerInput)
                    .onSubmit { gameState.submitManualOrSimulatedAnswer(gameState.manualAnswerInput) }
                    .textFieldStyle(.plain)
                    .font(ArchivalTheme.serifFont(size: 17))
                    .padding(10)
                    .background(ArchivalTheme.cardSurface)
                    .cornerRadius(6)
                    .overlay(RoundedRectangle(cornerRadius: 6).stroke(ArchivalTheme.gold24k, lineWidth: 1))

                Button(PlayerCopy.text("LOCK ANSWER", "ثبت پاسخ", language: gameState.configuration.language)) {
                    let text = gameState.manualAnswerInput.trimmingCharacters(in: .whitespacesAndNewlines)
                    if !text.isEmpty {
                        gameState.submitManualOrSimulatedAnswer(text)
                    }
                }
                .buttonStyle(PrimaryShowButtonStyle())
            }
            .frame(maxWidth: 600)
        }
    }

    private func resolveLocalImageURL(named: String) -> URL? {
        if let resURL = Bundle.main.resourceURL?.appendingPathComponent("\(named).png"),
           FileManager.default.fileExists(atPath: resURL.path) {
            return resURL
        }
        if let url = Bundle.main.url(forResource: named, withExtension: "png") {
            return url
        }
        let candidatePaths = [
            "/Users/Morad/Desktop/Jeopardy - Iranian Edition/App/Resources/\(named).png",
            "App/Resources/\(named).png"
        ]
        for path in candidatePaths {
            if FileManager.default.fileExists(atPath: path) {
                return URL(fileURLWithPath: path)
            }
        }
        return nil
    }
}
