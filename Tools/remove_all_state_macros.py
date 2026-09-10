#!/usr/bin/env python3
import sys

# 1. BoardView.swift
with open("App/Views/BoardView.swift", "r", encoding="utf-8") as f:
    b = f.read()

b = b.replace("    @State private var selectedStageTheme: GameStageTheme = ArchivalTheme.currentTheme\n", "")
b = b.replace("Picker(\"Theme\", selection: $selectedStageTheme)", "Picker(\"Theme\", selection: Binding(get: { ArchivalTheme.currentTheme }, set: { ArchivalTheme.currentTheme = $0 }))")
b = b.replace("""                .onChange(of: selectedStageTheme) { newTheme in
                    ArchivalTheme.currentTheme = newTheme
                }""", "")

with open("App/Views/BoardView.swift", "w", encoding="utf-8") as f:
    f.write(b)
print("Updated BoardView.swift")

# 2. LobbyView.swift
with open("App/Views/LobbyView.swift", "r", encoding="utf-8") as f:
    l = f.read()

l = l.replace("    @State private var stageTheme: GameStageTheme = ArchivalTheme.currentTheme\n", "")
l = l.replace("Picker(\"Theme\", selection: $stageTheme)", "Picker(\"Theme\", selection: Binding(get: { ArchivalTheme.currentTheme }, set: { ArchivalTheme.currentTheme = $0 }))")
l = l.replace("""                .onChange(of: stageTheme) { newTheme in
                    ArchivalTheme.currentTheme = newTheme
                }""", "")

with open("App/Views/LobbyView.swift", "w", encoding="utf-8") as f:
    f.write(l)
print("Updated LobbyView.swift")

# 3. ClueActiveView.swift
with open("App/Views/ClueActiveView.swift", "r", encoding="utf-8") as f:
    c = f.read()

c = c.replace("    @State private var timerPulse: Bool = false\n", "")

with open("App/Views/ClueActiveView.swift", "w", encoding="utf-8") as f:
    f.write(c)
print("Updated ClueActiveView.swift")
