import java.util.jar.JarFile

plugins {
    application
}

java {
    toolchain.languageVersion.set(JavaLanguageVersion.of(21))
}

tasks.withType<JavaCompile>().configureEach {
    options.release.set(21)
    options.encoding = "UTF-8"
}

val libraryDirectory = providers.gradleProperty("studentLabLibraries")
    .map { file(it) }
    .getOrElse(file("../.."))
val libraryArtifacts = files(
    libraryDirectory.resolve("fuzzy-core/build/libs/fuzzy-core-0.1.0-SNAPSHOT.jar"),
    libraryDirectory.resolve("fuzzy-algorithms/build/libs/fuzzy-algorithms-0.1.0-SNAPSHOT.jar"),
)

dependencies {
    implementation(libraryArtifacts)
}

val verifyLibraryArtifacts = tasks.register("verifyLibraryArtifacts") {
    doLast {
        libraryArtifacts.forEach { artifact ->
            check(artifact.isFile) { "Build the Student Lab library JAR first: $artifact" }
            JarFile(artifact).use { jar ->
                check(jar.manifest != null) { "Missing JAR manifest: $artifact" }
                check(jar.entries().asSequence().none { it.name.startsWith("javafx/") }) {
                    "JavaFX must not be bundled with a mathematical library: $artifact"
                }
            }
            logger.lifecycle("Library artifact: $artifact")
        }
        check(configurations.runtimeClasspath.get().files == libraryArtifacts.files) {
            "The consumer must use only the two library JARs"
        }
    }
}

tasks.named("compileJava") {
    dependsOn(verifyLibraryArtifacts)
}

application {
    mainClass.set("example.LibraryConsumer")
}
