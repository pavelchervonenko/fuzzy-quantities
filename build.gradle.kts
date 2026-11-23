import org.gradle.api.artifacts.ProjectDependency

plugins {
    base
}

allprojects {
    group = "ru.lab"
    version = "0.1.0-SNAPSHOT"
}

subprojects {
    repositories {
        mavenCentral()
    }

    plugins.withId("java") {
        extensions.configure<JavaPluginExtension> {
            toolchain.languageVersion.set(JavaLanguageVersion.of(21))
            withSourcesJar()
        }

        tasks.withType<JavaCompile>().configureEach {
            options.release.set(21)
            options.encoding = "UTF-8"
        }
        tasks.withType<Javadoc>().configureEach {
            options.encoding = "UTF-8"
        }
        tasks.withType<Test>().configureEach {
            useJUnitPlatform()
            testLogging {
                events("failed", "skipped")
            }
        }
        tasks.withType<Jar>().configureEach {
            isPreserveFileTimestamps = false
            isReproducibleFileOrder = true
        }

        dependencies {
            add("testImplementation", platform(libs.junit.bom))
            add("testImplementation", libs.junit.jupiter)
            add("testRuntimeOnly", libs.junit.platform.launcher)
        }
    }
}

val verifyModuleBoundaries = tasks.register("verifyModuleBoundaries") {
    group = "verification"
    description = "Checks project dependency directions, cycles, and production library classpaths."

    doLast {
        val allowed = mapOf(
            ":fuzzy-core" to emptySet(),
            ":fuzzy-algorithms" to setOf(":fuzzy-core"),
            ":fuzzy-application" to setOf(":fuzzy-core", ":fuzzy-algorithms"),
            ":fuzzy-io" to setOf(":fuzzy-core", ":fuzzy-application"),
            ":fuzzy-desktop" to setOf(":fuzzy-core", ":fuzzy-algorithms", ":fuzzy-application", ":fuzzy-io"),
        )
        val graph = subprojects.associate { module ->
            module.path to module.configurations.flatMap { configuration ->
                configuration.dependencies.withType<ProjectDependency>().map { it.path }
            }.toSet()
        }
        check(graph.keys == allowed.keys) { "Expected exactly five production modules: ${graph.keys}" }
        graph.forEach { (module, dependencies) ->
            check(allowed.getValue(module).containsAll(dependencies)) {
                "Forbidden dependencies in $module: ${dependencies - allowed.getValue(module)}"
            }
        }
        fun visit(module: String, ancestors: Set<String>) {
            check(module !in ancestors) { "Dependency cycle: $ancestors -> $module" }
            graph.getValue(module).forEach { visit(it, ancestors + module) }
        }
        graph.keys.forEach { visit(it, emptySet()) }

        for (module in subprojects.filter { it.name != "fuzzy-desktop" }) {
            for (name in listOf("compileClasspath", "runtimeClasspath")) {
                val artifacts = module.configurations.getByName(name).resolvedConfiguration.resolvedArtifacts
                check(artifacts.none { it.moduleVersion.id.group == "org.openjfx" }) {
                    "JavaFX is only allowed in fuzzy-desktop: ${module.path}/$name"
                }
            }
        }

        // Only application composition may refer directly to adapters and algorithms.
        val desktopSources = project(":fuzzy-desktop").fileTree("src/main/java") {
            include("**/*.java")
            exclude("module-info.java", "ru/lab/desktop/bootstrap/**")
        }
        val forbiddenDesktopImport = Regex("(?m)^\\s*import\\s+(?:static\\s+)?ru\\.lab\\.(?:io|algorithms)\\.")
        for (source in desktopSources) {
            check(!forbiddenDesktopImport.containsMatchIn(source.readText(Charsets.UTF_8))) {
                "Desktop views and view models must use application scenarios: $source"
            }
        }

        for (path in listOf(":fuzzy-core", ":fuzzy-algorithms")) {
            val module = project(path)
            for (name in listOf("compileClasspath", "runtimeClasspath")) {
                val artifacts = module.configurations.getByName(name).resolvedConfiguration.resolvedArtifacts
                check(artifacts.all { it.moduleVersion.id.group == project.group.toString()
                    && it.name == "fuzzy-core" && path == ":fuzzy-algorithms" }) {
                    "Unexpected production dependencies in $path/$name: $artifacts"
                }
                logger.lifecycle("$path/$name: ${artifacts.map { it.moduleVersion.id }.ifEmpty { listOf("JDK only") }}")
            }
        }
        logger.lifecycle("Module dependency directions and absence of cycles verified: $graph")
    }
}

tasks.register<Exec>("checkDocumentation") {
    group = "verification"
    description = "Checks diagrams, BPMN structure, links, and documented formula examples."
    commandLine(providers.gradleProperty("pythonExecutable").getOrElse("python3"), "docs/tools/check_design.py")
}

tasks.named("check") {
    dependsOn(verifyModuleBoundaries, subprojects.map { "${it.path}:check" })
}

tasks.named("assemble") {
    dependsOn(subprojects.map { "${it.path}:assemble" })
}

tasks.named("clean") {
    dependsOn(subprojects.map { "${it.path}:clean" })
}
