# Student Lab

Перед предметными изменениями прочитайте `docs/requirements.md`, `docs/architecture.md`,
`docs/math-model.md`, `docs/processes.md` и `docs/implementation-status.md`.

Java 21, Kotlin DSL, пять производственных Gradle-модулей. Сохраняйте зависимости:
core → стандартная Java; algorithms → core; application → core/algorithms;
io → core/application; desktop → application/core, а io/algorithms только в bootstrap.
Добавляйте зависимости по фактической необходимости. JavaFX допускается только в desktop;
порты хранения и журнала принадлежат application.

Проверки: `./gradlew clean check assemble`,
`./gradlew -p examples/library-consumer clean run`, `./gradlew checkDocumentation`.
Запуск UI: `./gradlew :fuzzy-desktop:run`.
Не выдавайте `NO-SOURCE` за выполненные тесты или запланированные функции за реализованные.
Развивайте математику небольшими согласованными шагами. Текущая модель ограничивает хвосты
через ε; деление отклоняется, если замкнутый носитель делителя содержит ноль.
Коммиты, push и публикации требуют отдельного поручения пользователя.
