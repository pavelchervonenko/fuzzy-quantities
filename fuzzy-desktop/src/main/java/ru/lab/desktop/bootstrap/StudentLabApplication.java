package ru.lab.desktop.bootstrap;

import java.util.Objects;
import javafx.application.Application;
import javafx.scene.Scene;
import javafx.stage.Stage;
import ru.lab.desktop.view.WorkspaceView;
import ru.lab.desktop.viewmodel.WorkspaceViewModel;

/** Composes the view and its state; mathematical work belongs to the libraries. */
public final class StudentLabApplication extends Application {
    @Override
    public void start(Stage stage) {
        var viewModel = new WorkspaceViewModel();
        var scene = new Scene(new WorkspaceView(viewModel), 1100, 720);
        scene.getStylesheets().add(Objects.requireNonNull(
                StudentLabApplication.class.getResource("/ru/lab/desktop/workspace.css")).toExternalForm());
        stage.setTitle("Student Lab");
        stage.setMinWidth(780);
        stage.setMinHeight(520);
        stage.setScene(scene);
        stage.show();
    }
}
