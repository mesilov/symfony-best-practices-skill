# Symfony Best Practices Skill

Версия **0.1.0** — единый эталонный Agent Skill для работы с **Symfony 8.x** в наших проектах. Официальная документация сверена на 2026-10-15 по линии Symfony 8.1 / PHP 8.4+; важные различия с 8.0 отмечены отдельно. Конкретные minor-версии, пакеты и команды всегда определяются по проекту.

[SKILL.md](skills/symfony-best-practices/SKILL.md) — короткий вход; 31 справочник покрывает 42 выбранных донорских скилла из двух репозиториев и 40 страниц официальной документации (43 исходные ссылки) и физически разложены по семи смысловым группам.

| Группа | Темы |
| --- | --- |
| workflow | Runtime, качество, конфигурация, тесты, логи/ошибки, deployment/performance, AI Mate |
| architecture | Слои/DDD/CQRS, bundles, Console, DI/events/Kernel, Workflow/Lock, utilities, AI/MCP |
| http | Routing/HttpKernel, REST/RFC 9457, DTO/forms/validation, sessions, Serializer, HttpClient/webhooks |
| data | Doctrine ORM/транзакции, запросы/batches, миграции, кеш |
| async | Messenger, Scheduler, Mailer/Notifier |
| security | Authentication, JWT, authorization/voters/rate limiting |
| presentation | Twig, Translation, UX components |

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

Доноры: [dev-toolings/superpowers-symfony](https://github.com/dev-toolings/superpowers-symfony), revision `459bcd0b7742e2f636374daa3552d9574527410e` — 29 скиллов; [fatonh/symfony-skills](https://github.com/fatonh/symfony-skills), revision `ecebbb967b4ae7006694aec9b32ec071c60d84d7` — еще 13.

[Карта 42 доноров и изменений](skills/symfony-best-practices/SOURCES.md), [77 донорских и 40 документальных source hashes](skills/symfony-best-practices/sources.json), [обзор исправлений](docs/source-review.md). Опечатка `symfony-schedu` разрешена в `symfony-scheduler`. Полные MIT-лицензии обоих доноров входят в пакет, авторская лицензия репозитория сохранена.

Официальные источники: [Symfony Docs, ветка 8.1](https://github.com/symfony/symfony-docs/tree/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe) и [Symfony AI](https://github.com/symfony/ai/tree/5ad77d9418152e61e5b2b2bbb29d070a07fc2a67). [Карта всех 40 страниц и ключевых дополнений](docs/official-documentation-review-2026-10-15.md). Ссылки `current` подвижны: пакет хранит проверенные revisions/hashes, а агент сверяет installed API. Mate, MCP Bundle и AI Bundle имеют собственные версии и подключаются по задаче.

## Разработка и сборка

Из корня репозитория, Python 3.11+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_release.py
```

На Windows используйте `.venv\Scripts\python.exe`. Для сверки всех фактических source hashes передайте четыре checkout на закрепленных SHA из sources.json:

```sh
.venv/bin/python scripts/validate.py \
  --upstream superpowers-symfony=<first-checkout> \
  --upstream symfony-skills=<second-checkout> \
  --docs-checkout symfony-docs=<symfony-docs-8.1-checkout> \
  --docs-checkout symfony-ai=<symfony-ai-checkout>
```

Проверка старого первого донора через `--upstream-dir <checkout>` также поддерживается. Обычная проверка работает без сети и проверяет структуру provenance; она не скачивает upstream.

Сборка создает `dist/symfony-best-practices-0.1.0.tar.gz`, `.zip` и `SHA256SUMS`. Архив содержит только самодостаточный skill, без исходного плагина, рабочих файлов и инструментов сборки. Повторная сборка в одном toolchain дает одинаковые байты; тест проверяет состав, содержимое и контрольные суммы обоих форматов. CI повторяет validator/tests/build и сохраняет артефакты.

[Дизайн](docs/superpowers/specs/2026-10-13-symfony-skill-0.1.0-design.md) · [План](docs/superpowers/plans/2026-10-13-symfony-skill-0.1.0.md) · [Результаты проверок](docs/verification-0.1.0.md) · [Changelog](CHANGELOG.md)

Структурная и сценарная проверки не доказывают работу всех рекомендаций в реальном приложении Symfony. Применение в проектах требует их обычных CI и интеграционных проверок.

## Лицензия

[MIT](LICENSE) для собственного пакета. Symfony Docs использованы как справочный источник под CC BY-SA 3.0; текст руководства и его примеры не включены. Полные MIT notices двух доноров и Symfony AI сохранены в [THIRD_PARTY_NOTICES.md](skills/symfony-best-practices/THIRD_PARTY_NOTICES.md).
