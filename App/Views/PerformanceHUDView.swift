import SwiftUI
import JeopardyGameEngine

public struct PerformanceHUDView: View {
    @ObservedObject var monitor: PerformanceMonitor

    public init(monitor: PerformanceMonitor = .shared) {
        self.monitor = monitor
    }

    public var body: some View {
        HStack(spacing: 16) {
            HStack(spacing: 4) {
                Image(systemName: "bolt.fill")
                    .foregroundColor(ArchivalTheme.bronzeAccent)
                Text("BUZZ: \(monitor.lastBuzzLatencyMicros) μs")
                    .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
            }

            HStack(spacing: 4) {
                Image(systemName: "waveform")
                    .foregroundColor(Color.blue)
                Text("ASR: \(String(format: "%.1f", monitor.lastASRLatencyMs)) ms")
                    .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
            }

            HStack(spacing: 4) {
                Image(systemName: "checkmark.shield")
                    .foregroundColor(Color.green)
                Text("RESOLVER: \(String(format: "%.2f", monitor.lastResolverLatencyMs)) ms")
                    .font(ArchivalTheme.sansFont(size: 11, weight: .bold))
            }
        }
        .foregroundColor(ArchivalTheme.textParchment)
        .padding(.horizontal, 12)
        .padding(.vertical, 4)
        .background(Color.black.opacity(0.8))
        .cornerRadius(6)
        .overlay(RoundedRectangle(cornerRadius: 6).stroke(ArchivalTheme.cardBorder, lineWidth: 1))
    }
}
