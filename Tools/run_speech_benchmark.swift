import Foundation
import JeopardyGameEngine

// 50-Item Persian & English Historical ASR Benchmark Suite
struct SpeechBenchmarkItem {
    let id: String
    let spokenText: String
    let targetCanonicalEntity: String
    let categoryContext: [String]
    let clueId: String
    let speechStyle: String
}

let benchmarkCorpus: [SpeechBenchmarkItem] = [
    // 1-10: Core Historical Leaders & Prime Ministers (Short & Formal)
    SpeechBenchmarkItem(id: "bm_01", spokenText: "محمد مصدق", targetCanonicalEntity: "Mohammad Mosaddegh", categoryContext: ["مصدق", "فاطمی", "نفت", "کودتا"], clueId: "oil_mosaddegh_200", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_02", spokenText: "دکتر مصدق", targetCanonicalEntity: "Mohammad Mosaddegh", categoryContext: ["مصدق", "نفت"], clueId: "oil_mosaddegh_200", speechStyle: "conversational"),
    SpeechBenchmarkItem(id: "bm_03", spokenText: "مصدق", targetCanonicalEntity: "Mohammad Mosaddegh", categoryContext: ["مصدق"], clueId: "oil_mosaddegh_200", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_04", spokenText: "میرزا تقی خان امیرکبیر", targetCanonicalEntity: "Amir Kabir", categoryContext: ["امیرکبیر", "دارالفنون", "قاجار"], clueId: "qajar_amir_kabir_200", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_05", spokenText: "امیرکبیر", targetCanonicalEntity: "Amir Kabir", categoryContext: ["امیرکبیر"], clueId: "qajar_amir_kabir_200", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_06", spokenText: "میرزا تقی خان", targetCanonicalEntity: "Amir Kabir", categoryContext: ["امیرکبیر"], clueId: "qajar_amir_kabir_200", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_07", spokenText: "امیرعباس هویدا", targetCanonicalEntity: "Amir Abbas Hoveyda", categoryContext: ["هویدا", "نخست وزیر", "پهلوی"], clueId: "court_hoveyda_600", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_08", spokenText: "هویدا", targetCanonicalEntity: "Amir Abbas Hoveyda", categoryContext: ["هویدا"], clueId: "court_hoveyda_600", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_09", spokenText: "حسین فاطمی", targetCanonicalEntity: "Hossein Fatemi", categoryContext: ["فاطمی", "باختر امروز"], clueId: "oil_fatemi_800", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_10", spokenText: "دکتر فاطمی", targetCanonicalEntity: "Hossein Fatemi", categoryContext: ["فاطمی"], clueId: "oil_fatemi_800", speechStyle: "conversational"),

    // 11-20: Qajar Kings, Intellectuals & Constitutional Revolution
    SpeechBenchmarkItem(id: "bm_11", spokenText: "ناصرالدین شاه", targetCanonicalEntity: "Nasir al-Din Shah Qajar", categoryContext: ["ناصرالدین شاه", "عکاسی", "قاجار"], clueId: "qajar_nasir_al_din_shah_600", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_12", spokenText: "ناصرالدین شاه قاجار", targetCanonicalEntity: "Nasir al-Din Shah Qajar", categoryContext: ["ناصرالدین شاه"], clueId: "qajar_nasir_al_din_shah_600", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_13", spokenText: "میرزا ملکم خان", targetCanonicalEntity: "Mirza Malkom Khan", categoryContext: ["ملکم خان", "فراموشخانه", "قانون"], clueId: "qajar_malkom_khan_1000", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_14", spokenText: "ملکم خان", targetCanonicalEntity: "Mirza Malkom Khan", categoryContext: ["ملکم خان"], clueId: "qajar_malkom_khan_1000", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_15", spokenText: "ستارخان", targetCanonicalEntity: "Sattar Khan", categoryContext: ["ستارخان", "مشروطه", "تبریز"], clueId: "mashruteh_sattar_khan_200", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_16", spokenText: "ستار خان سردار ملی", targetCanonicalEntity: "Sattar Khan", categoryContext: ["ستارخان", "سردار ملی"], clueId: "mashruteh_sattar_khan_200", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_17", spokenText: "شیخ فضل‌الله نوری", targetCanonicalEntity: "Sheikh Fazlollah Nuri", categoryContext: ["مشروعه", "فضل‌الله نوری"], clueId: "mashruteh_sheikh_fazlollah_600", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_18", spokenText: "شیخ فضل الله", targetCanonicalEntity: "Sheikh Fazlollah Nuri", categoryContext: ["فضل الله نوری"], clueId: "mashruteh_sheikh_fazlollah_600", speechStyle: "conversational"),
    SpeechBenchmarkItem(id: "bm_19", spokenText: "کلنل لیاخوف", targetCanonicalEntity: "Vladimir Liakhov", categoryContext: ["لیاخوف", "قزاق", "بهارستان"], clueId: "mashruteh_liakhov_800", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_20", spokenText: "صور اسرافیل", targetCanonicalEntity: "Sur-e Esrafil", categoryContext: ["صور اسرافیل", "دهخدا"], clueId: "mashruteh_sur_e_esrafil_1000", speechStyle: "short"),

    // 21-30: Treaties, Diplomacy, Places & Thematic Concepts
    SpeechBenchmarkItem(id: "bm_21", spokenText: "عهدنامه ترکمنچای", targetCanonicalEntity: "Treaty of Turkmenchay", categoryContext: ["ترکمنچای", "عباس میرزا", "قاجار"], clueId: "qajar_turkmenchay_400", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_22", spokenText: "ترکمنچای", targetCanonicalEntity: "Treaty of Turkmenchay", categoryContext: ["ترکمنچای"], clueId: "qajar_turkmenchay_400", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_23", spokenText: "نهضت تنباکو", targetCanonicalEntity: "Tobacco", categoryContext: ["تنباکو", "شیرازی"], clueId: "qajar_tobacco_protest_800", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_24", spokenText: "توتون و تنباکو", targetCanonicalEntity: "Tobacco", categoryContext: ["تنباکو"], clueId: "qajar_tobacco_protest_800", speechStyle: "conversational"),
    SpeechBenchmarkItem(id: "bm_25", spokenText: "سفارت انگلیس", targetCanonicalEntity: "The British Legation", categoryContext: ["سفارت انگلیس", "بست"], clueId: "mashruteh_british_bast_400", speechStyle: "conversational"),
    SpeechBenchmarkItem(id: "bm_26", spokenText: "سفارت بریتانیا", targetCanonicalEntity: "The British Legation", categoryContext: ["سفارت انگلیس"], clueId: "mashruteh_british_bast_400", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_27", spokenText: "کرمیت روزولت", targetCanonicalEntity: "Kermit Roosevelt Jr.", categoryContext: ["روزولت", "کودتا", "سیا"], clueId: "oil_kermit_roosevelt_400", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_28", spokenText: "عملیات چکمه", targetCanonicalEntity: "Operation Boot", categoryContext: ["چکمه", "ام آی سیکس"], clueId: "oil_operation_boot_600", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_29", spokenText: "چهل درصد", targetCanonicalEntity: "40%", categoryContext: ["کنسرسیوم", "درصد"], clueId: "oil_consortium_1000", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_30", spokenText: "جشن‌های ۲۵۰۰ ساله شاهنشاهی", targetCanonicalEntity: "The 2,500-Year Celebration of the Persian Empire", categoryContext: ["تخت جمشید", "۲۵۰۰ ساله"], clueId: "court_persepolis_200", speechStyle: "formal"),

    // 31-40: Religion, Cultural Life, Cinema & Media
    SpeechBenchmarkItem(id: "bm_31", spokenText: "ولایت فقیه", targetCanonicalEntity: "Velayat-e Faqih", categoryContext: ["ولایت فقیه", "حکومت اسلامی"], clueId: "theology_velayat_e_faqih_200", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_32", spokenText: "حکومت اسلامی ولایت فقیه", targetCanonicalEntity: "Velayat-e Faqih", categoryContext: ["ولایت فقیه"], clueId: "theology_velayat_e_faqih_200", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_33", spokenText: "ایالات متحده آمریکا", targetCanonicalEntity: "The United States", categoryContext: ["آمریکا", "کاپیتولاسیون"], clueId: "theology_capitulations_speech_400", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_34", spokenText: "آمریکا", targetCanonicalEntity: "The United States", categoryContext: ["آمریکا"], clueId: "theology_capitulations_speech_400", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_35", spokenText: "نجف اشرف", targetCanonicalEntity: "Najaf", categoryContext: ["نجف", "عراق", "تبعید"], clueId: "theology_najaf_600", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_36", spokenText: "نجف", targetCanonicalEntity: "Najaf", categoryContext: ["نجف"], clueId: "theology_najaf_600", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_37", spokenText: "طاغوت", targetCanonicalEntity: "Taghut", categoryContext: ["طاغوت", "قرآن"], clueId: "theology_taghut_800", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_38", spokenText: "مدرسه فیضیه قم", targetCanonicalEntity: "Fayziyeh Madrasa", categoryContext: ["فیضیه", "قم"], clueId: "theology_fayziyeh_1000", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_39", spokenText: "فیضیه", targetCanonicalEntity: "Fayziyeh Madrasa", categoryContext: ["فیضیه"], clueId: "theology_fayziyeh_1000", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_40", spokenText: "میرزا ابراهیم خان عکاس‌باشی", targetCanonicalEntity: "Mirza Ebrahim Khan Akkas-bashi", categoryContext: ["عکاس‌باشی", "سینما"], clueId: "cinema_akkas_bashi_200", speechStyle: "formal"),

    // 41-50: Cinema, Soundscapes & English Utterances
    SpeechBenchmarkItem(id: "bm_41", spokenText: "عکاس‌باشی", targetCanonicalEntity: "Mirza Ebrahim Khan Akkas-bashi", categoryContext: ["عکاس‌باشی"], clueId: "cinema_akkas_bashi_200", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_42", spokenText: "دختر لر", targetCanonicalEntity: "The Lor Girl (Dokhtar-e Lor)", categoryContext: ["دختر لر", "سپنتا"], clueId: "cinema_lor_girl_400", speechStyle: "short"),
    SpeechBenchmarkItem(id: "bm_43", spokenText: "روح‌انگیز سامی‌نژاد", targetCanonicalEntity: "Roohangiz Saminejad", categoryContext: ["سامی‌نژاد", "گلنار"], clueId: "cinema_saminejad_600", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_44", spokenText: "اوانس اوگانیانس", targetCanonicalEntity: "Ovanes Ohanian", categoryContext: ["اوگانیانس", "آبی و رابی"], clueId: "cinema_ohanian_800", speechStyle: "formal"),
    SpeechBenchmarkItem(id: "bm_45", spokenText: "گراند سینما در لاله زار", targetCanonicalEntity: "Grand Cinema", categoryContext: ["گراند سینما", "لاله‌زار"], clueId: "cinema_grand_cinema_1000", speechStyle: "conversational"),
    SpeechBenchmarkItem(id: "bm_46", spokenText: "Mohammad Mossadegh", targetCanonicalEntity: "Mohammad Mosaddegh", categoryContext: ["Mossadegh", "Nationalization"], clueId: "oil_mosaddegh_200", speechStyle: "english"),
    SpeechBenchmarkItem(id: "bm_47", spokenText: "Amir Kabir", targetCanonicalEntity: "Amir Kabir", categoryContext: ["Amir Kabir", "Dar al-Fonun"], clueId: "qajar_amir_kabir_200", speechStyle: "english"),
    SpeechBenchmarkItem(id: "bm_48", spokenText: "Sattar Khan", targetCanonicalEntity: "Sattar Khan", categoryContext: ["Sattar Khan", "Tabriz"], clueId: "mashruteh_sattar_khan_200", speechStyle: "english"),
    SpeechBenchmarkItem(id: "bm_49", spokenText: "Sheikh Fazlollah Nuri", targetCanonicalEntity: "Sheikh Fazlollah Nuri", categoryContext: ["Fazlollah", "Constitution"], clueId: "mashruteh_sheikh_fazlollah_600", speechStyle: "english"),
    SpeechBenchmarkItem(id: "bm_50", spokenText: "Velayat-e Faqih", targetCanonicalEntity: "Velayat-e Faqih", categoryContext: ["Velayat-e Faqih", "Islamic Government"], clueId: "theology_velayat_e_faqih_200", speechStyle: "english")
]

let qBank = QuestionBank.shared
let resolver = AnswerResolver.shared

var rawExactMatches = 0
var entityResolvedMatches = 0
var latencies: [Double] = []

for item in benchmarkCorpus {
    guard let clue = qBank.allClues.first(where: { $0.id == item.clueId }) else {
        continue
    }

    let start = mach_absolute_time()
    let res = resolver.resolve(utterance: item.spokenText, clue: clue)
    var info = mach_timebase_info()
    mach_timebase_info(&info)
    let elapsed = Double((mach_absolute_time() - start) * UInt64(info.numer) / UInt64(info.denom)) / 1_000_000.0

    latencies.append(elapsed)

    let normInput = PersianNormalizer.normalize(item.spokenText, stripDisposableHonorifics: true)
    let normCanonical = PersianNormalizer.normalize(clue.canonicalAnswer, stripDisposableHonorifics: true)
    if normInput == normCanonical {
        rawExactMatches += 1
    }

    if res.result == .correct {
        entityResolvedMatches += 1
    } else {
        print("  Failed item [\(item.id)] spoken: '\(item.spokenText)' -> Result: \(res.result) (method: \(res.resolutionMethod))")
    }
}

latencies.sort()
let median = latencies[latencies.count / 2]
let p90 = latencies[Int(Double(latencies.count) * 0.90)]
let p95 = latencies[Int(Double(latencies.count) * 0.95)]
let worst = latencies.last ?? 0.0

print("\n=======================================================")
print("SPEECH BENCHMARK RESULTS (50 ITEMS)")
print("=======================================================")
print("Total Utterances:                    50")
print("Raw Exact Canonical Matches:         \(rawExactMatches)/50 (\(Double(rawExactMatches)*2.0)%)")
print("Final Entity Resolution Accuracy:    \(entityResolvedMatches)/50 (\(Double(entityResolvedMatches)*2.0)%)")
print("\nAnswerResolver Perceived Latency Metrics:")
print("  Median: \(String(format: "%.3f", median)) ms")
print("  P90:    \(String(format: "%.3f", p90)) ms")
print("  P95:    \(String(format: "%.3f", p95)) ms")
print("  Worst:  \(String(format: "%.3f", worst)) ms")
print("=======================================================\n")
