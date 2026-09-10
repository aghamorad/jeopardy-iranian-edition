import Foundation
import JeopardyGameEngine

enum PlayerCopy {
    static func text(_ english: String, _ persian: String, language: GameLanguage) -> String {
        language == .persian ? persian : english
    }
    static func category(_ name: String, language: GameLanguage) -> String {
        if language == .persian { return loadedPersianCategories[name] ?? PersianCategoryNames[name] ?? "تاریخ و فرهنگ ایران" }
        return EnglishCategoryPuns[name] ?? name
    }
    static func number(_ value: Int, language: GameLanguage) -> String {
        let raw = NumberFormatter.localizedString(from: NSNumber(value: value), number: .decimal)
        guard language == .persian else { return raw }
        return raw.map { character in
            let latin = "0123456789"
            let persian = Array("۰۱۲۳۴۵۶۷۸۹")
            if let index = latin.firstIndex(of: character) { return persian[latin.distance(from: latin.startIndex, to: index)] }
            return character == "," ? "٬" : character
        }.reduce(into: "") { $0.append($1) }
    }
    static func millions(_ value: Int, language: GameLanguage) -> String {
        let amount = number(abs(value) / 1_000_000, language: language)
        let sign = value < 0 ? "−" : ""
        return language == .persian ? "\(sign)\(amount) میلیون تومان" : "\(sign)\(amount)M تومان"
    }

    private static let loadedPersianCategories: [String: String] = {
        let urls = [
            Bundle.main.resourceURL?.appendingPathComponent("persian_categories.json"),
            Bundle.main.url(forResource: "persian_categories", withExtension: "json"),
            URL(fileURLWithPath: "/Users/Morad/Desktop/Jeopardy - Iranian Edition/App/Resources/persian_categories.json")
        ].compactMap { $0 }
        for url in urls {
            if let data = try? Data(contentsOf: url),
               let values = try? JSONDecoder().decode([String: String].self, from: data),
               !values.isEmpty { return values }
        }
        return [:]
    }()
    private static let EnglishCategoryPuns: [String: String] = [
        "MYTHS & MONSTERS OF THE SHAHNAMEH": "Rostam-atically Speaking",
        "AMIR KABIR'S REFORMS": "Amir Kabir? Amir Kidding!",
        "TRADITIONAL CRAFTS & MASTERS": "Craft Work Makes the Dream Work",
        "THE SUFI MYSTICS": "Whirling Dervishes, Spinning Facts",
        "CUISINE OF THE PROVINCES": "Persian, Actually",
        "THE IRON COSSACK": "Steel Yourself",
        "THE OIL CRISIS: 1951-1953": "Crude Awakening",
        "COLD WAR ESPIONAGE IN TEHRAN": "The Spy Who Came in from Tehran",
        "PERSIAN GULF: TANKER WAR": "Ships, Lies & Oil Slicks",
        "BAZARIS & MERCHANTS": "Market Forces",
        "MONUMENTS OF EMPIRE": "Rock Solid History",
        "IDEAS THAT SHOOK TEHRAN": "Mind Over Mashhad",
        "CLASSICAL PERSIAN MUSIC MASTERS": "A Whole Lotta Radif",
        "SHIRAZ: ROSES & NIGHTINGALES": "Stop and Smell the Shiraz",
        "TEHRAN: BAZAAR TO MEGAPOLIS": "From Bazaar to Bigger Bazaar",
        "SAVAK: THE EYE OF THE SHAH": "Big Brother Is Watching",
        "HOSTAGE CRISIS: 444 DAYS": "Held Up in History",
        "THE WHITE REVOLUTION IN DEPTH": "A Revolution in White and Black"
    ]
    private static let PersianCategoryNames: [String: String] = [
        "THE OIL CRISIS: 1951-1953": "نفت، نفت، نفت!",
        "COLD WAR ESPIONAGE IN TEHRAN": "جاسوس‌بازی در تهران",
        "PERSIAN GULF: TANKER WAR": "نفتکش‌ها روی موج بلا",
        "SHAHNAMEH & THE HEROES": "رستم و رفقا",
        "BAZARIS & MERCHANTS": "بازار، پول، دردسر",
        "MONUMENTS OF EMPIRE": "سنگ‌هایی که حرف می‌زنند",
        "IDEAS THAT SHOOK TEHRAN": "فکرهایی که تهران را لرزاندند"
    ]
}
