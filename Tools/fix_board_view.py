#!/usr/bin/env python3

with open("App/Views/BoardView.swift", "r", encoding="utf-8") as f:
    content = f.read()

# 1. Fix gameState.returnToLobby()
content = content.replace("gameState.returnToLobby()", "gameState.phase = .lobby")

# 2. Fix ForEach type inference
content = content.replace("ForEach(0..<6, id: \\.self) { colIndex in", "ForEach(Array(0..<6), id: \\.self) { (colIndex: Int) in")
content = content.replace("ForEach(0..<5, id: \\.self) { rowIndex in", "ForEach(Array(0..<5), id: \\.self) { (rowIndex: Int) in")

# 3. Fix AnyShapeStyle stroke
old_stroke = """                RoundedRectangle(cornerRadius: 8)
                    .stroke(
                        slot?.isSolved == true
                            ? ArchivalTheme.cardBorder.opacity(0.2)
                            : LinearGradient(
                                colors: [
                                    ArchivalTheme.gold24k.opacity(0.55),
                                    ArchivalTheme.gold24k.opacity(0.15)
                                ],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            ),
                        lineWidth: 1.2
                    )"""

new_stroke = """                RoundedRectangle(cornerRadius: 8)
                    .stroke(
                        slot?.isSolved == true
                            ? AnyShapeStyle(ArchivalTheme.cardBorder.opacity(0.2))
                            : AnyShapeStyle(
                                LinearGradient(
                                    colors: [
                                        ArchivalTheme.gold24k.opacity(0.55),
                                        ArchivalTheme.gold24k.opacity(0.15)
                                    ],
                                    startPoint: .topLeading,
                                    endPoint: .bottomTrailing
                                )
                            ),
                        lineWidth: 1.2
                    )"""

content = content.replace(old_stroke, new_stroke)

with open("App/Views/BoardView.swift", "w", encoding="utf-8") as f:
    f.write(content)

print("BoardView.swift updated successfully.")
