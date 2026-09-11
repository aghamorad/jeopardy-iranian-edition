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
        // The Mac app is a window onto the web show, not a copy of it. Three
        // files, no engine, no bundled assets: `build_release.sh` copies `Web/`
        // into the bundle and `ShowSource` finds it there.
        .executableTarget(
            name: "JeopardyApp",
            dependencies: [],
            path: "App",
            exclude: ["Resources"]
        ),
        .executableTarget(
            name: "JeopardyTests",
            dependencies: ["JeopardyGameEngine"],
            path: "Tests"
        )
    ]
)
