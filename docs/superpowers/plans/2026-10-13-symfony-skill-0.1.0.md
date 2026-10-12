# Symfony Skill 0.1.0 Implementation Plan

**Goal:** Собрать проверяемый переносимый skill для Symfony 8.x на основе 29 выбранных доноров.
**Architecture:** Один короткий вход и 12 условно загружаемых справочников. Provenance и лицензии входят в пакет; проверка и упаковка живут в репозитории.
**Tech Stack:** Markdown, Agent Skills YAML, Python 3.11+, PyYAML 6.0.3, unittest, GitHub Actions.

## 1. Источники и тестовый контракт

- [x] Сверить все 29 каталогов на pinned donor SHA и изучить SKILL.md и reference.md каждой выбранной темы.
- [x] Сверить спорные места с Symfony 8.0, Doctrine ORM, Foundry и UX TwigComponent.
- [x] Запустить сценарии без нового skill, сохранить фактический результат без выдуманного RED.
- [x] Создать tests/test_package.py с subprocess-проверками validator и builder; запустить `python3 -m unittest discover -s tests -v` до реализации. Ожидаются failures из-за отсутствующих команд.

## 2. Канонический skill

- [x] Создать skills/symfony-best-practices/SKILL.md, agents/openai.yaml, 12 references, LICENSE, THIRD_PARTY_NOTICES.md, SOURCES.md и sources.json.
- [x] Добавить Symfony 8.x/PHP 8.4 baseline, runtime discovery, version gates и ограничение проверок по задаче.
- [x] Зафиксировать donor SHA, SHA-256 58 материалов и LICENSE, соответствие каждому reference, opt-in architecture decisions и исправления источников.

## 3. Validator и release builder

- [x] Реализовать scripts/validate.py: YAML schema, version, ссылки и routing, provenance coverage/hashes/license, запрет symlink и незавершенных placeholders.
- [x] Реализовать scripts/build_release.py: allowlist только канонического skill, validate-before-build, стабильные порядок/mode/timestamp и SHA256SUMS.
- [x] Прогнать негативные тесты: версия, отсутствующий reference, сломанная ссылка, path escape, symlink, потерянный donor, malformed SHA/hash, отсутствующий notice; проверить два независимых rebuild byte-for-byte.

## 4. Документация и CI

- [x] Обновить README.md: установка всего каталога и запуск `$symfony-best-practices`, команды разработки пакета и границы совместимости.
- [x] Создать VERSION, CHANGELOG.md, requirements-dev.txt, .github/workflows/validate.yml; игнорировать dist, venv и bytecode.
- [x] Записать docs/source-review.md и docs/verification-0.1.0.md с фактическими результатами.

## 5. Приемка

- [x] Повторить сценарии агентом с новым skill; проверить прочтенные references и решения.
- [x] Выполнить validator, unittest и skill-creator quick_validate.py; проверить archive inventory и SHA256SUMS.
- [x] Выполнить `git diff --check`, проверить diff/coverage и первичный checkout. Передать пользователю skill, архив и результаты проверок.
