# Sources and adaptation decisions

Version 0.1.0, reviewed on 2026-10-13. Scope: Symfony 8.x; examples and baseline API verified against Symfony 8.0 / PHP 8.4+. Package versions still come from each project's lock file.

## Donor provenance

Selected 29 skills from [dev-toolings/superpowers-symfony](https://github.com/dev-toolings/superpowers-symfony), pinned at `459bcd0b7742e2f636374daa3552d9574527410e`. Both SKILL.md and reference.md are accounted for in each donor entry: 58 Markdown source hashes plus the upstream LICENSE hash are recorded in [sources.json](sources.json). Hashes identify the reviewed source; they do not establish runtime correctness or replace reviewing a future upstream update.

The requested symfony-schedu directory does not exist in this revision. It is mapped explicitly to symfony-scheduler. No other donor skills, plugin hooks, agents, commands, or runtime helper scripts are bundled.

| Donor | Consolidated reference |
| --- | --- |
| [bootstrap-check](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/bootstrap-check) | [workflow-and-quality](references/workflow-and-quality.md) |
| [daily-workflow](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/daily-workflow) | [workflow-and-quality](references/workflow-and-quality.md) |
| [effective-context](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/effective-context) | [workflow-and-quality](references/workflow-and-quality.md) |
| [quality-checks](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/quality-checks) | [workflow-and-quality](references/workflow-and-quality.md) |
| [config-env-parameters](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/config-env-parameters) | [configuration](references/configuration.md) |
| [controller-cleanup](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/controller-cleanup) | [architecture](references/architecture.md) |
| [cqrs-and-handlers](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/cqrs-and-handlers) | [architecture](references/architecture.md) |
| [interfaces-and-autowiring](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/interfaces-and-autowiring) | [architecture](references/architecture.md) |
| [ports-and-adapters](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/ports-and-adapters) | [architecture](references/architecture.md) |
| [strategy-pattern](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/strategy-pattern) | [architecture](references/architecture.md) |
| [value-objects-and-dtos](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/value-objects-and-dtos) | [architecture](references/architecture.md) |
| [doctrine-relations](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-relations) | [doctrine-modeling](references/doctrine-modeling.md) |
| [doctrine-transactions](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-transactions) | [doctrine-modeling](references/doctrine-modeling.md) |
| [doctrine-batch-processing](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-batch-processing) | [doctrine-performance](references/doctrine-performance.md) |
| [doctrine-fetch-modes](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-fetch-modes) | [doctrine-performance](references/doctrine-performance.md) |
| [doctrine-migrations](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-migrations) | [migrations](references/migrations.md) |
| [doctrine-fixtures-foundry](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/doctrine-fixtures-foundry) | [testing](references/testing.md) |
| [e2e-panther-playwright](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/e2e-panther-playwright) | [testing](references/testing.md) |
| [functional-tests](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/functional-tests) | [testing](references/testing.md) |
| [tdd-with-phpunit](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/tdd-with-phpunit) | [testing](references/testing.md) |
| [test-doubles-mocking](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/test-doubles-mocking) | [testing](references/testing.md) |
| [symfony-messenger](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/symfony-messenger) | [messenger](references/messenger.md) |
| [messenger-retry-failures](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/messenger-retry-failures) | [messenger](references/messenger.md) |
| [symfony-scheduler](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/symfony-scheduler) | [scheduler](references/scheduler.md) |
| [form-types-validation](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/form-types-validation) | [security-and-forms](references/security-and-forms.md) |
| [symfony-voters](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/symfony-voters) | [security-and-forms](references/security-and-forms.md) |
| [rate-limiting](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/rate-limiting) | [security-and-forms](references/security-and-forms.md) |
| [symfony-cache](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/symfony-cache) | [cache](references/cache.md) |
| [twig-components](https://github.com/dev-toolings/superpowers-symfony/tree/459bcd0b7742e2f636374daa3552d9574527410e/content/skills/twig-components) | [twig-components](references/twig-components.md) |

## Adaptation decisions

- Keep one portable entry with conditional references. Runtime wrappers and exact versions are discovered from the consuming project; no dependency on the donor's symfony-context or Superpowers skills.
- Target Symfony 8.x. Use 8.0-compatible baseline guidance and inspect installed minor APIs before using newer features; do not initiate framework upgrades.
- Diagnose without automatic pull/install/migration/fixture/cache/queue mutations. Existing task authorization governs concrete changes.
- Replace blanket line counts, mandatory layers/interfaces and automatic CQRS with use-case and existing-project criteria.
- Require a fresh EntityManager after closure; clear cannot reopen it. Separate ORM wrapInTransaction from DBAL transactional.
- Distinguish bounded retry policy from RecoverableMessageHandlingException forcing retries on the 8.0 baseline. retryDelay is already available there; do not blindly copy donor 8.1 labels.
- Strengthen message idempotency for races and external-success/local-crash windows. A status pre-check alone is insufficient.
- Treat irreversible migrations honestly; a destructive down or dry-run is not a data-preserving recovery proof.
- Preserve Foundry factory-specific proxy behavior and version gates for extensions/reset attributes. Browser-server connections need their own DB isolation; process-local rollback is insufficient.
- Separate scheduler emission locks, job overlap and successful business completion. Multiple schedule consumers can be coordinated rather than universally forbidden.
- Include cache tenant/user/permission isolation, Twig escaping and the distinction between application rate limiting and edge DoS protection.

## Primary sources

The references link to relevant official docs. Symfony 8.0, Doctrine ORM 3.5.0, Foundry and UX TwigComponent source revisions are recorded in sources.json; Doctrine Migrations 3.9.0 implicit-commit docs and AbstractMigration source were also inspected. No claim of compatibility with every later minor or optional bundle follows from this review. Online docs can change; verify matching installed APIs for real application work.

## License

Original project work is covered by [LICENSE](LICENSE). Donor attribution and its full MIT notice are included in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md). Official docs are linked as primary evidence; their manuals are not bundled.
