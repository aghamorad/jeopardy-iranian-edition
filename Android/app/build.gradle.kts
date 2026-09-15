import java.util.Properties

plugins {
    id("com.android.application")
}

/* The signing key lives outside the tree, with its passwords beside it in a
   gitignored `keystore.properties`. Android refuses an unsigned package, so
   unlike the .ipa — which ships unsigned and lets the sideloader sign it — this
   one has to carry a signature of its own to be installable at all. The key is
   self-signed and is nobody's identity; it exists so that every future .apk
   signed with it is accepted as an update to the last. */
val keystoreProperties = Properties().apply {
    val file = rootProject.file("keystore.properties")
    if (file.exists()) file.inputStream().use { load(it) }
}

android {
    namespace = "com.morad.jeopardy"
    compileSdk = 34

    defaultConfig {
        applicationId = "com.morad.jeopardy"
        minSdk = 24
        targetSdk = 34
        // Kept in step with `build_release.sh` and `iOS/project.yml`, so the three
        // apps never disagree about which one is newer. A sideloader compares this
        // to decide whether an .apk is an update.
        versionCode = 107
        versionName = "1.0.7"
    }

    signingConfigs {
        create("release") {
            val store = rootProject.file(keystoreProperties.getProperty("storeFile") ?: "keystore/jeopardy.jks")
            if (store.exists()) {
                storeFile = store
                storePassword = keystoreProperties.getProperty("storePassword")
                keyAlias = keystoreProperties.getProperty("keyAlias")
                keyPassword = keystoreProperties.getProperty("keyPassword")
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            // The web tree is the app; shrinking would only be shrinking an asset
            // folder and a one-file Activity.
            signingConfig = signingConfigs.getByName("release")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

/* The show, staged verbatim — the same contract `build_ipa.sh` enforces with
   `ditto` and then verifies with a `diff -rq`. `Sync` rather than `Copy` so a
   file deleted from `Web/` is deleted here too instead of lingering in the
   bundle as a stale asset nothing can reach.

   Staged into the module rather than pointed at `../../Web` through
   `assets.srcDirs` because the loader addresses the tree as `/assets/Web/…`,
   the same shape the iOS and macOS bundles carry. */
val stageWeb by tasks.registering(Sync::class) {
    from(rootProject.file("../Web"))
    into(layout.projectDirectory.dir("src/main/assets/Web"))
    exclude("**/.DS_Store")
}

// A release that shipped a stale or half-copied Web tree is the one failure mode
// worth blocking on, so the check is a real one: the two trees have to agree.
val verifyWeb by tasks.registering {
    dependsOn(stageWeb)
    val source = rootProject.file("../Web")
    val staged = layout.projectDirectory.dir("src/main/assets/Web").asFile
    doLast {
        require(source.resolve("index.html").isFile) { "Web/index.html is missing" }
        for (required in listOf("data/clues.js", "data/clues_fa.js", "i18n.js", "app.js")) {
            require(staged.resolve(required).isFile) { "staged Web tree is missing $required" }
        }
        val expected = source.walkTopDown().filter { it.isFile && it.name != ".DS_Store" }
            .map { it.relativeTo(source).path }.toSet()
        val actual = staged.walkTopDown().filter { it.isFile && it.name != ".DS_Store" }
            .map { it.relativeTo(staged).path }.toSet()
        val missing = expected - actual
        val extra = actual - expected
        require(missing.isEmpty() && extra.isEmpty()) {
            "staged Web tree drifted from source; missing=${missing.take(5)} extra=${extra.take(5)}"
        }
    }
}

tasks.named("preBuild") { dependsOn(verifyWeb) }

dependencies {
    // `WebViewAssetLoader`: serves the staged tree from
    // `https://appassets.androidplatform.net/` rather than `file:///android_asset/`.
    // The game keeps its language and edition choices in `localStorage`, and a
    // `file://` origin is opaque enough that WebView will not promise to keep them.
    // A real https origin behaves the way the web build was written to behave.
    implementation("androidx.webkit:webkit:1.11.0")
}
