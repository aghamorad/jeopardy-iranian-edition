#!/usr/bin/env python3
import sys

# 1. Update ArchivalTheme.swift: Add ClueTileButtonStyle if missing
with open("App/Theme/ArchivalTheme.swift", "r", encoding="utf-8") as f:
    content = f.read()

if "struct ClueTileButtonStyle" not in content:
    content += """

public struct ClueTileButtonStyle: ButtonStyle {
    public init() {}
    public func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.96 : 1.0)
            .brightness(configuration.isPressed ? 0.12 : 0.0)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }
}
"""
    with open("App/Theme/ArchivalTheme.swift", "w", encoding="utf-8") as f:
        f.write(content)
    print("Added ClueTileButtonStyle to ArchivalTheme.swift")

# 2. Update BoardView.swift: Fix AnyShapeStyle in ClueCardView and remove private ClueTileButtonStyle
with open("App/Views/BoardView.swift", "r", encoding="utf-8") as f:
    board_content = f.read()

# Replace the mismatched fill
old_fill = """                RoundedRectangle(cornerRadius: 8)
                    .fill(
                        slot?.isSolved == true
                            ? ArchivalTheme.ink.opacity(0.4)
                            : LinearGradient(
                                colors: [
                                    Color(red: 0.12, green: 0.14, blue: 0.20),
                                    Color(red: 0.07, green: 0.08, blue: 0.12)
                                ],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            )
                    )"""

new_fill = """                RoundedRectangle(cornerRadius: 8)
                    .fill(
                        slot?.isSolved == true
                            ? AnyShapeStyle(ArchivalTheme.ink.opacity(0.4))
                            : AnyShapeStyle(
                                LinearGradient(
                                    colors: [
                                        Color(red: 0.12, green: 0.14, blue: 0.20),
                                        Color(red: 0.07, green: 0.08, blue: 0.12)
                                    ],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            )
                    )"""

if old_fill in board_content:
    board_content = board_content.replace(old_fill, new_fill)
    print("Fixed ShapeStyle fill in BoardView.swift")
else:
    print("Warning: old_fill not found exactly in BoardView.swift")

# Remove duplicate ClueTileButtonStyle in BoardView.swift if present
if "private struct ClueTileButtonStyle" in board_content:
    board_content = board_content.replace("""private struct ClueTileButtonStyle: ButtonStyle {
    func makeBody(configuration: Configuration) -> some View {
        configuration.label
            .scaleEffect(configuration.isPressed ? 0.96 : 1.0)
            .brightness(configuration.isPressed ? 0.12 : 0.0)
            .animation(.easeOut(duration: 0.12), value: configuration.isPressed)
    }
}""", "")
    print("Removed duplicate ClueTileButtonStyle from BoardView.swift")

with open("App/Views/BoardView.swift", "w", encoding="utf-8") as f:
    f.write(board_content)

# 3. Update ClueActiveView.swift: Fix ForEach range ambiguity
with open("App/Views/ClueActiveView.swift", "r", encoding="utf-8") as f:
    clue_content = f.read()

# Replace any ambiguous ForEach
target_lines = [
    "ForEach(Array(0..<min(4, clue.options.count)), id: \\.self) { optIdx in",
    "ForEach(0..<min(4, clue.options.count), id: \\.self) { optIdx in"
]
for target in target_lines:
    if target in clue_content:
        clue_content = clue_content.replace(target, "ForEach(Array(clue.options.indices.prefix(4)), id: \\.self) { optIdx in")
        print(f"Replaced {target} in ClueActiveView.swift")

with open("App/Views/ClueActiveView.swift", "w", encoding="utf-8") as f:
    f.write(clue_content)

print("Fix script completed.")
