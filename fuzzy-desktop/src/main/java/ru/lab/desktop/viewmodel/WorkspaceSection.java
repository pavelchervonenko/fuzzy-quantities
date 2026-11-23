package ru.lab.desktop.viewmodel;

/** The available workspaces and their initial empty states. */
public enum WorkspaceSection {
    VALUES("Величины", "Величин пока нет", "Здесь появятся величины Стьюдента."),
    OPERATIONS("Операции", "Операций пока нет", "Здесь появятся результаты вычислений."),
    GENERATION("Генерация", "Выборок и наборов пока нет", "Здесь появятся результаты генерации."),
    CLUSTERS("Кластеры", "Кластеры ещё не построены", "Здесь появятся группы похожих величин."),
    LOG("Журнал", "Журнал пуст", "Здесь появятся записи запусков.");

    private final String title;
    private final String emptyTitle;
    private final String emptyDescription;

    WorkspaceSection(String title, String emptyTitle, String emptyDescription) {
        this.title = title;
        this.emptyTitle = emptyTitle;
        this.emptyDescription = emptyDescription;
    }

    public String title() {
        return title;
    }

    public String emptyTitle() {
        return emptyTitle;
    }

    public String emptyDescription() {
        return emptyDescription;
    }
}
