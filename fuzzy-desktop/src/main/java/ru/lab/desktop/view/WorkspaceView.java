package ru.lab.desktop.view;

import java.util.EnumMap;
import java.util.Map;
import java.util.Objects;
import javafx.css.PseudoClass;
import javafx.geometry.Pos;
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.layout.BorderPane;
import javafx.scene.layout.VBox;
import ru.lab.desktop.viewmodel.WorkspaceSection;
import ru.lab.desktop.viewmodel.WorkspaceViewModel;

/** Thin view: renders navigation and empty states from a separate view model. */
public final class WorkspaceView extends BorderPane {
    private static final PseudoClass ACTIVE = PseudoClass.getPseudoClass("active");
    private final Map<WorkspaceSection, Button> navigation = new EnumMap<>(WorkspaceSection.class);
    private final Label heading = new Label();
    private final Label emptyTitle = new Label();
    private final Label emptyDescription = new Label();

    public WorkspaceView(WorkspaceViewModel viewModel) {
        Objects.requireNonNull(viewModel, "viewModel");
        getStyleClass().add("workspace");

        var brand = new Label("Student Lab");
        brand.getStyleClass().add("brand");
        var sidebar = new VBox(8, brand);
        sidebar.getStyleClass().add("sidebar");
        for (var section : WorkspaceSection.values()) {
            var button = new Button(section.title());
            button.setId("nav-" + section.name().toLowerCase(java.util.Locale.ROOT));
            button.getStyleClass().add("nav-button");
            button.setMaxWidth(Double.MAX_VALUE);
            button.setOnAction(event -> viewModel.select(section));
            sidebar.getChildren().add(button);
            navigation.put(section, button);
        }
        setLeft(sidebar);

        heading.setId("section-title");
        heading.getStyleClass().add("section-title");
        emptyTitle.setId("empty-title");
        emptyTitle.getStyleClass().add("empty-title");
        emptyDescription.getStyleClass().add("empty-description");
        emptyTitle.setWrapText(true);
        emptyDescription.setWrapText(true);
        var emptyState = new VBox(12, emptyTitle, emptyDescription);
        emptyState.setAlignment(Pos.CENTER);
        emptyState.getStyleClass().add("empty-state");
        var content = new BorderPane(emptyState);
        content.setTop(heading);
        content.getStyleClass().add("content");
        setCenter(content);

        viewModel.selectedSectionProperty().addListener((observable, previous, selected) -> render(selected));
        render(viewModel.selectedSection());
    }

    private void render(WorkspaceSection selected) {
        heading.setText(selected.title());
        emptyTitle.setText(selected.emptyTitle());
        emptyDescription.setText(selected.emptyDescription());
        navigation.forEach((section, button) -> button.pseudoClassStateChanged(ACTIVE, section == selected));
    }
}
