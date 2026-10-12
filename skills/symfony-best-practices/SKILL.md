---
name: symfony-best-practices
description: Use when implementing, debugging, refactoring, or reviewing Symfony 8.x applications, including controllers, services, configuration, Doctrine persistence, Messenger, Scheduler, forms, security, cache, Twig components, and PHPUnit tests.
license: MIT
metadata:
  version: "0.1.0"
---

# Symfony Best Practices

Use the project's conventions and installed APIs to make the smallest change that satisfies the requested behavior. Target Symfony **8.x**; the reference baseline is **8.0 / PHP 8.4+**. Check the actual minor versions before using newer features.

## Establish context

Read repository instructions, `composer.json`, `composer.lock`, relevant configuration, existing code/tests, and CI commands. Identify the verified PHP/console/Composer/test runner from Makefile, scripts, container configuration, or documentation. Use existing wrappers; do not guess a Compose service or fall back to host PHP when the project runs in containers.

Record the behavior to preserve, versions of affected packages, runtime, test database/transport, and relevant constraints. If the project is outside Symfony 8.x, identify the mismatch and use documentation for its installed line; this skill does not authorize an upgrade. Check installed command help or source for uncertain flags/signatures. Documentation access can use any available source; no particular MCP or companion skill is required.

## Load guidance by task

Read only relevant references; combine them when a change crosses boundaries.

| Task | Reference |
| --- | --- |
| Bootstrap, daily work, diagnostics, context, quality gates | [Workflow and quality](references/workflow-and-quality.md) |
| Environment variables, parameters, secrets | [Configuration](references/configuration.md) |
| Thin controllers/commands, DI, CQRS, ports, strategies, VOs/DTOs | [Architecture](references/architecture.md) |
| Relations, owning sides, transactions, locking | [Doctrine modeling](references/doctrine-modeling.md) |
| N+1, fetch modes, projections, bounded batches | [Doctrine performance](references/doctrine-performance.md) |
| Schema changes, data migrations, rollback | [Migrations](references/migrations.md) |
| PHPUnit, functional tests, doubles, Foundry, Panther/Playwright | [Testing](references/testing.md) |
| Async handlers, transports, idempotency, retries/failures | [Messenger](references/messenger.md) |
| Recurring work, timezones, downtime, overlap | [Scheduler](references/scheduler.md) |
| Forms/validation, voters, rate limiting | [Security and forms](references/security-and-forms.md) |
| Pools, TTLs, tags, stampede, HTTP cache | [Cache](references/cache.md) |
| UX Twig components, props, slots, escaping | [Twig components](references/twig-components.md) |

## Apply and verify

Keep entry points focused on input, authorization, delegation, and response. Follow established module boundaries; add CQRS, ports, strategies, or infrastructure only when the use case warrants them. Preserve public behavior during refactoring.

For changed behavior, add a focused regression/acceptance test, observe the relevant failure, implement, and rerun. Choose real DB/transport/browser checks where their behavior matters; mocks alone do not prove persistence or delivery. Run the project's required quality gates and inspect the diff for unrelated changes.

Inspection does not imply permission to mutate shared state: identify the environment before migrations, fixture resets, queue consumption/retry/removal, or cache clearing. Use changes already authorized by the task; never include credentials, personal payloads, or decrypted configuration in reports.

Report what changed, the selected versions/runner, commands and results, and checks that were skipped or blocked. Local checks, CI, deployment, and live integration are separate evidence.

[Sources and adaptation decisions](SOURCES.md) record all 29 donors, pinned revision, corrections, and license provenance.
