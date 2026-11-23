package ru.lab.desktop.viewmodel;

import java.util.Objects;
import javafx.beans.property.ReadOnlyObjectProperty;
import javafx.beans.property.ReadOnlyObjectWrapper;

/** Navigation state, independent of scene nodes and stages. */
public final class WorkspaceViewModel {
    private final ReadOnlyObjectWrapper<WorkspaceSection> selectedSection =
            new ReadOnlyObjectWrapper<>(WorkspaceSection.VALUES);

    public ReadOnlyObjectProperty<WorkspaceSection> selectedSectionProperty() {
        return selectedSection.getReadOnlyProperty();
    }

    public WorkspaceSection selectedSection() {
        return selectedSection.get();
    }

    public void select(WorkspaceSection section) {
        selectedSection.set(Objects.requireNonNull(section, "section"));
    }
}
