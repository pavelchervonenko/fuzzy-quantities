# Документация Student Lab

- [Назначение и требования](requirements.md)
- [Математическая модель](math-model.md)
- [Архитектура](architecture.md)
- [Процессы приложения](processes.md)
- [Реализованные возможности](implementation-status.md)

## Схемы

| Схема | PNG | SVG | BPMN |
|---|---|---|---|
| Данные и связи — Чен | [PNG](diagrams/01-chen.png) | [SVG](diagrams/01-chen.svg) | — |
| Функции и потоки — Гейн–Сарсон | [PNG](diagrams/02-gane-sarson.png) | [SVG](diagrams/02-gane-sarson.svg) | — |
| 1.0 Задать и изменить величины | [PNG](diagrams/bpmn-10-values.png) | [SVG](diagrams/bpmn-10-values.svg) | [BPMN](diagrams/bpmn-10-values.bpmn) |
| 2.0 Генерация | [PNG](diagrams/bpmn-20-generation.png) | [SVG](diagrams/bpmn-20-generation.svg) | [BPMN](diagrams/bpmn-20-generation.bpmn) |
| 3.0 Принадлежность, арифметика и сравнение | [PNG](diagrams/bpmn-30-operations.png) | [SVG](diagrams/bpmn-30-operations.svg) | [BPMN](diagrams/bpmn-30-operations.bpmn) |
| 4.0 Кластеризация | [PNG](diagrams/bpmn-40-clustering.png) | [SVG](diagrams/bpmn-40-clustering.svg) | [BPMN](diagrams/bpmn-40-clustering.bpmn) |
| 5.0 Сохранение, загрузка и экспорт | [PNG](diagrams/bpmn-50-files.png) | [SVG](diagrams/bpmn-50-files.svg) | [BPMN](diagrams/bpmn-50-files.bpmn) |
| 6.0 Чтение журнала | [PNG](diagrams/bpmn-60-journal.png) | [SVG](diagrams/bpmn-60-journal.svg) | [BPMN](diagrams/bpmn-60-journal.bpmn) |
| Компоненты — C4 C3 | [PNG](diagrams/04-c4-components.png) | [SVG](diagrams/04-c4-components.svg) | — |

BPMN описывает обработку запросов приложением. Это описательные модели,
не предназначенные для исполнения процессным движком.

## Обновление изображений

Нужны Python 3, Pillow и шрифты DejaVu Sans:

```bash
python3 docs/tools/render_diagrams.py
python3 docs/tools/render_processes.py
```

Для формул нужны Python 3 и Matplotlib. Их исходная LaTeX-запись хранится в комментариях `math-model.md`:

```bash
python3 docs/tools/render_formulas.py
```

Проверка ссылок, изображений, BPMN и опорных формул:

```bash
./gradlew checkDocumentation
```

В Windows интерпретатор можно выбрать через `-PpythonExecutable=python`.
Проверка схем не заменяет тесты Java-приложения.
