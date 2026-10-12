# Проверка Symfony Best Practices 0.1.0

Дата: 2026-10-13. Ветка: codex/symfony-skill-0.1.0, исходный commit: 2b5d9b46161910c7eb75518358702c9d16d150fd. Работа выполнена в отдельном managed worktree; основной checkout не изменялся.

## Выполненные проверки

| Проверка | Результат |
| --- | --- |
| Package validator | PASS: metadata/UI, версия 0.1.0, ссылки/routing, 7 групп / 18 references, 42 repository-qualified донорских записи и 77 source entries |
| Provenance с pinned donor checkout | PASS: оба pinned HEAD 459bcd0b7742e2f636374daa3552d9574527410e и ecebbb967b4ae7006694aec9b32ec071c60d84d7, фактические SHA-256 всех 77 файлов и обеих LICENSE совпали |
| skill-creator quick_validate.py | PASS: Skill is valid |
| unittest | PASS: 11 test methods, 18 прежних + 6 новых поврежденных вариантов и 4 отдельных rejection tests |
| Архивы | PASS: tar.gz/zip содержат ровно 24 файла канонического сгруппированного skill; bytes файлов и SHA256SUMS проверены |
| Воспроизводимость | PASS: два независимых rebuild в одном toolchain дали одинаковые байты архивов и SHA256SUMS |
| Сценарное применение | 10 первоначальных сценариев + 5 новых B1–B5 с адресными references; checkpoint ambiguity исправлена ранее, новая Console ссылка и resolver-version ambiguity исправлены и повторно проверены |
| Независимое ревью упаковки | Critical/important дефектов не найдено; reviewer независимо повторил validator, upstream hashes, 11 tests и упаковку; minor whitespace исправлен, diff check повторен |
| Whitespace | git diff --check: PASS |

Локальное окружение проверки: Python 3.14.7, PyYAML 6.0.3 в отдельном временном venv. CI workflow настроен на Python 3.11; запуск нативного GitHub CI в этой работе не выполнялся. Для обычной локальной проверки используются команды из [README](../README.md).

Перед реализацией package commands были запущены те же пять начальных test methods: все пять завершились ожидаемыми assertion failures, потому что skill и команды validator/builder отсутствовали. После реализации и расширения негативных случаев одиннадцать методов проходят. Это проверяемый RED/GREEN для упаковки.

Baseline агент без нового skill также ответил на шесть исходных сценариев; зафиксированных провалов не наблюдалось. Улучшение поведения модели в процентах не заявляется. [Сценарии и rubric](../tests/scenarios.md) позволяют повторить текстовую проверку.

## Обнаруженное и исправленное

В первоначальном batch pseudocode checkpoint был указан после явного flush. При сохранении checkpoint через ORM в ручной transaction он мог остаться unflushed и потеряться при clear. Порядок исправлен и сверён с EntityManager::wrapInTransaction: ORM checkpoint изменяется до final flush, DBAL update допускается только в той же transaction. Дополнительно уточнено отличие retry sequence от broker redelivery и CommandTester helper от нового test-case helper.

## Границы результата

В этой работе не запускались настоящее Symfony приложение, integration DB/broker, Panther/Playwright или live provider; проектное принятие выполняется при использовании скилла в конкретных приложениях. Документальная проверка API не является сертификатом для всех версий optional bundles.

Подготовлены файлы skill, код проверки/сборки, CI workflow и локальные release archives. GitHub tag/release, внешняя публикация, deployment и их CI не выполнялись.

## Расширение второго донора

Добавлены 13 выбранных skills fatonh/symfony-skills и учтены все 19 файлов этих каталогов, включая 6 PHP templates/examples. Они не скопированы в исполняемые assets: guidance адаптирован, hashes и обе MIT notices сохранены. Имя doctrine-migrations встречается в обоих репозиториях и не дедуплицируется без source ID.

До расширения агент прочитал текущий skill и зафиксировал адресные пробелы B1–B5: Console long-run/input lifecycle, RFC 9457/security error paths, JWT lifecycle, module discovery и PATCH presence. После расширения независимый агент предложил конкретные решения для всех пяти задач, используя нужные references. Это проверка текстового покрытия, не сравнительный benchmark и не Symfony runtime evidence.

Во время нового ревью исправлена несуществующая Console signals URL и явно разделены baseline 8.0 input alternatives и Console resolver API 8.1. Дополнительно ссылки Symfony 8.0 во всех references сверены с pinned docs source tree; пути к multiple buses, profiler и Cache приведены к существующим страницам. Все локальные links и routing проверены validator.
