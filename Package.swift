// swift-tools-version: 5.9
import PackageDescription

let package = Package(
    name: "JeopardyIranianEdition",
    defaultLocalization: "en",
    platforms: [
        .macOS(.v14),
        .iOS(.v17)
    ],
    products: [
        .library(
            name: "JeopardyGameEngine",
            targets: ["JeopardyGameEngine"]
        ),
        .executable(
            name: "JeopardyApp",
            targets: ["JeopardyApp"]
        ),
        .executable(
            name: "JeopardyTests",
            targets: ["JeopardyTests"]
        )
    ],
    dependencies: [],
    targets: [
        .target(
            name: "JeopardyGameEngine",
            dependencies: [],
            path: "GameEngine"
        ),
        .executableTarget(
            name: "JeopardyApp",
            dependencies: ["JeopardyGameEngine"],
            path: "App",
            resources: [.process("Resources")]
        ),
        .executableTarget(
            name: "JeopardyTests",
            dependencies: ["JeopardyGameEngine"],
            path: "Tests"
        )
    ]
)
