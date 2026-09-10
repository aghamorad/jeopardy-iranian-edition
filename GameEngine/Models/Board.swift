import Foundation

public struct BoardSlot: Identifiable, Hashable, Codable {
    public let id: String
    public let category: String
    public let categoryIndex: Int
    public let valueIndex: Int
    public let value: Int
    public let clue: Clue
    public var isSolved: Bool
    public let isSpecialWager: Bool

    public init(category: String, categoryIndex: Int, valueIndex: Int, value: Int, clue: Clue, isSolved: Bool = false, isSpecialWager: Bool = false) {
        self.id = "\(categoryIndex)_\(valueIndex)"
        self.category = category
        self.categoryIndex = categoryIndex
        self.valueIndex = valueIndex
        self.value = value
        self.clue = clue
        self.isSolved = isSolved
        self.isSpecialWager = isSpecialWager
    }
}

public struct GameBoard: Codable {
    public let categories: [String]
    public var slots: [BoardSlot]

    public init(categories: [String], slots: [BoardSlot]) {
        self.categories = categories
        self.slots = slots
    }

    public func slot(at categoryIndex: Int, valueIndex: Int) -> BoardSlot? {
        slots.first { $0.categoryIndex == categoryIndex && $0.valueIndex == valueIndex }
    }

    public mutating func markSolved(slotId: String) {
        if let idx = slots.firstIndex(where: { $0.id == slotId }) {
            slots[idx].isSolved = true
        }
    }

    public var isComplete: Bool {
        slots.allSatisfy { $0.isSolved }
    }
}
