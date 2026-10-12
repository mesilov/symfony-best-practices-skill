# Symfony Best Practices 0.1.0

## Назначение и целевая линия

Единый переносимый Agent Skill для разработки, диагностики и ревью Symfony 8.x в наших проектах. Начальная проверенная линия — Symfony 8.0 и PHP 8.4+. Конкретные компоненты, их minor-версии и инструменты определяются по composer.lock и проектным инструкциям. Пример из документации другой minor-версии не становится разрешенным API автоматически.

## Выбранная структура

Канонический пакет: skills/symfony-best-practices/. SKILL.md содержит триггеры, общие ограничения и таблицу маршрутизации; 18 references/<group>/*.md в семи смысловых группах раскрывают отдельные темы. agents/openai.yaml обеспечивает обычное автоматическое обнаружение Codex. Пакет самодостаточен и не требует MCP, плагина Superpowers, сети, глобального PHP или конкретного Docker service name.

Альтернативы: 29 отдельных skills сохраняют донорскую структуру, но дублируют общие правила и усложняют сопровождение. Один монолитный SKILL.md постоянно загружает все темы в контекст. Короткий единый вход со справочниками соответствует запросу на общий эталон и оставляет детали условными.

## Темы и происхождение

1. workflow: runtime/quality, configuration, tests/fixtures/browser isolation.
2. architecture: services/domain/DI/CQRS/VOs, modules/bundles, Console input/lifecycle.
3. http: REST/RFC 9457 и DTO/validation/forms, включая PATCH presence.
4. data: ORM/relations/transactions, queries/batches, migrations, cache.
5. async: Messenger/retries/outbox и Scheduler.
6. security: authentication/firewalls, JWT lifecycle, authorization/voters/rate limits.
7. presentation: Twig/UX components.

Донор dev-toolings/superpowers-symfony закреплен на 459bcd0b7742e2f636374daa3552d9574527410e (29 skill entries / 58 Markdown files). fatonh/symfony-skills закреплен на ecebbb967b4ae7006694aec9b32ec071c60d84d7 (13 entries / 13 Markdown и 6 supporting PHP files). Все 42 записи сохранены с identity repository ID + name: doctrine-migrations каждого донора учитывается отдельно. Опечатка symfony-schedu разрешается в symfony-scheduler. Карта, 77 SHA-256, обе полные MIT notices и изменения входят в устанавливаемый пакет.

## Контракт работы агента

Сначала определить runtime и версии, затем читать справочники по задаче. Использовать существующие make/composer/container wrappers. Сохранять HTTP/CLI контракт при рефакторинге. CQRS, отдельные слои, интерфейсы, tags и DTO выбираются по задаче и текущей архитектуре, а не внедряются повсеместно. Новое поведение проверять тестом; базу, миграции, concurrency и очереди проверять на соответствующем уровне. В отчете различать выполненные и пропущенные проверки.

Диагностика не означает разрешение на cache:clear, установку зависимостей, запуск migrations/fixtures, очередей или изменение production. Конкретные изменения выполняются в рамках запроса пользователя; неизвестные общие/production ресурсы сначала идентифицируются. Секреты не выводятся в отчеты и логи.

## Проверка и упаковка

Python validator проверяет метаданные, локальные ссылки, routing, полное покрытие доноров, provenance и лицензии. Unittest проверяет валидный пакет и поврежденные варианты. Детерминированный builder создает tar.gz, zip и SHA256SUMS только из канонического каталога skill. CI повторяет эти проверки и публикует build artifacts.

Сценарные проверки агентом оценивают REST/problem details, auth/JWT, PATCH и Console lifecycle, а также выбор runtime и minor-version API, Doctrine batch/rollback, Messenger redelivery/retry, migrations, изоляцию cache/Twig и границы доказательств. Это проверка рекомендаций; исполнение в реальном Symfony приложении отдельным условием приемки не является.

## Критерии готовности

- Один skill с именем symfony-best-practices и metadata.version 0.1.0; 18 доступных справочников в 7 группах.
- Все 42 донорских записи представлены, лицензии сохранены, SHA и hashes зафиксированы.
- Нет обязательной зависимости от донорского symfony-context, Superpowers, конкретного container service или MCP.
- Исправлены противоречия retry, закрытого EntityManager, конкурентной идемпотентности, migration rollback и browser DB isolation.
- Validator, негативные тесты, проверка воспроизводимости архивов и сценарная проверка проходят; ограничения проверки явно описаны.
