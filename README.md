# Student Lab

Настольное приложение и Java-библиотека для нечётких величин на основе функции Стьюдента.
Целевая модель ограничивает слабые хвосты параметром ε и выполняет операции через α-сечения.

Исходники написаны на Java 21, сборка — Gradle Kotlin DSL.

## Возможности

`fuzzy-core` создаёт ограниченную через ε нечёткую величину Стьюдента
из `StudentParameters(c, s, k)` и вычисляет принадлежность, замкнутый носитель
и аналитические α-сечения. Отдельный пример вызывает этот API через готовый JAR.
Доступна JavaFX-оболочка с пятью разделами.
Арифметика, генераторы, кластеризация и работа с файлами запланированы.

## Модули

| Модуль | Назначение | Допустимые зависимости |
|---|---|---|
| `fuzzy-core` | Математические значения и инварианты | Стандартная Java |
| `fuzzy-algorithms` | Арифметика, ранжирование, генерация и кластеризация | core |
| `fuzzy-application` | Эксперименты, снимки, сценарии и порты | core, algorithms |
| `fuzzy-io` | JSON, CSV и журнал | core, application |
| `fuzzy-desktop` | JavaFX, MVVM и композиция приложения | application, core; io и algorithms только в bootstrap |

Имя Gradle-проекта — `fuzzy-quantities`, Java-префикс — `ru.lab`.
Зависимости между модулями добавляются по необходимости; сейчас прямых обращений между ними нет.
JavaFX используется только в desktop. Версии библиотек заданы в `gradle/libs.versions.toml`.

## Сборка

Нужен JDK 21, выбранный в `JAVA_HOME` и `PATH`. Gradle устанавливать отдельно не требуется:
Wrapper загружает закреплённую версию. Для первой загрузки нужны доступ к серверам Gradle
и Maven Central. В IDE выберите JDK 21 и Gradle JVM 21.

Из корня проекта:

```bash
./gradlew clean check assemble
./gradlew -p examples/library-consumer clean run
```

Библиотечные JAR и архивы исходников создаются в `<модуль>/build/libs/`.
Пример использует готовые JAR core и algorithms без JavaFX и исходников библиотек.
Подробности — в [примере потребителя](examples/library-consumer/README.md).

В Windows используйте `gradlew.bat`. В WSL запускайте Linux Wrapper.

## Запуск

Для Linux/WSL нужны GTK 3 и графический дисплей, например WSLg.

```bash
./gradlew :fuzzy-desktop:run
```

Можно собрать отдельный дистрибутив:

```bash
./gradlew :fuzzy-desktop:installDist
./fuzzy-desktop/build/install/fuzzy-desktop/bin/fuzzy-desktop
```

## Документация

[Назначение и требования](docs/requirements.md) ·
[математическая модель](docs/math-model.md) ·
[архитектура](docs/architecture.md) ·
[процессы](docs/processes.md) ·
[схемы](docs/README.md) ·
[реализованные возможности](docs/implementation-status.md).

Проверка схем и ссылок: `./gradlew checkDocumentation`.
Для неё нужны Python 3 и Pillow; для воспроизведения изображений также нужны шрифты DejaVu Sans.
Python не требуется для обычной Java-сборки.
