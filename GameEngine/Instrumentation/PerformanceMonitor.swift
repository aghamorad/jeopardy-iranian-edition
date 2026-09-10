import Foundation

public struct PerformanceMetric: Identifiable {
    public let id = UUID()
    public let name: String
    public let durationMs: Double
    public let timestamp: Date

    public init(name: String, durationMs: Double) {
        self.name = name
        self.durationMs = durationMs
        self.timestamp = Date()
    }
}

public final class PerformanceMonitor: ObservableObject {
    public static let shared = PerformanceMonitor()

    @Published public private(set) var recentMetrics: [PerformanceMetric] = []
    @Published public private(set) var lastBuzzLatencyMicros: Int64 = 0
    @Published public private(set) var lastASRLatencyMs: Double = 0.0
    @Published public private(set) var lastResolverLatencyMs: Double = 0.0

    private init() {}

    public func record(name: String, durationMs: Double) {
        DispatchQueue.main.async {
            let metric = PerformanceMetric(name: name, durationMs: durationMs)
            self.recentMetrics.append(metric)
            if self.recentMetrics.count > 30 {
                self.recentMetrics.removeFirst()
            }
            if name == "AnswerResolver" {
                self.lastResolverLatencyMs = durationMs
            } else if name == "ASR" {
                self.lastASRLatencyMs = durationMs
            }
        }
    }

    public func recordBuzzLatency(micros: Int64) {
        DispatchQueue.main.async {
            self.lastBuzzLatencyMicros = micros
            self.record(name: "BuzzResolution", durationMs: Double(micros) / 1000.0)
        }
    }
}
