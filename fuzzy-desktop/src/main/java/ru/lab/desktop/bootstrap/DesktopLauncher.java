package ru.lab.desktop.bootstrap;

import javafx.application.Application;

/** Classpath entry point for the desktop distribution. */
public final class DesktopLauncher {
    private DesktopLauncher() {
    }

    public static void main(String[] args) {
        Application.launch(StudentLabApplication.class, args);
    }
}
