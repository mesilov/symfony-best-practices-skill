# Symfony Best Practices Skill

**Единый Agent Skill для разработки, диагностики и ревью Symfony 8.x приложений.** Помогает агенту выбрать подходящие API и архитектурные решения, реализовать изменение по правилам проекта и проверить результат.

Версия **0.1.0** · **7 блоков** · **31 тематический справочник**.

Инструкции для агента — [SKILL.md](skills/symfony-best-practices/SKILL.md) и `references/` — написаны на английском. Этот README на русском объясняет покрытие, применение и установку. Короткий SKILL.md направляет агента к справочникам, нужным для конкретной задачи.

## Что охватывает

| Блок | Подсистемы и рекомендации | Справочников |
| --- | --- | ---: |
| **HTTP и API** | [Routing, Controllers и HttpKernel](skills/symfony-best-practices/references/http/routing-and-kernel.md): маршруты, аргументы, lifecycle и subrequests. [REST и RFC 9457](skills/symfony-best-practices/references/http/rest-api.md): статусы и безопасные ошибки. [DTO, Forms и Validator](skills/symfony-best-practices/references/http/validation-and-forms.md): mapping, nested validation, PATCH missing/null. [Session](skills/symfony-best-practices/references/http/sessions.md): cookies, concurrency, private cache. [Serializer](skills/symfony-best-practices/references/http/serializer.md): поля, группы и границы данных. [HttpClient и Webhook](skills/symfony-best-practices/references/http/http-client-and-webhooks.md): timeout/retry, подписи и replay. | 6 |
| **Данные и кеш** | [Doctrine ORM](skills/symfony-best-practices/references/data/doctrine-modeling.md): relations, transactions и locking. [Запросы и batches](skills/symfony-best-practices/references/data/doctrine-performance.md): N+1, pagination, память и checkpoints. [Migrations](skills/symfony-best-practices/references/data/migrations.md): SQL, совместимость и recovery. [Cache](skills/symfony-best-practices/references/data/cache.md): pools, TTL, tags, invalidation и tenant/user isolation. | 4 |
| **Фоновые задачи и доставка** | [Messenger](skills/symfony-best-practices/references/async/messenger.md): routing, retries, failure transport, idempotency и outbox. [Scheduler](skills/symfony-best-practices/references/async/scheduler.md): расписания, catch-up, emission и job overlap. [Mailer и Notifier](skills/symfony-best-practices/references/async/mailer-and-notifier.md): transport, serializable context, очередь и доставка. | 3 |
| **Безопасность** | [Authentication](skills/symfony-best-practices/references/security/authentication.md): users/providers, firewalls, passwords, sessions и CSRF. [JWT](skills/symfony-best-practices/references/security/jwt.md): проверка токена, refresh и revocation. [Authorization и RateLimiter](skills/symfony-best-practices/references/security/authorization-and-rate-limiting.md): voters, resource/tenant access и ограничения запросов. | 3 |
| **Архитектура и компоненты** | [Services и domain](skills/symfony-best-practices/references/architecture/architecture.md): use cases, DTO/value objects, CQRS, ports/adapters и стратегии по необходимости. [Модули и bundles](skills/symfony-best-practices/references/architecture/bundle-organization.md): границы и discovery. [Console](skills/symfony-best-practices/references/architecture/console-commands.md): input, validation, exit codes, cancellation/resume. [Container, Kernel и Events](skills/symfony-best-practices/references/architecture/container-and-events.md): DI, autowiring и listeners. [Workflow и Lock](skills/symfony-best-practices/references/architecture/workflow-and-locks.md): transitions, concurrency и leases. [Filesystem, UID, YAML, ExpressionLanguage](skills/symfony-best-practices/references/architecture/framework-utilities.md): применение и границы доверия. [AI Bundle и MCP Bundle](skills/symfony-best-practices/references/architecture/ai-integration.md): tools, auth/authz, data trust и budgets. | 7 |
| **Представление** | [Twig и Translation](skills/symfony-best-practices/references/presentation/twig-and-translation.md): templates, escaping, locale, ICU и cache variants. [UX Twig Components](skills/symfony-best-practices/references/presentation/twig-components.md): props, hydration и lifecycle. | 2 |
| **Разработка и эксплуатация** | [Runtime и качество](skills/symfony-best-practices/references/workflow/workflow-and-quality.md): версии, проектные runners и quality gates. [Configuration](skills/symfony-best-practices/references/workflow/configuration.md): env, typed injection и secrets. [Testing](skills/symfony-best-practices/references/workflow/testing.md): PHPUnit, kernel/functional tests, Foundry, Panther/Playwright и изоляция. [Logging и ошибки](skills/symfony-best-practices/references/workflow/logging-and-errors.md): channels, redaction и error pages. [Deployment и performance](skills/symfony-best-practices/references/workflow/deployment-and-performance.md): release lifecycle, workers, OPcache и HTTP cache. [AI Mate](skills/symfony-best-practices/references/workflow/ai-mate.md): CLI для контекста разработки. | 6 |

Общие правила проходят через все блоки: явные контракты, проверка установленных версий, авторизация и tenant boundaries, безопасная работа с секретами, конкурентная обработка и проверяемые результаты.

## Как агент применяет скилл

Агент читает инструкции репозитория, `composer.json`/`composer.lock`, релевантные конфигурацию, код и тесты. Определяет проектный PHP/Console/Composer/test runner и выбирает справочники под задачу. Затем фиксирует ожидаемое поведение, добавляет подходящий regression/acceptance test, реализует изменение и запускает необходимые проверки.

Например, задача **добавить защищённый `POST /api/orders`** затронет:

1. **Контекст проекта:** установленный Symfony, похожие endpoints, формат ответов/ошибок и тестовый runner.
2. **HTTP/API и Security:** маршрут, JSON input, validation, authentication, доступ пользователя/tenant и выходные поля.
3. **Данные:** существующий use case/repository, transaction и ограничения БД, если заказ сохраняется.
4. **Проверки:** успешное создание, invalid input, отсутствие credentials, отказ в доступе и сохранённое состояние.
5. **Отчёт:** изменённый контракт, выполненные команды и результаты, пропущенные или заблокированные проверки.

К остальным темам агент обращается по задаче: отправка уведомления подключит Mailer/Notifier и при необходимости Messenger; внешний API — HttpClient. Для уточнения незнакомого API он сверяет installed code/help или документацию соответствующей версии.

### Примеры запросов

```text
Используй $symfony-best-practices. Добавь POST /api/orders по соглашениям проекта,
с проверкой доступа, validation и функциональными тестами.
```

```text
Используй $symfony-best-practices. Найди причину N+1 в списке заказов,
предложи исправление и проверь число запросов на тестовой БД.
```

```text
Используй $symfony-best-practices. Проведи ревью Messenger handler:
retries, concurrent duplicates, provider idempotency и поведение после сбоя.
```

## Совместимость и принципы

- **Symfony 8.x.** Официальная документация сверена на **2026-10-15** по линии **8.1 / PHP 8.4+**. Важные отличия 8.0 отмечены отдельно; фактические версии берутся из проекта.
- **Версии компонентов.** Doctrine, Foundry, UX, Lexik, Symfony AI и их bridges проверяются независимо от minor-версии Symfony. Mate, AI Bundle и MCP Bundle подключаются по задаче.
- **Архитектура проекта.** Скилл поддерживает текущие соглашения. CQRS, DDD, interfaces, ports и отдельные buses вводятся при обоснованной необходимости.
- **Окружение и операции.** Используются проектные make/Composer/container wrappers. Миграции, fixture resets, cache clearing и обработка общих очередей выполняются в рамках задачи и выбранного окружения. Работа с другой версией Symfony сама по себе не разрешает upgrade.
- **Проверка результата.** Скилл задаёт рекомендации агенту; выполнение подтверждают тесты, CI и проверки проекта. Локальный тест, доставка через реальный provider и deployment имеют разные границы доказательности.

## Установка

Скопируйте **весь** каталог `skills/symfony-best-practices/` в каталог skills используемого агента. Для проекта с поддержкой такого расположения Agent Skills:

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

В архиве верхний каталог называется `symfony-best-practices/`; его можно целиком разместить в `.agents/skills/`. Обновляйте существующую установку по процедуре проекта, сохраняя локальные изменения. Для глобальной установки Codex используется `${CODEX_HOME:-$HOME/.codex}/skills/`. Для другого агента выберите его поддерживаемый каталог; загрузка и UI зависят от клиента.

Явный вызов: `$symfony-best-practices`. Метаданные Codex также допускают автоматический выбор скилла. Python нужен для разработки и проверки пакета; сам skill состоит из Markdown, metadata и справочников.

## Источники и адаптация

Покрытие собрано из **42 выбранных донорских скиллов** и **40 страниц официальной документации** — всех 43 заданных URL, включая три дополнительных Security anchors.

| Источник | Материалы |
| --- | --- |
| [dev-toolings/superpowers-symfony](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e) | 29 skills / 58 Markdown files |
| [fatonh/symfony-skills](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7) | 13 skills / 19 files, включая PHP templates/examples |
| [Symfony Docs 8.1](https://github.com/symfony/symfony-docs/tree/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe) | 37 framework pages |
| [Symfony AI](https://github.com/symfony/ai/tree/5ad77d9418152e61e5b2b2bbb29d070a07fc2a67) | 3 AI pages |

Повторения объединены, спорные и зависящие от версии рекомендации уточнены. Пакет хранит закреплённые revisions, paths, hashes и лицензии; подвижные ссылки `current` служат исходными адресами проверки.

- [Карта доноров и справочников](skills/symfony-best-practices/SOURCES.md).
- [Manifest: 77 донорских и 40 документальных source hashes](skills/symfony-best-practices/sources.json).
- [Обзор исправлений источников](docs/source-review.md).
- [Карта официальной документации и дополнений](docs/official-documentation-review-2026-10-15.md).

## Разработка и сборка

Из корня репозитория, Python 3.11+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_release.py
```

На Windows используйте `.venv\Scripts\python.exe`. Чтобы сверить фактические HEAD и source hashes, передайте checkout каждого источника на закреплённом SHA из `sources.json`:

```sh
.venv/bin/python scripts/validate.py \
  --upstream superpowers-symfony=<first-checkout> \
  --upstream symfony-skills=<second-checkout> \
  --docs-checkout symfony-docs=<symfony-docs-8.1-checkout> \
  --docs-checkout symfony-ai=<symfony-ai-checkout>
```

Legacy `--upstream-dir <checkout>` проверяет первого донора. Обычный validator работает без сети: проверяет структуру, routing, покрытие и notices, не скачивая источники.

Сборка создаёт `dist/symfony-best-practices-0.1.0.tar.gz`, `.zip` и `SHA256SUMS`. Архив содержит самодостаточный skill. Повторные сборки в одном toolchain проверяются побайтово; CI workflow выполняет validator/tests/build и сохраняет артефакты. Фактически выполненные проверки и их границы описаны в [verification](docs/verification-0.1.0.md).

[Дизайн](docs/superpowers/specs/2026-10-13-symfony-skill-0.1.0-design.md) · [План](docs/superpowers/plans/2026-10-13-symfony-skill-0.1.0.md) · [Changelog](CHANGELOG.md)

## Лицензия

[MIT](LICENSE) для собственного пакета. Symfony Docs использованы как справочный источник под CC BY-SA 3.0; текст руководства и его примеры не включены. Полные MIT notices двух доноров и Symfony AI сохранены в [THIRD_PARTY_NOTICES.md](skills/symfony-best-practices/THIRD_PARTY_NOTICES.md).
