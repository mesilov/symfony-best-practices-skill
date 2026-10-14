# Sources and adaptation decisions

Version 0.1.0, reviewed on 2026-10-15. Scope: Symfony 8.x; official documentation line 8.1 / PHP 8.4+, with explicit 8.0 compatibility notes. Installed minor/package versions govern actual application use.

## Pinned donors

- superpowers-symfony: [dev-toolings/superpowers-symfony](https://github.com/dev-toolings/superpowers-symfony), `459bcd0b7742e2f636374daa3552d9574527410e`: 29 skills / 58 Markdown files.
- symfony-skills: [fatonh/symfony-skills](https://github.com/fatonh/symfony-skills), `ecebbb967b4ae7006694aec9b32ec071c60d84d7`: 13 skills / 13 Markdown and 6 supporting PHP files.

Together: 42 source-skill entries and 77 file hashes, plus both LICENSE hashes in [sources.json](sources.json), schema version 3. Identity is repository ID + skill name: both repositories' doctrine-migrations are preserved separately. The requested symfony-schedu typo is explicitly mapped to superpowers-symfony/symfony-scheduler.

Hashes identify reviewed material; they do not prove runtime correctness. Templates/examples from the second donor were inspected and hashed, then rewritten as guidance rather than copied with placeholders. The full notices for both donors are included in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).

## Semantic groups

The 31 references live in seven directories: workflow, architecture, http, data, async, security, and presentation. Routing in [SKILL.md](SKILL.md) follows these groups; read only the references needed for a task. Overlapping donor topics share references rather than introducing duplicate instructions.

| Source | Donor skill | Consolidated reference |
| --- | --- | --- |
| superpowers-symfony | [bootstrap-check](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/bootstrap-check) | [workflow-and-quality](references/workflow/workflow-and-quality.md) |
| superpowers-symfony | [daily-workflow](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/daily-workflow) | [workflow-and-quality](references/workflow/workflow-and-quality.md) |
| superpowers-symfony | [effective-context](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/effective-context) | [workflow-and-quality](references/workflow/workflow-and-quality.md) |
| superpowers-symfony | [quality-checks](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/quality-checks) | [workflow-and-quality](references/workflow/workflow-and-quality.md) |
| superpowers-symfony | [config-env-parameters](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/config-env-parameters) | [configuration](references/workflow/configuration.md) |
| superpowers-symfony | [controller-cleanup](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/controller-cleanup) | [architecture](references/architecture/architecture.md) |
| superpowers-symfony | [cqrs-and-handlers](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/cqrs-and-handlers) | [architecture](references/architecture/architecture.md) |
| superpowers-symfony | [interfaces-and-autowiring](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/interfaces-and-autowiring) | [architecture](references/architecture/architecture.md) |
| superpowers-symfony | [ports-and-adapters](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/ports-and-adapters) | [architecture](references/architecture/architecture.md) |
| superpowers-symfony | [strategy-pattern](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/strategy-pattern) | [architecture](references/architecture/architecture.md) |
| superpowers-symfony | [value-objects-and-dtos](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/value-objects-and-dtos) | [architecture](references/architecture/architecture.md) |
| superpowers-symfony | [doctrine-relations](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-relations) | [doctrine-modeling](references/data/doctrine-modeling.md) |
| superpowers-symfony | [doctrine-transactions](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-transactions) | [doctrine-modeling](references/data/doctrine-modeling.md) |
| superpowers-symfony | [doctrine-batch-processing](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-batch-processing) | [doctrine-performance](references/data/doctrine-performance.md) |
| superpowers-symfony | [doctrine-fetch-modes](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-fetch-modes) | [doctrine-performance](references/data/doctrine-performance.md) |
| superpowers-symfony | [doctrine-migrations](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-migrations) | [migrations](references/data/migrations.md) |
| superpowers-symfony | [doctrine-fixtures-foundry](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-fixtures-foundry) | [testing](references/workflow/testing.md) |
| superpowers-symfony | [e2e-panther-playwright](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/e2e-panther-playwright) | [testing](references/workflow/testing.md) |
| superpowers-symfony | [functional-tests](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/functional-tests) | [testing](references/workflow/testing.md) |
| superpowers-symfony | [tdd-with-phpunit](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/tdd-with-phpunit) | [testing](references/workflow/testing.md) |
| superpowers-symfony | [test-doubles-mocking](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/test-doubles-mocking) | [testing](references/workflow/testing.md) |
| superpowers-symfony | [symfony-messenger](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/symfony-messenger) | [messenger](references/async/messenger.md) |
| superpowers-symfony | [messenger-retry-failures](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/messenger-retry-failures) | [messenger](references/async/messenger.md) |
| superpowers-symfony | [symfony-scheduler](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/symfony-scheduler) | [scheduler](references/async/scheduler.md) |
| superpowers-symfony | [form-types-validation](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/form-types-validation) | [validation-and-forms](references/http/validation-and-forms.md) |
| superpowers-symfony | [symfony-voters](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/symfony-voters) | [authorization-and-rate-limiting](references/security/authorization-and-rate-limiting.md) |
| superpowers-symfony | [rate-limiting](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/rate-limiting) | [authorization-and-rate-limiting](references/security/authorization-and-rate-limiting.md) |
| superpowers-symfony | [symfony-cache](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/symfony-cache) | [cache](references/data/cache.md) |
| superpowers-symfony | [twig-components](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/twig-components) | [twig-components](references/presentation/twig-components.md) |
| symfony-skills | [bundle-organization](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/bundle-organization) | [bundle-organization](references/architecture/bundle-organization.md) |
| symfony-skills | [console-commands](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/console-commands) | [console-commands](references/architecture/console-commands.md) |
| symfony-skills | [doctrine-migrations](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/doctrine-migrations) | [migrations](references/data/migrations.md) |
| symfony-skills | [doctrine-orm](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/doctrine-orm) | [doctrine-modeling](references/data/doctrine-modeling.md) |
| symfony-skills | [doctrine-query-optimization](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/doctrine-query-optimization) | [doctrine-performance](references/data/doctrine-performance.md) |
| symfony-skills | [dto-and-validation](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/dto-and-validation) | [validation-and-forms](references/http/validation-and-forms.md), [architecture](references/architecture/architecture.md) |
| symfony-skills | [jwt-authentication](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/jwt-authentication) | [jwt](references/security/jwt.md) |
| symfony-skills | [layered-architecture](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/layered-architecture) | [architecture](references/architecture/architecture.md), [bundle-organization](references/architecture/bundle-organization.md) |
| symfony-skills | [messenger-async](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/messenger-async) | [messenger](references/async/messenger.md) |
| symfony-skills | [problem-details-rfc9457](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/problem-details-rfc9457) | [rest-api](references/http/rest-api.md) |
| symfony-skills | [rest-controller-conventions](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/rest-controller-conventions) | [rest-api](references/http/rest-api.md) |
| symfony-skills | [security-authentication](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/security-authentication) | [authentication](references/security/authentication.md), [authorization-and-rate-limiting](references/security/authorization-and-rate-limiting.md) |
| symfony-skills | [transactional-patterns](https://github.com/fatonh/symfony-skills/tree/ecebbb967b4ae7006694aec9b32ec071c60d84d7/skills/transactional-patterns) | [doctrine-modeling](references/data/doctrine-modeling.md) |

## Adaptation decisions

- Use project runtime wrappers and actual installed APIs, not donor hooks/runner helpers, a fixed container name or a required MCP. Preserve authorization and evidence boundaries.
- Keep architecture conditional. Module layout, DTOs, CQRS, interfaces, service families, ID types and construction patterns follow real use-case/project needs; do not ban supported Command APIs or require method-level attributes on every 8.x version.
- Preserve pure domain boundaries: HTTP problem/status mapping lives in the HTTP adapter; authenticated JWT claims do not substitute for current tenant/resource authorization.
- Respect hydration: MapInput constructors do not run; PATCH omission and explicit null can differ; MapQueryString and MapRequestPayload have different baseline validation statuses.
- Require a fresh closed EntityManager, a flushed checkpoint in the page transaction, and real data-aware migration recovery. Outer commit is different from flush/postFlush.
- Use bounded retry policy deliberately; RecoverableMessageHandlingException forces retries on baseline. Concurrent duplicates and provider crash windows need atomic claims/idempotency/reconciliation.
- DispatchAfterCurrentBusStamp controls dispatch timing; it does not by itself establish a durable outbox or same-transaction transport write.
- Scope RFC 9457 errors to the API contract, preserve protocol headers/security handlers/HTML flows, and expose only allowlisted safe details, including 4xx.
- JWT verification, cookie CSRF, refresh rotation and access-token revocation require concrete mechanisms. Lexik's supported blocklist means access JWTs are not universally irrevocable.
- Preserve version-specific Foundry proxy/reset behavior and browser-process DB isolation. Separate scheduler emission coordination from job overlap/completion. Cache identity/freshness and Twig escaping remain explicit.

## Primary evidence and license

References link to official Symfony, Doctrine, Foundry, UX, Lexik and RFC documentation. Primary source revisions/URLs are recorded in sources.json. Online documentation is not bundled and can change; check the consuming project's installed API.

Original project work uses [LICENSE](LICENSE). Both donor MIT notices are preserved in full. Verification checks source hashes against explicitly supplied pinned checkouts; the normal offline validator checks schema, coverage, routing and notice integrity without downloading anything.

## Official documentation review

All 43 requested current URLs are represented by 40 unique pages: the Security page additionally covers the three requested anchors. The reviewed framework line is **8.1** (2026-10-15); the AI documentation is maintained in its own repository and its APIs follow installed AI package versions. Earlier 8.0 links remain compatibility evidence, not the current-line default.

- Symfony Docs contributors: [pinned 8.1 source](https://github.com/symfony/symfony-docs/tree/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe), commit `9162aaaa515256a0ceeab6b98e313e9d1dcb89fe`; [CC BY-SA 3.0](https://creativecommons.org/licenses/by-sa/3.0/).
- Symfony AI, Fabien Potencier and contributors: [pinned source](https://github.com/symfony/ai/tree/5ad77d9418152e61e5b2b2bbb29d070a07fc2a67), commit `5ad77d9418152e61e5b2b2bbb29d070a07fc2a67`; MIT.

The following is a source-to-guidance map, not a bundled copy of the manuals. Guidance is an original synthesis of API facts and project decisions; manual prose/examples are not redistributed or relicensed. See sources.json `documentation` for all original URLs/anchors, exact source paths, revisions, SHA-256 and license hashes. The validator checks every selected page and combined donor/documentation coverage.

| Official page | Addressed reference |
| --- | --- |
| [routing](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/routing.rst) | [routing-and-kernel](references/http/routing-and-kernel.md) |
| [controller](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/controller.rst) | [routing-and-kernel](references/http/routing-and-kernel.md), [validation-and-forms](references/http/validation-and-forms.md) |
| [components/http_kernel](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/components/http_kernel.rst) | [routing-and-kernel](references/http/routing-and-kernel.md) |
| [reference/configuration/kernel](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/reference/configuration/kernel.rst) | [container-and-events](references/architecture/container-and-events.md), [configuration](references/workflow/configuration.md) |
| [service_container](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/service_container.rst) | [container-and-events](references/architecture/container-and-events.md) |
| [event_dispatcher](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/event_dispatcher.rst) | [container-and-events](references/architecture/container-and-events.md) |
| [configuration](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/configuration.rst) | [configuration](references/workflow/configuration.md) |
| [templates](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/templates.rst) | [twig-and-translation](references/presentation/twig-and-translation.md), [twig-components](references/presentation/twig-components.md) |
| [doctrine](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/doctrine.rst) | [doctrine-modeling](references/data/doctrine-modeling.md), [doctrine-performance](references/data/doctrine-performance.md), [migrations](references/data/migrations.md) |
| [forms](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/forms.rst) | [validation-and-forms](references/http/validation-and-forms.md) |
| [validation](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/validation.rst) | [validation-and-forms](references/http/validation-and-forms.md) |
| [testing](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/testing.rst) | [testing](references/workflow/testing.md) |
| [session](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/session.rst) | [sessions](references/http/sessions.md) |
| [cache](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/cache.rst) | [cache](references/data/cache.md) |
| [logging](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/logging.rst) | [logging-and-errors](references/workflow/logging-and-errors.md) |
| [controller/error_pages](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/controller/error_pages.rst) | [logging-and-errors](references/workflow/logging-and-errors.md), [rest-api](references/http/rest-api.md) |
| [console](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/console.rst) | [console-commands](references/architecture/console-commands.md) |
| [mailer](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/mailer.rst) | [mailer-and-notifier](references/async/mailer-and-notifier.md) |
| [notifier](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/notifier.rst) | [mailer-and-notifier](references/async/mailer-and-notifier.md) |
| [messenger](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/messenger.rst) | [messenger](references/async/messenger.md) |
| [scheduler](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/scheduler.rst) | [scheduler](references/async/scheduler.md) |
| [serializer](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/serializer.rst) | [serializer](references/http/serializer.md) |
| [translation](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/translation.rst) | [twig-and-translation](references/presentation/twig-and-translation.md) |
| [security](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/security.rst) | [authentication](references/security/authentication.md), [authorization-and-rate-limiting](references/security/authorization-and-rate-limiting.md) |
| [security/passwords](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/security/passwords.rst) | [authentication](references/security/authentication.md) |
| [security/csrf](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/security/csrf.rst) | [authentication](references/security/authentication.md), [validation-and-forms](references/http/validation-and-forms.md) |
| [http_client](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/http_client.rst) | [http-client-and-webhooks](references/http/http-client-and-webhooks.md) |
| [webhook](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/webhook.rst) | [http-client-and-webhooks](references/http/http-client-and-webhooks.md) |
| [components/filesystem](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/components/filesystem.rst) | [framework-utilities](references/architecture/framework-utilities.md) |
| [components/uid](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/components/uid.rst) | [framework-utilities](references/architecture/framework-utilities.md) |
| [components/yaml](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/components/yaml.rst) | [framework-utilities](references/architecture/framework-utilities.md) |
| [expression_language](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/expression_language.rst) | [framework-utilities](references/architecture/framework-utilities.md) |
| [lock](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/lock.rst) | [workflow-and-locks](references/architecture/workflow-and-locks.md), [scheduler](references/async/scheduler.md) |
| [workflow](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/workflow.rst) | [workflow-and-locks](references/architecture/workflow-and-locks.md) |
| [deployment](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/deployment.rst) | [deployment-and-performance](references/workflow/deployment-and-performance.md) |
| [performance](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/performance.rst) | [deployment-and-performance](references/workflow/deployment-and-performance.md) |
| [http_cache](https://github.com/symfony/symfony-docs/blob/9162aaaa515256a0ceeab6b98e313e9d1dcb89fe/http_cache.rst) | [deployment-and-performance](references/workflow/deployment-and-performance.md), [cache](references/data/cache.md), [sessions](references/http/sessions.md) |
| [ai/components/mate](https://github.com/symfony/ai/blob/5ad77d9418152e61e5b2b2bbb29d070a07fc2a67/docs/components/mate.rst) | [ai-mate](references/workflow/ai-mate.md) |
| [ai/bundles/mcp-bundle](https://github.com/symfony/ai/blob/5ad77d9418152e61e5b2b2bbb29d070a07fc2a67/docs/bundles/mcp-bundle.rst) | [ai-integration](references/architecture/ai-integration.md) |
| [ai/bundles/ai-bundle](https://github.com/symfony/ai/blob/5ad77d9418152e61e5b2b2bbb29d070a07fc2a67/docs/bundles/ai-bundle.rst) | [ai-integration](references/architecture/ai-integration.md) |
