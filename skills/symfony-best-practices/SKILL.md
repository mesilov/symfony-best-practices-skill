---
name: symfony-best-practices
description: Use when implementing, debugging, refactoring, or reviewing Symfony 8.x applications, including HTTP/routing, DI/events, Doctrine, async work, security, tests, deployment, and optional Symfony AI/MCP integration.
license: MIT
metadata:
  version: "0.1.0"
---

# Symfony Best Practices

Use the project's conventions and installed APIs to make the smallest change that satisfies the requested behavior. Target Symfony **8.x**; the official documentation review is **8.1 / PHP 8.4+**, with explicit 8.0 compatibility notes. Check installed minors; Symfony AI/bundle versions are independent.

## Establish context

Read repository instructions, `composer.json`, `composer.lock`, relevant configuration, existing code/tests, and CI commands. Identify the verified PHP/console/Composer/test runner from Makefile, scripts, container configuration, or documentation. Use existing wrappers; do not guess a Compose service or fall back to host PHP when the project runs in containers.

Record the behavior to preserve, versions of affected packages, runtime, test database/transport, and relevant constraints. If the project is outside Symfony 8.x, identify the mismatch and use documentation for its installed line; this skill does not authorize an upgrade. Check installed command help or source for uncertain flags/signatures. Documentation access can use any available source; no particular MCP or companion skill is required.

## Load guidance by task

Read only relevant references; combine them when a change crosses boundaries.

| Group | Read for the current task |
| --- | --- |
| Workflow | [Runtime/quality](references/workflow/workflow-and-quality.md), [configuration](references/workflow/configuration.md), [tests](references/workflow/testing.md), [logs/errors](references/workflow/logging-and-errors.md), [deployment/performance](references/workflow/deployment-and-performance.md), [AI Mate](references/workflow/ai-mate.md) |
| Architecture | [Services/domain](references/architecture/architecture.md), [bundles](references/architecture/bundle-organization.md), [console](references/architecture/console-commands.md), [DI/events](references/architecture/container-and-events.md), [Workflow/Lock](references/architecture/workflow-and-locks.md), [utilities](references/architecture/framework-utilities.md), [AI/MCP](references/architecture/ai-integration.md) |
| HTTP/API | [Routing/kernel](references/http/routing-and-kernel.md), [REST/errors](references/http/rest-api.md), [DTOs/forms/validation](references/http/validation-and-forms.md), [sessions](references/http/sessions.md), [Serializer](references/http/serializer.md), [HttpClient/webhooks](references/http/http-client-and-webhooks.md) |
| Data | [ORM/transactions](references/data/doctrine-modeling.md), [queries/batches](references/data/doctrine-performance.md), [migrations](references/data/migrations.md), [cache](references/data/cache.md) |
| Background work | [Messenger](references/async/messenger.md), [Scheduler](references/async/scheduler.md), [Mailer/Notifier](references/async/mailer-and-notifier.md) |
| Security | [Authentication](references/security/authentication.md), [JWT](references/security/jwt.md), [authorization/rate limits](references/security/authorization-and-rate-limiting.md) |
| Presentation | [Twig/translation](references/presentation/twig-and-translation.md), [Twig components](references/presentation/twig-components.md) |

## Apply and verify

Keep entry points focused on input, authorization, delegation, and response. Follow established module boundaries; add CQRS, ports, strategies, or infrastructure only when the use case warrants them. Preserve public behavior during refactoring.

For changed behavior, add a focused regression/acceptance test, observe the relevant failure, implement, and rerun. Choose real DB/transport/browser checks where their behavior matters; mocks alone do not prove persistence or delivery. Run the project's required quality gates and inspect the diff for unrelated changes.

Inspection does not imply permission to mutate shared state: identify the environment before migrations, fixture resets, queue consumption/retry/removal, or cache clearing. Use changes already authorized by the task; never include credentials, personal payloads, or decrypted configuration in reports.

Report what changed, the selected versions/runner, commands and results, and checks that were skipped or blocked. Local checks, CI, deployment, and live integration are separate evidence.

[Sources and adaptation decisions](SOURCES.md) record 42 donors and 40 official documentation pages (43 requested URLs), pinned revisions, corrections, and licenses.
