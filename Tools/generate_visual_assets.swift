import AppKit
import CoreGraphics
import Foundation

let resourcesDir = "App/Resources"
try? FileManager.default.createDirectory(atPath: resourcesDir, withIntermediateDirectories: true)

func savePNG(image: NSImage, filename: String) {
    guard let tiffData = image.tiffRepresentation,
          let bitmap = NSBitmapImageRep(data: tiffData),
          let pngData = bitmap.representation(using: .png, properties: [:]) else {
        print("Failed to encode PNG for \(filename)")
        return
    }
    let url = URL(fileURLWithPath: "\(resourcesDir)/\(filename)")
    do {
        try pngData.write(to: url)
        print("Generated \(filename) (\(Int(image.size.width))x\(Int(image.size.height)))")
    } catch {
        print("Error saving \(filename): \(error)")
    }
}

// 1. Studio Stage Backdrop (1920x1080)
func generateStudioBackdrop() {
    let width: CGFloat = 1920
    let height: CGFloat = 1080
    let image = NSImage(size: NSSize(width: width, height: height))
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { return }

    // Deep studio gradient: Midnight blue (#07090F) to Obsidian (#0F131D)
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let bgColors = [
        CGColor(red: 0.04, green: 0.06, blue: 0.10, alpha: 1.0),
        CGColor(red: 0.08, green: 0.10, blue: 0.16, alpha: 1.0),
        CGColor(red: 0.03, green: 0.04, blue: 0.07, alpha: 1.0)
    ] as CFArray
    let bgLocations: [CGFloat] = [0.0, 0.5, 1.0]
    if let bgGradient = CGGradient(colorsSpace: colorSpace, colors: bgColors, locations: bgLocations) {
        ctx.drawLinearGradient(bgGradient, start: CGPoint(x: 0, y: height), end: CGPoint(x: 0, y: 0), options: [])
    }

    // Studio Spotlights (Cones of warm golden light from ceiling)
    let spotColors = [
        CGColor(red: 0.95, green: 0.78, blue: 0.40, alpha: 0.16),
        CGColor(red: 0.85, green: 0.65, blue: 0.25, alpha: 0.04),
        CGColor(red: 0.0, green: 0.0, blue: 0.0, alpha: 0.0)
    ] as CFArray
    let spotLocations: [CGFloat] = [0.0, 0.4, 1.0]
    if let spotGrad = CGGradient(colorsSpace: colorSpace, colors: spotColors, locations: spotLocations) {
        // Spotlight 1 (Left)
        ctx.saveGState()
        ctx.drawRadialGradient(spotGrad, startCenter: CGPoint(x: 400, y: height - 50), startRadius: 10, endCenter: CGPoint(x: 550, y: 350), endRadius: 650, options: [])
        ctx.restoreGState()

        // Spotlight 2 (Right)
        ctx.saveGState()
        ctx.drawRadialGradient(spotGrad, startCenter: CGPoint(x: width - 400, y: height - 50), startRadius: 10, endCenter: CGPoint(x: width - 550, y: 350), endRadius: 650, options: [])
        ctx.restoreGState()

        // Center Stage Wash
        ctx.saveGState()
        let centerColors = [
            CGColor(red: 0.45, green: 0.55, blue: 0.85, alpha: 0.12),
            CGColor(red: 0.1, green: 0.15, blue: 0.3, alpha: 0.0)
        ] as CFArray
        if let centerGrad = CGGradient(colorsSpace: colorSpace, colors: centerColors, locations: [0.0, 1.0]) {
            ctx.drawRadialGradient(centerGrad, startCenter: CGPoint(x: width / 2, y: height / 2 + 100), startRadius: 50, endCenter: CGPoint(x: width / 2, y: height / 2), endRadius: 800, options: [])
        }
        ctx.restoreGState()
    }

    // Architectural Persian Grid Overlay & Stage Beams
    ctx.setStrokeColor(CGColor(red: 0.77, green: 0.61, blue: 0.29, alpha: 0.07))
    ctx.setLineWidth(1.0)
    for x in stride(from: 0, through: width, by: 60) {
        ctx.move(to: CGPoint(x: x, y: 0))
        ctx.addLine(to: CGPoint(x: x, y: height))
        ctx.strokePath()
    }
    for y in stride(from: 0, through: height, by: 60) {
        ctx.move(to: CGPoint(x: 0, y: y))
        ctx.addLine(to: CGPoint(x: width, y: y))
        ctx.strokePath()
    }

    // Top Studio Truss (Metallic burnished beam)
    ctx.setFillColor(CGColor(red: 0.06, green: 0.07, blue: 0.09, alpha: 0.95))
    ctx.fill(CGRect(x: 0, y: height - 32, width: width, height: 32))
    ctx.setStrokeColor(CGColor(red: 0.77, green: 0.61, blue: 0.29, alpha: 0.4))
    ctx.setLineWidth(2.0)
    ctx.stroke(CGRect(x: 0, y: height - 32, width: width, height: 2))

    image.unlockFocus()
    savePNG(image: image, filename: "studio_stage_bg.png")
}

// 2. Persian Shamseh Geometric Rosette (512x512)
func generateShamseh() {
    let size: CGFloat = 512
    let image = NSImage(size: NSSize(width: size, height: size))
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { return }

    let center = CGPoint(x: size / 2, y: size / 2)
    let radius = size * 0.44

    // 16-pointed star rosette
    ctx.saveGState()
    ctx.translateBy(x: center.x, y: center.y)

    let gold = CGColor(red: 0.85, green: 0.68, blue: 0.32, alpha: 0.9)
    let bronze = CGColor(red: 0.65, green: 0.48, blue: 0.20, alpha: 0.8)
    let lapis = CGColor(red: 0.15, green: 0.28, blue: 0.48, alpha: 0.6)

    // Outer concentric circles
    ctx.setStrokeColor(gold)
    ctx.setLineWidth(3.0)
    ctx.strokeEllipse(in: CGRect(x: -radius, y: -radius, width: radius * 2, height: radius * 2))

    ctx.setStrokeColor(bronze)
    ctx.setLineWidth(1.5)
    ctx.strokeEllipse(in: CGRect(x: -radius + 8, y: -radius + 8, width: (radius - 8) * 2, height: (radius - 8) * 2))

    // Intersecting squares / 16-point geometric stars
    let numSquares = 8
    for i in 0..<numSquares {
        let angle = CGFloat(i) * (.pi / CGFloat(numSquares * 2))
        ctx.saveGState()
        ctx.rotate(by: angle)
        let rectRadius = radius * 0.85
        let path = CGPath(rect: CGRect(x: -rectRadius, y: -rectRadius, width: rectRadius * 2, height: rectRadius * 2), transform: nil)
        ctx.setStrokeColor(gold)
        ctx.setLineWidth(2.0)
        ctx.addPath(path)
        ctx.strokePath()

        // Inner petal fill
        ctx.setFillColor(lapis)
        ctx.fillEllipse(in: CGRect(x: -rectRadius * 0.45, y: -rectRadius * 0.45, width: rectRadius * 0.9, height: rectRadius * 0.9))
        ctx.restoreGState()
    }

    // Central Sun / Medallion
    ctx.setFillColor(gold)
    ctx.fillEllipse(in: CGRect(x: -radius * 0.22, y: -radius * 0.22, width: radius * 0.44, height: radius * 0.44))

    ctx.setFillColor(CGColor(red: 0.10, green: 0.12, blue: 0.16, alpha: 1.0))
    ctx.fillEllipse(in: CGRect(x: -radius * 0.14, y: -radius * 0.14, width: radius * 0.28, height: radius * 0.28))

    ctx.setFillColor(gold)
    ctx.fillEllipse(in: CGRect(x: -radius * 0.06, y: -radius * 0.06, width: radius * 0.12, height: radius * 0.12))

    ctx.restoreGState()

    image.unlockFocus()
    savePNG(image: image, filename: "persian_shamseh.png")
}

// 3. Sealed Wager / Daily Double Graphic (600x400)
func generateSealedWagerCard() {
    let width: CGFloat = 600
    let height: CGFloat = 400
    let image = NSImage(size: NSSize(width: width, height: height))
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { return }

    // Crimson & Royal Gold Imperial Frame
    let rect = CGRect(x: 10, y: 10, width: width - 20, height: height - 20)
    let path = CGPath(roundedRect: rect, cornerWidth: 16, cornerHeight: 16, transform: nil)

    // Dark crimson gradient
    let colorSpace = CGColorSpaceCreateDeviceRGB()
    let sealColors = [
        CGColor(red: 0.45, green: 0.08, blue: 0.08, alpha: 0.96),
        CGColor(red: 0.22, green: 0.04, blue: 0.04, alpha: 0.98),
        CGColor(red: 0.12, green: 0.02, blue: 0.02, alpha: 1.0)
    ] as CFArray
    if let grad = CGGradient(colorsSpace: colorSpace, colors: sealColors, locations: [0.0, 0.6, 1.0]) {
        ctx.saveGState()
        ctx.addPath(path)
        ctx.clip()
        ctx.drawRadialGradient(grad, startCenter: CGPoint(x: width / 2, y: height / 2), startRadius: 20, endCenter: CGPoint(x: width / 2, y: height / 2), endRadius: width / 2, options: [])
        ctx.restoreGState()
    }

    // Gold borders
    ctx.setStrokeColor(CGColor(red: 0.90, green: 0.75, blue: 0.35, alpha: 1.0))
    ctx.setLineWidth(4.0)
    ctx.addPath(path)
    ctx.strokePath()

    let innerRect = rect.insetBy(dx: 12, dy: 12)
    let innerPath = CGPath(roundedRect: innerRect, cornerWidth: 10, cornerHeight: 10, transform: nil)
    ctx.setStrokeColor(CGColor(red: 0.77, green: 0.61, blue: 0.29, alpha: 0.6))
    ctx.setLineWidth(1.5)
    ctx.addPath(innerPath)
    ctx.strokePath()

    // Sun rays radiating from center
    let center = CGPoint(x: width / 2, y: height / 2 + 10)
    ctx.saveGState()
    ctx.setStrokeColor(CGColor(red: 0.95, green: 0.80, blue: 0.35, alpha: 0.12))
    ctx.setLineWidth(2.0)
    for a in stride(from: 0, to: 360, by: 15) {
        let rad = CGFloat(a) * .pi / 180.0
        ctx.move(to: center)
        ctx.addLine(to: CGPoint(x: center.x + cos(rad) * 350, y: center.y + sin(rad) * 350))
        ctx.strokePath()
    }
    ctx.restoreGState()

    // Central Wax Seal Stamp
    let stampRadius: CGFloat = 85
    let stampRect = CGRect(x: center.x - stampRadius, y: center.y - stampRadius, width: stampRadius * 2, height: stampRadius * 2)
    ctx.setFillColor(CGColor(red: 0.65, green: 0.12, blue: 0.10, alpha: 0.95))
    ctx.fillEllipse(in: stampRect)
    ctx.setStrokeColor(CGColor(red: 0.95, green: 0.80, blue: 0.35, alpha: 0.9))
    ctx.setLineWidth(3.0)
    ctx.strokeEllipse(in: stampRect)

    image.unlockFocus()
    savePNG(image: image, filename: "sealed_wager_card.png")
}

// 4. Persepolis Victory Trophy (512x512)
func generateTrophy() {
    let size: CGFloat = 512
    let image = NSImage(size: NSSize(width: size, height: size))
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { return }

    let center = CGPoint(x: size / 2, y: size / 2)

    // Marble Base
    let baseRect = CGRect(x: center.x - 110, y: 40, width: 220, height: 50)
    ctx.setFillColor(CGColor(red: 0.12, green: 0.13, blue: 0.16, alpha: 1.0))
    ctx.fill(baseRect)
    ctx.setStrokeColor(CGColor(red: 0.77, green: 0.61, blue: 0.29, alpha: 0.8))
    ctx.setLineWidth(3.0)
    ctx.stroke(baseRect)

    // Gold Trophy Pedestal
    let pedPath = CGMutablePath()
    pedPath.move(to: CGPoint(x: center.x - 70, y: 90))
    pedPath.addLine(to: CGPoint(x: center.x + 70, y: 90))
    pedPath.addLine(to: CGPoint(x: center.x + 25, y: 220))
    pedPath.addLine(to: CGPoint(x: center.x - 25, y: 220))
    pedPath.closeSubpath()
    ctx.setFillColor(CGColor(red: 0.85, green: 0.68, blue: 0.30, alpha: 1.0))
    ctx.addPath(pedPath)
    ctx.fillPath()

    // Grand Golden Chalice / Urn
    let chalicePath = CGMutablePath()
    chalicePath.move(to: CGPoint(x: center.x - 30, y: 220))
    chalicePath.addLine(to: CGPoint(x: center.x + 30, y: 220))
    chalicePath.addCurve(to: CGPoint(x: center.x + 130, y: 400), control1: CGPoint(x: center.x + 110, y: 250), control2: CGPoint(x: center.x + 140, y: 340))
    chalicePath.addLine(to: CGPoint(x: center.x - 130, y: 400))
    chalicePath.addCurve(to: CGPoint(x: center.x - 30, y: 220), control1: CGPoint(x: center.x - 140, y: 340), control2: CGPoint(x: center.x - 110, y: 250))
    chalicePath.closeSubpath()

    ctx.setFillColor(CGColor(red: 0.95, green: 0.78, blue: 0.35, alpha: 1.0))
    ctx.addPath(chalicePath)
    ctx.fillPath()
    ctx.setStrokeColor(CGColor(red: 0.65, green: 0.48, blue: 0.18, alpha: 1.0))
    ctx.setLineWidth(3.0)
    ctx.addPath(chalicePath)
    ctx.strokePath()

    // Chalice Handles (Winged Persepolis Griffin handles)
    let leftHandle = CGMutablePath()
    leftHandle.move(to: CGPoint(x: center.x - 110, y: 380))
    leftHandle.addCurve(to: CGPoint(x: center.x - 110, y: 260), control1: CGPoint(x: center.x - 190, y: 380), control2: CGPoint(x: center.x - 190, y: 260))
    ctx.setStrokeColor(CGColor(red: 0.88, green: 0.72, blue: 0.32, alpha: 1.0))
    ctx.setLineWidth(14.0)
    ctx.addPath(leftHandle)
    ctx.strokePath()

    let rightHandle = CGMutablePath()
    rightHandle.move(to: CGPoint(x: center.x + 110, y: 380))
    rightHandle.addCurve(to: CGPoint(x: center.x + 110, y: 260), control1: CGPoint(x: center.x + 190, y: 380), control2: CGPoint(x: center.x + 190, y: 260))
    ctx.addPath(rightHandle)
    ctx.strokePath()

    // Laurel Wreath
    ctx.setStrokeColor(CGColor(red: 0.28, green: 0.65, blue: 0.35, alpha: 0.7))
    ctx.setLineWidth(4.0)
    ctx.strokeEllipse(in: CGRect(x: center.x - 90, y: 270, width: 180, height: 90))

    image.unlockFocus()
    savePNG(image: image, filename: "trophy_cup.png")
}

// 5. Category Period Badges (256x256 each)
func generateBadge(filename: String, primaryColor: (CGFloat, CGFloat, CGFloat), symbol: String) {
    let size: CGFloat = 256
    let image = NSImage(size: NSSize(width: size, height: size))
    image.lockFocus()
    guard let ctx = NSGraphicsContext.current?.cgContext else { return }

    let center = CGPoint(x: size / 2, y: size / 2)
    let r = size * 0.44

    // Outer Circle
    ctx.setFillColor(CGColor(red: primaryColor.0 * 0.2, green: primaryColor.1 * 0.2, blue: primaryColor.2 * 0.2, alpha: 0.95))
    ctx.fillEllipse(in: CGRect(x: center.x - r, y: center.y - r, width: r * 2, height: r * 2))

    ctx.setStrokeColor(CGColor(red: primaryColor.0, green: primaryColor.1, blue: primaryColor.2, alpha: 1.0))
    ctx.setLineWidth(4.0)
    ctx.strokeEllipse(in: CGRect(x: center.x - r, y: center.y - r, width: r * 2, height: r * 2))

    // Inner Gold Bezel
    ctx.setStrokeColor(CGColor(red: 0.85, green: 0.68, blue: 0.32, alpha: 0.8))
    ctx.setLineWidth(2.0)
    ctx.strokeEllipse(in: CGRect(x: center.x - r + 8, y: center.y - r + 8, width: (r - 8) * 2, height: (r - 8) * 2))

    // Centered Glyphs / Letters
    let str = symbol as NSString
    let font = NSFont.systemFont(ofSize: 48, weight: .bold)
    let attrs: [NSAttributedString.Key: Any] = [
        .font: font,
        .foregroundColor: NSColor(calibratedRed: 0.95, green: 0.85, blue: 0.50, alpha: 1.0)
    ]
    let strSize = str.size(withAttributes: attrs)
    str.draw(at: CGPoint(x: center.x - strSize.width / 2, y: center.y - strSize.height / 2), withAttributes: attrs)

    image.unlockFocus()
    savePNG(image: image, filename: filename)
}

print("Generating visual assets for Iranian Jeopardy...")
generateStudioBackdrop()
generateShamseh()
generateSealedWagerCard()
generateTrophy()

generateBadge(filename: "badge_safavid.png", primaryColor: (0.2, 0.4, 0.8), symbol: "صفوی")
generateBadge(filename: "badge_qajar.png", primaryColor: (0.7, 0.2, 0.2), symbol: "قاجار")
generateBadge(filename: "badge_mashruteh.png", primaryColor: (0.3, 0.6, 0.4), symbol: "مشروطه")
generateBadge(filename: "badge_pahlavi.png", primaryColor: (0.8, 0.6, 0.2), symbol: "پهلوی")
generateBadge(filename: "badge_oil.png", primaryColor: (0.8, 0.4, 0.1), symbol: "نفت")
generateBadge(filename: "badge_cinema.png", primaryColor: (0.6, 0.3, 0.7), symbol: "سینما")
generateBadge(filename: "badge_war.png", primaryColor: (0.7, 0.2, 0.3), symbol: "دفاع")
generateBadge(filename: "badge_culture.png", primaryColor: (0.2, 0.6, 0.6), symbol: "فرهنگ")

print("All visual assets generated successfully!")
