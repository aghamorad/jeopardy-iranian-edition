import Foundation
import PDFKit
import Vision

// Native Apple Vision OCR Tool for Scanned Source Books
// Runs 100% offline on macOS Apple Neural Engine / GPU

guard CommandLine.arguments.count >= 2 else {
    print("Usage: swift Tools/run_ocr.swift <path_to_pdf> [output_dir] [max_pages]")
    exit(1)
}

let pdfPath = CommandLine.arguments[1]
let pdfURL = URL(fileURLWithPath: pdfPath)
let outputDir = CommandLine.arguments.count >= 3 ? CommandLine.arguments[2] : "/tmp/ocr_output"
let maxPages = CommandLine.arguments.count >= 4 ? Int(CommandLine.arguments[3]) ?? 9999 : 9999

guard let doc = PDFDocument(url: pdfURL) else {
    print("Error: Could not open PDF at \(pdfPath)")
    exit(1)
}

let fileManager = FileManager.default
try? fileManager.createDirectory(atPath: outputDir, withIntermediateDirectories: true)

print("Starting native Vision OCR on: \(pdfURL.lastPathComponent)")
print("Total pages in PDF: \(doc.pageCount) | Processing up to: \(min(doc.pageCount, maxPages)) pages")

struct OCRPageResult: Codable {
    let pageIndex: Int
    let text: String
}

var results: [OCRPageResult] = []
let request = VNRecognizeTextRequest()
request.recognitionLevel = .accurate
request.usesLanguageCorrection = true

for i in 0..<min(doc.pageCount, maxPages) {
    guard let page = doc.page(at: i) else { continue }
    let pageBounds = page.bounds(for: .mediaBox)
    let renderer = ImageRenderer(bounds: pageBounds)
    guard let image = page.thumbnail(of: CGSize(width: pageBounds.width * 2, height: pageBounds.height * 2), for: .mediaBox).cgImage(forProposedRect: nil, context: nil, hints: nil) else {
        continue
    }
    
    let handler = VNImageRequestHandler(cgImage: image, options: [:])
    try? handler.perform([request])
    
    let recognizedStrings = request.results?.compactMap { observation in
        observation.topCandidates(1).first?.string
    } ?? []
    
    let fullText = recognizedStrings.joined(separator: "\n")
    results.append(OCRPageResult(pageIndex: i + 1, text: fullText))
    if (i + 1) % 10 == 0 || i == 0 {
        print("Processed page \(i + 1)/\(min(doc.pageCount, maxPages))")
    }
}

let baseName = (pdfURL.lastPathComponent as NSString).deletingPathExtension
let jsonURL = URL(fileURLWithPath: outputDir).appendingPathComponent("\(baseName)_ocr.json")
let encoder = JSONEncoder()
encoder.outputFormatting = .prettyPrinted
if let data = try? encoder.encode(results) {
    try? data.write(to: jsonURL)
    print("OCR Complete! Saved \(results.count) pages to \(jsonURL.path)")
}
