# Symfony Best Practices Skill

Версия **0.1.0** — единый эталонный Agent Skill для работы с **Symfony 8.x** в наших проектах. Проверенная базовая линия: Symfony 8.0 / PHP 8.4+. Конкретные minor-версии, пакеты и команды всегда определяются по проекту.

[SKILL.md](skills/symfony-best-practices/SKILL.md) — короткий вход; 12 справочников покрывают все 29 выбранных донорских скиллов: рабочий процесс и качество, конфигурацию, архитектуру, Doctrine, миграции, тесты, Messenger, Scheduler, формы/безопасность, кеш и Twig.

## Установка

Скопируйте **весь** каталог `skills/symfony-best-practices/` в каталог skills используемого агента. Для проекта с Agent Skills:

```text
<project>/.agents/skills/symfony-best-practices/
    SKILL.md
    agents/openai.yaml
    references/
    LICENSE
    THIRD_PARTY_NOTICES.md
    SOURCES.md
    sources.json
```

Каталог назначения должен отсутствовать либо обновляться по установленной в проекте процедуре: не затирайте чужую версию. В архиве релиза верхний каталог называется `symfony-best-practices/`; его можно целиком разместить в `.agents/skills/`. Для глобальной установки Codex используется `${CODEX_HOME:-$HOME/.codex}/skills/`. Для другого агента используйте его поддерживаемый каталог Agent Skills; загрузка и UI зависят от клиента.

Вызов: `$symfony-best-practices`, например: «Используй $symfony-best-practices для ревью этого Symfony endpoint». Метаданные Codex допускают обычное автоматическое обнаружение. Python нужен только для разработки/проверки пакета, не для использования скилла.

## Как применяется эталон

Агент определяет версии и runtime, использует проектные make/Composer/container wrappers и читает только нужные справочники. Скилл учитывает текущую архитектуру: CQRS, порты, отдельные buses и стратегии вводятся по задаче. Проверки выбираются по измененному поведению; реальные БД, очереди и браузеры проверяются там, где от них зависит результат.

Скилл не устанавливает проектные зависимости и не запускает миграции, очистку кеша, fixture resets или общие workers автоматически. Изменения выполняются в пределах задачи и выбранного окружения. Работа с проектом вне Symfony 8.x не означает согласованный upgrade.

## Происхождение

Донор: [dev-toolings/superpowers-symfony](https://github.com/dev-toolings/superpowers-symfony), revision `459bcd0b7742e2f636374daa3552d9574527410e`.

[Карта 29 доноров и изменений](skills/symfony-best-practices/SOURCES.md), [58 хешей источников](skills/symfony-best-practices/sources.json), [обзор исправлений](docs/source-review.md). Опечатка `symfony-schedu` разрешена в `symfony-scheduler`. Полная MIT-лицензия донора входит в пакет, авторская лицензия репозитория сохранена.

## Разработка и сборка

Из корня репозитория, Python 3.11+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_release.py
```

На Windows используйте `.venv\Scripts\python.exe`. Для проверки фактических donor hashes добавьте `--upstream-dir <checkout>` к validator; checkout должен стоять на закрепленном SHA. Обычная проверка работает без сети и проверяет структуру provenance; она не скачивает upstream.

Сборка создает `dist/symfony-best-practices-0.1.0.tar.gz`, `.zip` и `SHA256SUMS`. Архив содержит только самодостаточный skill, без исходного плагина, рабочих файлов и инструментов сборки. Повторная сборка в одном toolchain дает одинаковые байты; тест проверяет состав, содержимое и контрольные суммы обоих форматов. CI повторяет validator/tests/build и сохраняет артефакты.

[Дизайн](docs/superpowers/specs/2026-10-13-symfony-skill-0.1.0-design.md) · [План](docs/superpowers/plans/2026-10-13-symfony-skill-0.1.0.md) · [Результаты проверок](docs/verification-0.1.0.md) · [Changelog](CHANGELOG.md)

Структурная и сценарная проверки не доказывают работу всех рекомендаций в реальном приложении Symfony. Применение в проектах требует их обычных CI и интеграционных проверок.

## Лицензия

[MIT](LICENSE). Донорский copyright и полный notice сохранены в [THIRD_PARTY_NOTICES.md](skills/symfony-best-practices/THIRD_PARTY_NOTICES.md).
