import java.util.Locale

plugins {
    application
}

// JavaFX is resolved from Maven Central; no third-party Gradle plugin is needed.
val javafxVersion = libs.versions.javafx.get()
val operatingSystem = System.getProperty("os.name").lowercase(Locale.ROOT)
val architecture = System.getProperty("os.arch").lowercase(Locale.ROOT)
val javafxPlatform = when {
    operatingSystem.contains("linux") && architecture in setOf("amd64", "x86_64") -> "linux"
    operatingSystem.contains("linux") && architecture == "aarch64" -> "linux-aarch64"
    operatingSystem.contains("mac") && architecture in setOf("amd64", "x86_64") -> "mac"
    operatingSystem.contains("mac") && architecture == "aarch64" -> "mac-aarch64"
    operatingSystem.contains("win") && architecture in setOf("amd64", "x86_64") -> "win"
    else -> error("Unsupported JavaFX platform: $operatingSystem/$architecture")
}

dependencies {
    for (module in listOf("base", "graphics", "controls")) {
        implementation("org.openjfx:javafx-$module:$javafxVersion:$javafxPlatform") {
            isTransitive = false
        }
    }
}

java {
    modularity.inferModulePath.set(true)
}

application {
    mainModule.set("ru.lab.desktop")
    mainClass.set("ru.lab.desktop.bootstrap.DesktopLauncher")
}
