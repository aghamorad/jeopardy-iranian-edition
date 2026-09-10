import SwiftUI
import JeopardyGameEngine

public struct OpeningView: View {
    @Binding private var selectedLanguage: GameLanguage
    private let onContinue: (GameLanguage) -> Void

    public init(selectedLanguage: Binding<GameLanguage>, onContinue: @escaping (GameLanguage) -> Void) {
        self._selectedLanguage = selectedLanguage
        self.onContinue = onContinue
    }

    public var body: some View {
        ZStack {
            Color.black
            if let art = StageAssets.image("splash_reference") {
                Image(platformImage: art).resizable().scaledToFit()
            }
            VStack(spacing: 10) {
                Spacer()
                Text("SELECT LANGUAGE  /  زبان را انتخاب کنید")
                    .font(.system(size: 11, weight: .bold))
                    .tracking(2.6)
                    .foregroundColor(.white.opacity(0.76))
                HStack(spacing: 12) {
                    languageButton("ENGLISH", language: .english)
                    languageButton("فارسی  ·  UNDER CONSTRUCTION", language: .persian)
                }
                .frame(width: 520)
            }
            .padding(.bottom, 38)
        }
        .frame(minWidth: 1100, minHeight: 620)
        #if os(iOS)
        // The splash art says "press any key". There is no key, so anywhere on
        // the screen stands in for one; the language buttons still win their own
        // taps and pick a language explicitly.
        .onTapGesture { onContinue(selectedLanguage) }
        #endif
        .onAppear {
            TheatreDirector.shared.startMenuMusic()
        }
    }

    private func languageButton(_ title: String, language: GameLanguage) -> some View {
        let selected = selectedLanguage == language
        return Button {
            selectedLanguage = language
            onContinue(language)
        } label: {
            Text(title)
                .font(.system(size: language == .persian ? 13 : 12, weight: .semibold))
                .tracking(language == .persian ? 0.5 : 2.6)
                .foregroundColor(.white)
                .frame(maxWidth: .infinity)
                .frame(height: 48)
                .background(Color.black.opacity(selected ? 0.84 : 0.66))
                .overlay(
                    RoundedRectangle(cornerRadius: 5)
                        .stroke(
                            selected
                                ? LinearGradient(colors: [.green, .white, .red], startPoint: .leading, endPoint: .trailing)
                                : LinearGradient(colors: [.white.opacity(0.48), .white.opacity(0.18)], startPoint: .top, endPoint: .bottom),
                            lineWidth: selected ? 1.8 : 1
                        )
                )
        }
        .buttonStyle(.plain)
    }
}
