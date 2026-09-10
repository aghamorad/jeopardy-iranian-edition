import Foundation
import GameController

public enum ControllerAction {
    case primary(playerIndex: Int)
    case move(column: Int, row: Int)
    case buzz(playerIndex: Int)
    case selectOption(playerIndex: Int, optionIndex: Int)
}

public enum ControllerFamily: String, Codable {
    case playStation
    case xbox
    case generic
}

public enum ControllerFace: String, CaseIterable {
    case bottom, right, left, top
}

public struct ControllerGlyphs: Equatable {
    public let top: String
    public let left: String
    public let right: String
    public let bottom: String
    public let buzz: String
}

public final class ControllerManager: ObservableObject {
    public static let shared = ControllerManager()

    @Published public private(set) var connectedControllers: [GCController] = []
    @Published public private(set) var assignedPlayers: [Int: GCController] = [:] // PlayerIndex -> Controller

    public var onAction: ((ControllerAction) -> Void)?
    public var requiresOptionHold: (() -> Bool)?
    private var holdWork: [String: DispatchWorkItem] = [:]

    private init() {
        setupGameControllerNotifications()
        refreshControllers()
    }

    private func setupGameControllerNotifications() {
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleControllerConnected),
            name: .GCControllerDidConnect,
            object: nil
        )
        NotificationCenter.default.addObserver(
            self,
            selector: #selector(handleControllerDisconnected),
            name: .GCControllerDidDisconnect,
            object: nil
        )
    }

    @objc private func handleControllerConnected(notification: Notification) {
        refreshControllers()
    }

    @objc private func handleControllerDisconnected(notification: Notification) {
        if let disconnected = notification.object as? GCController {
            assignedPlayers = assignedPlayers.filter { $0.value !== disconnected }
        }
        refreshControllers()
    }

    public func refreshControllers() {
        connectedControllers = GCController.controllers()
        for (index, controller) in connectedControllers.prefix(6).enumerated() {
            assignedPlayers[index] = controller
            setupControllerInput(controller: controller, playerIndex: index)
        }
    }

    public func assign(playerIndex: Int, controller: GCController) {
        assignedPlayers[playerIndex] = controller
        setupControllerInput(controller: controller, playerIndex: playerIndex)
    }

    private func setupControllerInput(controller: GCController, playerIndex: Int) {
        guard let gamepad = controller.extendedGamepad else { return }

        gamepad.dpad.up.pressedChangedHandler = { [weak self] _, _, pressed in if pressed { self?.onAction?(.move(column: 0, row: -1)) } }
        gamepad.dpad.down.pressedChangedHandler = { [weak self] _, _, pressed in if pressed { self?.onAction?(.move(column: 0, row: 1)) } }
        gamepad.dpad.left.pressedChangedHandler = { [weak self] _, _, pressed in if pressed { self?.onAction?(.move(column: -1, row: 0)) } }
        gamepad.dpad.right.pressedChangedHandler = { [weak self] _, _, pressed in if pressed { self?.onAction?(.move(column: 1, row: 0)) } }
        // The physical bottom face button is × on PlayStation and A on Xbox.
        // It selects/continues on the board and acts as the main buzzer.
        gamepad.buttonA.pressedChangedHandler = { [weak self] _, _, pressed in
            self?.handleFaceButton(controller: controller, playerIndex: playerIndex, face: .bottom, pressed: pressed)
        }

        gamepad.buttonB.pressedChangedHandler = { [weak self] _, _, pressed in
            self?.handleFaceButton(controller: controller, playerIndex: playerIndex, face: .right, pressed: pressed)
        }

        gamepad.buttonX.pressedChangedHandler = { [weak self] _, _, pressed in
            self?.handleFaceButton(controller: controller, playerIndex: playerIndex, face: .left, pressed: pressed)
        }

        gamepad.buttonY.pressedChangedHandler = { [weak self] _, _, pressed in
            self?.handleFaceButton(controller: controller, playerIndex: playerIndex, face: .top, pressed: pressed)
        }

        gamepad.rightTrigger.pressedChangedHandler = { [weak self] _, _, pressed in
            if pressed {
                self?.onAction?(.buzz(playerIndex: playerIndex))
            }
        }
    }

    private func handleFaceButton(controller: GCController, playerIndex: Int, face: ControllerFace, pressed: Bool) {
        DispatchQueue.main.async { [weak self] in
            guard let self else { return }
            let key = "\(ObjectIdentifier(controller).hashValue)-\(face.rawValue)"
            if !pressed {
                self.holdWork[key]?.cancel()
                self.holdWork.removeValue(forKey: key)
                return
            }

            if self.requiresOptionHold?() == true {
                let item = DispatchWorkItem { [weak self] in
                    self?.holdWork.removeValue(forKey: key)
                    self?.onAction?(.selectOption(playerIndex: playerIndex, optionIndex: Self.optionIndex(for: face)))
                }
                self.holdWork[key]?.cancel()
                self.holdWork[key] = item
                DispatchQueue.main.asyncAfter(deadline: .now() + 0.82, execute: item)
            } else if face == .bottom {
                self.onAction?(.primary(playerIndex: playerIndex))
            }
        }
    }

    public static func optionIndex(for face: ControllerFace) -> Int {
        switch face {
        case .bottom: return 0
        case .right: return 1
        case .left: return 2
        case .top: return 3
        }
    }

    public static func family(forDeviceName name: String) -> ControllerFamily {
        let value = name.lowercased()
        if value.contains("dualsense") || value.contains("dualshock") || value.contains("playstation") || value.contains("sony") {
            return .playStation
        }
        if value.contains("xbox") || value.contains("microsoft") {
            return .xbox
        }
        return .generic
    }

    public func family(forPlayerIndex playerIndex: Int) -> ControllerFamily? {
        guard let controller = assignedPlayers[playerIndex] else { return nil }
        return Self.family(forDeviceName: (controller.vendorName ?? "") + " " + controller.productCategory)
    }

    public func glyphs(forPlayerIndex playerIndex: Int) -> ControllerGlyphs? {
        guard let family = family(forPlayerIndex: playerIndex) else { return nil }
        switch family {
        case .playStation:
            return ControllerGlyphs(top: "△", left: "□", right: "○", bottom: "×", buzz: "×")
        case .xbox:
            return ControllerGlyphs(top: "Y", left: "X", right: "B", bottom: "A", buzz: "A")
        case .generic:
            return ControllerGlyphs(top: "Y", left: "X", right: "B", bottom: "A", buzz: "A")
        }
    }

    public func deviceName(forPlayerIndex playerIndex: Int) -> String? {
        guard let controller = assignedPlayers[playerIndex] else { return nil }
        return controller.vendorName ?? controller.productCategory
    }

    /// Keyboard mapping fallback for seamless local testing without gamepads
    public func handleKeyboardInput(key: String) {
        switch key.lowercased() {
        // Player 1: Space to buzz, 1-4 for MC
        case " ": onAction?(.buzz(playerIndex: 0))
        case "1": onAction?(.selectOption(playerIndex: 0, optionIndex: 0))
        case "2": onAction?(.selectOption(playerIndex: 0, optionIndex: 1))
        case "3": onAction?(.selectOption(playerIndex: 0, optionIndex: 2))
        case "4": onAction?(.selectOption(playerIndex: 0, optionIndex: 3))

        // Player 2: Enter to buzz, 7-0 for MC
        case "\r", "\n": onAction?(.buzz(playerIndex: 1))
        case "7": onAction?(.selectOption(playerIndex: 1, optionIndex: 0))
        case "8": onAction?(.selectOption(playerIndex: 1, optionIndex: 1))
        case "9": onAction?(.selectOption(playerIndex: 1, optionIndex: 2))
        case "0": onAction?(.selectOption(playerIndex: 1, optionIndex: 3))

        // Player 3: Tab or 'z' to buzz, Q/W/E/R for MC
        case "z", "\t": onAction?(.buzz(playerIndex: 2))
        case "q": onAction?(.selectOption(playerIndex: 2, optionIndex: 0))
        case "w": onAction?(.selectOption(playerIndex: 2, optionIndex: 1))
        case "e": onAction?(.selectOption(playerIndex: 2, optionIndex: 2))
        case "r": onAction?(.selectOption(playerIndex: 2, optionIndex: 3))

        // Player 4: 'm' or '\\' to buzz, U/I/O/P for MC
        case "m", "\\": onAction?(.buzz(playerIndex: 3))
        case "u": onAction?(.selectOption(playerIndex: 3, optionIndex: 0))
        case "i": onAction?(.selectOption(playerIndex: 3, optionIndex: 1))
        case "o": onAction?(.selectOption(playerIndex: 3, optionIndex: 2))
        case "p": onAction?(.selectOption(playerIndex: 3, optionIndex: 3))

        default:
            break
        }
    }
}
