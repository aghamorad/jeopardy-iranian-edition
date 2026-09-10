import Foundation

public enum InputSource: String, Codable { case gamepad, keyboard, mouse, trackpad, bot }
public enum ContestantAction: String, Codable { case join, buzz, select, submit, cancel, navigate, wager }
public struct ContestantInputEvent: Codable, Hashable {
    public let playerID: UUID
    public let inputSource: InputSource
    public let action: ContestantAction
    public let timestamp: TimeInterval
    public let deviceID: String
    public let metadata: [String: String]
    public init(playerID: UUID, inputSource: InputSource, action: ContestantAction, timestamp: TimeInterval = ProcessInfo.processInfo.systemUptime, deviceID: String = "", metadata: [String: String] = [:]) { self.playerID = playerID; self.inputSource = inputSource; self.action = action; self.timestamp = timestamp; self.deviceID = deviceID; self.metadata = metadata }
}

public actor ContestantInputRouter {
    public static let shared = ContestantInputRouter()
    private var handlers: [UUID: (ContestantInputEvent) -> Void] = [:]
    public func register(_ playerID: UUID, handler: @escaping (ContestantInputEvent) -> Void) { handlers[playerID] = handler }
    public func unregister(_ playerID: UUID) { handlers.removeValue(forKey: playerID) }
    public func send(_ event: ContestantInputEvent) { handlers[event.playerID]?(event) }
}
