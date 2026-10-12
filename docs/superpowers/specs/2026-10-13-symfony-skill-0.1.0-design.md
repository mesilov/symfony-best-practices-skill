# Symfony Best Practices 0.1.0

## Назначение и целевая линия

Единый переносимый Agent Skill для разработки, диагностики и ревью Symfony 8.x в наших проектах. Начальная проверенная линия — Symfony 8.0 и PHP 8.4+. Конкретные компоненты, их minor-версии и инструменты определяются по composer.lock и проектным инструкциям. Пример из документации другой minor-версии не становится разрешенным API автоматически.

## Выбранная структура

Канонический пакет: skills/symfony-best-practices/. SKILL.md содержит триггеры, общие ограничения и таблицу маршрутизации; двенадцать references/*.md раскрывают отдельные темы. agents/openai.yaml обеспечивает обычное автоматическое обнаружение Codex. Пакет самодостаточен и не требует MCP, плагина Superpowers, сети, глобального PHP или конкретного Docker service name.

Альтернативы: 29 отдельных skills сохраняют донорскую структуру, но дублируют общие правила и усложняют сопровождение. Один монолитный SKILL.md постоянно загружает все темы в контекст. Короткий единый вход со справочниками соответствует запросу на общий эталон и оставляет детали условными.

## Темы и происхождение

1. workflow-and-quality: bootstrap-check, daily-workflow, effective-context, quality-checks.
2. configuration: config-env-parameters.
3. architecture: controller-cleanup, cqrs-and-handlers, interfaces-and-autowiring, ports-and-adapters, strategy-pattern, value-objects-and-dtos.
4. doctrine-modeling: doctrine-relations, doctrine-transactions.
5. doctrine-performance: doctrine-batch-processing, doctrine-fetch-modes.
6. migrations: doctrine-migrations.
7. testing: doctrine-fixtures-foundry, e2e-panther-playwright, functional-tests, tdd-with-phpunit, test-doubles-mocking.
8. messenger: symfony-messenger, messenger-retry-failures.
9. scheduler: symfony-scheduler.
10. security-and-forms: form-types-validation, symfony-voters, rate-limiting.
11. cache: symfony-cache.
12. twig-components: twig-components.

Донор dev-toolings/superpowers-symfony закреплен на 459bcd0b7742e2f636374daa3552d9574527410e. Читаются SKILL.md и reference.md каждого выбранного каталога. Опечатка symfony-schedu в запросе разрешается в существующий symfony-scheduler. Карта всех 29 доноров, SHA-256 58 Markdown-файлов, полный MIT notice и список изменений входят в устанавливаемый пакет.

## Контракт работы агента

Сначала определить runtime и версии, затем читать справочники по задаче. Использовать существующие make/composer/container wrappers. Сохранять HTTP/CLI контракт при рефакторинге. CQRS, отдельные слои, интерфейсы, tags и DTO выбираются по задаче и текущей архитектуре, а не внедряются повсеместно. Новое поведение проверять тестом; базу, миграции, concurrency и очереди проверять на соответствующем уровне. В отчете различать выполненные и пропущенные проверки.

Диагностика не означает разрешение на cache:clear, установку зависимостей, запуск migrations/fixtures, очередей или изменение production. Конкретные изменения выполняются в рамках запроса пользователя; неизвестные общие/production ресурсы сначала идентифицируются. Секреты не выводятся в отчеты и логи.

## Проверка и упаковка

Python validator проверяет метаданные, локальные ссылки, routing, полное покрытие доноров, provenance и лицензии. Unittest проверяет валидный пакет и поврежденные варианты. Детерминированный builder создает tar.gz, zip и SHA256SUMS только из канонического каталога skill. CI повторяет эти проверки и публикует build artifacts.

Сценарные проверки агентом оценивают выбор runtime и minor-version API, Doctrine batch/rollback, Messenger redelivery/retry, migrations, изоляцию cache/Twig и границы доказательств. Это проверка рекомендаций; исполнение в реальном Symfony приложении отдельным условием приемки не является.

## Критерии готовности

- Один skill с именем symfony-best-practices и metadata.version 0.1.0; 12 доступных справочников.
- Все 29 доноров представлены, лицензии сохранены, SHA и hashes зафиксированы.
- Нет обязательной зависимости от донорского symfony-context, Superpowers, конкретного container service или MCP.
- Исправлены противоречия retry, закрытого EntityManager, конкурентной идемпотентности, migration rollback и browser DB isolation.
- Validator, негативные тесты, проверка воспроизводимости архивов и сценарная проверка проходят; ограничения проверки явно описаны.
