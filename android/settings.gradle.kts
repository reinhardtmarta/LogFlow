pluginManagement {
    val flutterSdkPath =
        run {
            val properties = java.util.Properties()
            file("local.properties").inputStream().use { properties.load(it) }
            val flutterSdkPath = properties.getProperty("flutter.sdk")
            require(flutterSdkPath != null) { "flutter.sdk not set in local.properties" }
            flutterSdkPath
        }

    includeBuild("$flutterSdkPath/packages/flutter_tools/gradle")

    repositories {
        google()
        mavenCentral()
        gradlePluginPortal()
    }
}

plugins {
    id("dev.flutter.flutter-plugin-loader") version "1.0.0"
    id("com.android.application") version "9.0.1" apply false
    id("org.jetbrains.kotlin.android") version "2.3.20" apply false
}

include(":app")

// Manually include Flutter native plugins from .flutter-plugins-dependencies
// This is a workaround for flutter-plugin-loader not auto-including them
fun Settings.includeFlutterNativePlugins(flutterSourceDir: String) {
    val pluginsFile = file("$flutterSourceDir/.flutter-plugins-dependencies")
    if (!pluginsFile.exists()) return

    val json = groovy.json.JsonSlurper().parseText(pluginsFile.readText())
    val androidPlugins = (json.plugins.android as List<Any>)?.filter { (it as Map<String, Any>)["native_build"] as? Boolean == true } ?: return

    androidPlugins.forEach { plugin ->
        val pluginMap = plugin as Map<String, Any>
        val name = pluginMap["name"] as String
        val path = pluginMap["path"] as String
        val pluginDir = file(path)
        if (pluginDir.exists()) {
            include(":$name")
            project(":$name").projectDir = pluginDir
            println("Included Flutter native plugin: $name from $path")
        }
    }
}

// Get flutter source path from local.properties
val flutterSourceDir: String by lazy {
    val properties = java.util.Properties()
    file("local.properties").inputStream().use { properties.load(it) }
    "${properties.getProperty("flutter.sdk")}/../.."
}

includeFlutterNativePlugins(flutterSourceDir)
