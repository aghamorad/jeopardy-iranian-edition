import SwiftUI
import JeopardyGameEngine

public struct SourceInspectorView: View {
    public let clue: Clue
    public let onClose: () -> Void

    public init(clue: Clue, onClose: @escaping () -> Void) {
        self.clue = clue
        self.onClose = onClose
    }

    public var body: some View {
        VStack(spacing: 0) {
            // Header
            HStack {
                HStack(spacing: 8) {
                    Image(systemName: "books.vertical.fill")
                        .foregroundColor(ArchivalTheme.bronzeAccent)
                    Text("ARCHIVAL PROVENANCE INSPECTOR")
                        .font(ArchivalTheme.sansFont(size: 14, weight: .bold))
                        .foregroundColor(ArchivalTheme.textParchment)
                        .tracking(2)
                }

                Spacer()

                Button(action: onClose) {
                    HStack(spacing: 6) {
                        Image(systemName: "xmark")
                        Text("Close Inspector")
                    }
                    .font(ArchivalTheme.sansFont(size: 12, weight: .semibold))
                    .foregroundColor(ArchivalTheme.textParchment)
                    .padding(.horizontal, 12)
                    .padding(.vertical, 6)
                    .background(ArchivalTheme.cardSurface)
                    .cornerRadius(6)
                    .overlay(RoundedRectangle(cornerRadius: 6).stroke(ArchivalTheme.cardBorder, lineWidth: 1))
                }
                .buttonStyle(.plain)
            }
            .padding(20)
            .background(ArchivalTheme.cardSurface)

            Divider().background(ArchivalTheme.cardBorder)

            // Content Scroll
            ScrollView {
                VStack(alignment: .leading, spacing: 22) {
                    // Clue & Canonical Answer
                    inspectorSection(title: "CLUE") {
                        Text(clue.clueText)
                            .font(ArchivalTheme.serifFont(size: 16))
                            .foregroundColor(ArchivalTheme.textParchment)
                            .lineSpacing(4)
                    }

                    HStack(alignment: .top, spacing: 30) {
                        inspectorSection(title: "CANONICAL ANSWER") {
                            Text(clue.canonicalAnswer)
                                .font(ArchivalTheme.serifFont(size: 18, weight: .bold))
                                .foregroundColor(ArchivalTheme.bronzeAccent)
                        }

                        inspectorSection(title: "EVIDENCE TYPE") {
                            Text(clue.evidenceType.rawValue.uppercased())
                                .font(ArchivalTheme.sansFont(size: 12, weight: .bold))
                                .foregroundColor(.white)
                                .padding(.horizontal, 10)
                                .padding(.vertical, 4)
                                .background(evidenceColor(for: clue.evidenceType))
                                .cornerRadius(4)
                        }

                        inspectorSection(title: "VALIDATION STATUS") {
                            HStack(spacing: 6) {
                                Image(systemName: "checkmark.seal.fill")
                                    .foregroundColor(ArchivalTheme.correctGreen)
                                Text(clue.editorialValidationStatus.uppercased())
                                    .font(ArchivalTheme.sansFont(size: 12, weight: .bold))
                                    .foregroundColor(ArchivalTheme.textParchment)
                            }
                        }
                    }

                    // Accepted Aliases
                    inspectorSection(title: "ACCEPTED ALIASES & VARIANTS") {
                        FlowLayout(spacing: 8) {
                            ForEach(clue.acceptedAliases, id: \.self) { alias in
                                Text(alias)
                                    .font(ArchivalTheme.sansFont(size: 12))
                                    .foregroundColor(ArchivalTheme.textParchment)
                                    .padding(.horizontal, 10)
                                    .padding(.vertical, 4)
                                    .background(ArchivalTheme.cardSurface)
                                    .cornerRadius(4)
                                    .overlay(RoundedRectangle(cornerRadius: 4).stroke(ArchivalTheme.cardBorder, lineWidth: 1))
                            }
                        }
                    }

                    // Archival Source & Citation
                    inspectorSection(title: "PRIMARY ARCHIVAL SOURCE CITATION") {
                        VStack(alignment: .leading, spacing: 8) {
                            HStack {
                                Text("Work:")
                                    .font(ArchivalTheme.sansFont(size: 13, weight: .semibold))
                                    .foregroundColor(ArchivalTheme.bronzeAccent)
                                Text("\(clue.author) — \(clue.bookTitle)")
                                    .font(ArchivalTheme.sansFont(size: 13))
                                    .foregroundColor(ArchivalTheme.textParchment)
                            }

                            HStack {
                                Text("Chapter / Section:")
                                    .font(ArchivalTheme.sansFont(size: 13, weight: .semibold))
                                    .foregroundColor(ArchivalTheme.bronzeAccent)
                                Text(clue.chapter)
                                    .font(ArchivalTheme.sansFont(size: 13))
                                    .foregroundColor(ArchivalTheme.textParchment)
                            }

                            HStack {
                                Text("Exact Page Provenance:")
                                    .font(ArchivalTheme.sansFont(size: 13, weight: .semibold))
                                    .foregroundColor(ArchivalTheme.bronzeAccent)
                                Text("Page \(clue.page)")
                                    .font(ArchivalTheme.sansFont(size: 13, weight: .bold))
                                    .foregroundColor(ArchivalTheme.bronzeAccent)
                            }
                        }
                        .padding(14)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(ArchivalTheme.cardSurface)
                        .cornerRadius(6)
                    }

                    // Verbatim Supporting Passage
                    inspectorSection(title: "SUPPORTING VERBATIM PASSAGE FROM BOOK") {
                        Text("\"\(clue.supportingPassage)\"")
                            .font(ArchivalTheme.serifFont(size: 15))
                            .italic()
                            .foregroundColor(ArchivalTheme.textParchment)
                            .lineSpacing(5)
                            .padding(16)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .background(ArchivalTheme.cardSurface)
                            .cornerRadius(6)
                            .overlay(
                                RoundedRectangle(cornerRadius: 6)
                                    .stroke(ArchivalTheme.bronzeAccent.opacity(0.4), lineWidth: 1)
                            )
                    }

                    // Distractor Rationales (Multiple Choice Auditing)
                    inspectorSection(title: "MULTIPLE CHOICE DISTRACTORS & AUDIT RATIONALE") {
                        VStack(alignment: .leading, spacing: 10) {
                            ForEach(clue.distractorRationales, id: \.option) { rationale in
                                VStack(alignment: .leading, spacing: 4) {
                                    HStack {
                                        Text("• \(rationale.option)")
                                            .font(ArchivalTheme.sansFont(size: 13, weight: .bold))
                                            .foregroundColor(ArchivalTheme.textParchment)
                                        Spacer()
                                        Text("Dangerous Distractor")
                                            .font(ArchivalTheme.sansFont(size: 11))
                                            .foregroundColor(ArchivalTheme.textMuted)
                                    }
                                    Text("Why Plausible: \(rationale.whyPlausible)")
                                        .font(ArchivalTheme.sansFont(size: 12))
                                        .foregroundColor(ArchivalTheme.textMuted)
                                    Text("Why Strictly Wrong: \(rationale.whyWrong)")
                                        .font(ArchivalTheme.sansFont(size: 12))
                                        .foregroundColor(ArchivalTheme.wrongRed.opacity(0.9))
                                }
                                .padding(10)
                                .background(ArchivalTheme.cardSurface)
                                .cornerRadius(6)
                            }
                        }
                    }
                }
                .padding(24)
            }
        }
        .frame(minWidth: 800, minHeight: 650)
        .background(ArchivalTheme.backgroundDark)
    }

    @ViewBuilder
    private func inspectorSection<Content: View>(title: String, @ViewBuilder content: () -> Content) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title)
                .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
                .foregroundColor(ArchivalTheme.bronzeAccent)
                .tracking(2)
            content()
        }
    }

    private func evidenceColor(for type: EvidenceType) -> Color {
        switch type {
        case .establishedFact: return Color.blue.opacity(0.8)
        case .scholarlyInterpretation: return Color.purple.opacity(0.8)
        case .primaryTestimony: return Color.orange.opacity(0.8)
        case .disputed: return Color.red.opacity(0.8)
        }
    }
}

// Simple FlowLayout helper for SwiftUI
struct FlowLayout: Layout {
    var spacing: CGFloat = 8

    func sizeThatFits(proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) -> CGSize {
        let width = proposal.width ?? 500
        var height: CGFloat = 0
        var x: CGFloat = 0
        var y: CGFloat = 0
        var maxHeightInRow: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > width {
                x = 0
                y += maxHeightInRow + spacing
                maxHeightInRow = 0
            }
            maxHeightInRow = max(maxHeightInRow, size.height)
            x += size.width + spacing
        }
        height = y + maxHeightInRow
        return CGSize(width: width, height: height)
    }

    func placeSubviews(in bounds: CGRect, proposal: ProposedViewSize, subviews: Subviews, cache: inout ()) {
        var x = bounds.minX
        var y = bounds.minY
        var maxHeightInRow: CGFloat = 0

        for subview in subviews {
            let size = subview.sizeThatFits(.unspecified)
            if x + size.width > bounds.maxX {
                x = bounds.minX
                y += maxHeightInRow + spacing
                maxHeightInRow = 0
            }
            subview.place(at: CGPoint(x: x, y: y), proposal: ProposedViewSize(size))
            maxHeightInRow = max(maxHeightInRow, size.height)
            x += size.width + spacing
        }
    }
}
