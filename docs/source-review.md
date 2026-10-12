# Обзор источников 0.1.0

Дата проверки: 2026-10-13. Первый донор закреплен на `459bcd0b7742e2f636374daa3552d9574527410e`, второй fatonh/symfony-skills — на `ecebbb967b4ae7006694aec9b32ec071c60d84d7`. [Полная карта](../skills/symfony-best-practices/SOURCES.md) содержит 42 repository-qualified skill entries и 77 файлов (71 Markdown и 6 supporting PHP examples/templates). Скилл переработан под Symfony 8.x, проверенная базовая линия — 8.0 / PHP 8.4+.

Общие донорские рекомендации сохранены: тонкие entry points, явные зависимости, Doctrine owning sides, ограниченные batch loops, миграции через versioned files, изоляция тестов, идемпотентные handlers, validation/authorization и кеш с определенным freshness contract. Повторяющиеся инструкции объединены. Примеры API другой minor-версии не перенесены как универсально доступные.

## Уточнения и исправления

| ID | Донорское правило / риск | Решение в эталоне |
| --- | --- | --- |
| O1 | bootstrap-check заявляет read-only, но предлагает cache:clear и DB setup | Диагностика отделена от изменения state; окружение подтверждается до boot/DB операций |
| O2 | daily-workflow автоматически предлагает pull, миграции и fixtures | Текущий checkout/runtime и конкретный запрос определяют операции; destructive reset не является ежедневной проверкой |
| O3 | controller-cleanup, DI, CQRS, ports задают жесткие line counts и архитектурные формы | Ответственность и контракт важнее количества строк; CQRS/interfaces/layers/XML вводятся по реальной потребности |
| O4 | Recoverable exception рекомендована для transient failures при небольшом max_retries; retryDelay помечен 8.1+ | На 8.0 recoverable игнорирует max_retries; bounded retry использует обычную retryable ошибку. retryDelay уже доступен |
| O5 | После rollback предлагается clear и повторный find на том же EM | После закрытия нужен fresh manager и повторное получение зависимых repositories; clear не открывает manager |
| O6 | Проверка status перед обработкой приведена как идемпотентность | Unique/atomic claim плюс recovery; отдельно provider idempotency и crash/reconciliation; outbox при необходимой atomic publication |
| O7 | down всегда должен быть обратным up и назван working rollback | Обратимость доказывается данными; irreversible явно помечается, dry-run не доказывает recovery/locks/runtime |
| O8 | Foundry v2 объявлен всегда возвращающим real objects, proxy helpers запрещены | Поведение зависит от типа factory/version; v2.2 proxy code сохраняется, deprecation v2.7 и extension/reset v2.9 gated |
| O9 | Panther предлагается изолировать DAMA rollback и безусловно отключать sandbox | Отдельный server process требует committed fixtures/cleanup или isolated resettable DB; sandbox не отключается автоматически |
| O10 | Scheduler требует только один consumer и смешивает stateful/lock с защитой heavy job | Координация consumers допустима; emission lock, job overlap, catch-up и business completion разделены |
| O11 | Cache предлагает универсальные tags/hash/expiry и описывает ранний recompute как stale zero-latency | Выбор зависит от freshness/coherence; tenant/user/permissions входят в контракт ключа, invalidation после commit, topology проверяется |
| O12 | Несколько capabilities названы 8.1+ как группа без точного package/signature | Используется проверенный 8.0 baseline; новый API сверяется по конкретному component/minor и owning class |

| O13 | console-commands запрещает supported Command/execute, named arguments и требует 8.1 method form | Сохраняется supported классическая форма при необходимости; 8.0 invokable и MapInput покрыты, новые method APIs gated по installed minor |
| O14 | bundle-organization задает обязательную module-first структуру и широкий Domain exclude | Flat layout допустим, app modules не становятся bundles; из discovery исключаются POJOs, не все реальные domain services |
| O15 | problem-details помещает HTTP status/type в domain exception | Mapping выполняется в HTTP adapter; pure domain не получает Symfony/HTTP dependencies |
| O16 | problem-details требует все поля и копирует HttpException message, теряет headers | RFC optional members соблюдены, 4xx тоже санитизируются, protocol headers сохраняются; formatter scoped к API и security paths |
| O17 | dto-and-validation считает MapQueryString failures 422 и ожидает top-level ValidationFailedException | На baseline MapQueryString по умолчанию 404; статус выбран явно, exception/cause chain учитывается |
| O18 | DTO правила исключают nullable input и смешивают JSON decode depth с object MaxDepth | PATCH missing/null разделены, actual hydration/PropertyInfo/cascade проверяются; decoder depth и object graph controls различаются |
| O19 | JWT назван неотзываемым; stateless APIs объявлены не нуждающимися в CSRF | Supported server-side blocklist/revocation проверяются; cookie credentials требуют CSRF analysis независимо от stateless |
| O20 | doctrine-orm требует UUID v7, string enums, private constructor и universal orphanRemoval | Существующий ID/domain contract сохраняется; int-backed enums допустимы, ownership и lifecycle определяют mapping |
| O21 | query-optimization обещает двухзапросный Paginator, constant-time keyset и JDBC batching | Проверяется фактический query plan/count и stable seek tuple; ORM memory batching не обещает multi-row SQL batching |
| O22 | messenger-async/transactional-patterns приравнивают stamp к atomic outbox, flush/postFlush к commit | Same physical connection/transaction и dispatch timing проверяются; stamp deferral и durable outbox разделены |

Дополнительно усилены escaping в Twig, защита персонального HTTP cache, DB unique constraint поверх UniqueEntity и отличие RateLimiter от edge DoS protection. Не переносились донорские plugin hooks, slash commands, agents, runner-selection и остальные невыбранные skills.

## Первичные источники

- [Symfony 8.0 docs](https://github.com/symfony/symfony-docs/tree/eea05cbfe063b9cf99afaf303b8cad76757f43bb): setup, best practices, console/testing, configuration, forms, Messenger, Scheduler, Cache, RateLimiter. В setup указана базовая PHP 8.4+; в Messenger явно описан forced retry.
- [Doctrine ORM 3.5.0](https://github.com/doctrine/orm/tree/6deec3655ba3e8f15280aac11e264225854d2369): batch processing, transactions/concurrency и EntityManager::wrapInTransaction. Полный callback выполняется перед final flush/commit; при неуспехе manager закрывается.
- [Doctrine Migrations 3.9.0 implicit commits](https://github.com/doctrine/migrations/blob/3.9.0/docs/en/explanation/implicit-commits.rst) и [AbstractMigration](https://github.com/doctrine/migrations/blob/3.9.0/src/AbstractMigration.php): nontransactional DDL и явная необратимость.
- [Foundry docs](https://github.com/zenstruck/foundry/blob/8b6feea05407f2edf4970312119167cfd9828e10/docs/index.rst): real/proxy factories, deprecation, reset и PHPUnit extension version gates.
- [UX TwigComponent docs](https://github.com/symfony/ux-twig-component/blob/a1f1765482f92705f074ded029d33165dcf7a05f/doc/index.rst): public props, mount и порядок hydration.

- [Lexik 3.x token invalidation](https://github.com/lexik/LexikJWTAuthenticationBundle/blob/8d614e1406ffabd36b1de5d3560e2dcc9db75e79/Resources/doc/11-invalidate-token.rst), [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html) и [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html): blocklist/logout, HTTP error semantics и verification/trust.

## Проверка и ее границы

SHA-256 всех 77 файлов фактически сверяются validator с обоими pinned checkout через повторяемые --upstream ID=PATH. Legacy --upstream-dir проверяет первый checkout. Обычный offline validator проверяет форму provenance и лицензий, а не скачивает upstream. Обе исходные MIT-лицензии воспроизведены полностью и входит в оба архива; документы первичных источников не копируются в пакет.

Сценарное ревью обнаружило неоднозначный порядок checkpoint/flush в новом batch pseudocode: теперь ORM checkpoint изменяется до final flush, а прямой DBAL update явно выполняется внутри той же transaction. Сценарные решения и структурный validator не доказывают поведение каждого API в реальном приложении; такую проверку выполняют проектные тесты/CI при применении.
