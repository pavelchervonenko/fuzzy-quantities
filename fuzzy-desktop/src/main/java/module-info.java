/** JavaFX application boundary; computational libraries remain independent JARs. */
module ru.lab.desktop {
    requires javafx.controls;

    exports ru.lab.desktop.bootstrap;
}
