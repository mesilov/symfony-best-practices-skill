# Symfony Best Practices Skill

An Agent Skill for building, debugging, and reviewing **Symfony 8.x** applications.

**0.1.0** · **7 groups** · **31 references**.

Start with [SKILL.md](skills/symfony-best-practices/SKILL.md). Read the references for your task.

## Coverage

| Group | Topics |
| --- | --- |
| **HTTP and API** | [Routing, Controllers, HttpKernel](skills/symfony-best-practices/references/http/routing-and-kernel.md); [REST, RFC 9457](skills/symfony-best-practices/references/http/rest-api.md); [DTOs, Forms, Validator](skills/symfony-best-practices/references/http/validation-and-forms.md); [Session](skills/symfony-best-practices/references/http/sessions.md); [Serializer](skills/symfony-best-practices/references/http/serializer.md); [HttpClient, Webhook](skills/symfony-best-practices/references/http/http-client-and-webhooks.md) |
| **Data and cache** | [Doctrine ORM, transactions, locking](skills/symfony-best-practices/references/data/doctrine-modeling.md); [queries, pagination, batches](skills/symfony-best-practices/references/data/doctrine-performance.md); [Migrations](skills/symfony-best-practices/references/data/migrations.md); [Cache, TTL, invalidation](skills/symfony-best-practices/references/data/cache.md) |
| **Background work** | [Messenger, retries, idempotency, outbox](skills/symfony-best-practices/references/async/messenger.md); [Scheduler](skills/symfony-best-practices/references/async/scheduler.md); [Mailer, Notifier](skills/symfony-best-practices/references/async/mailer-and-notifier.md) |
| **Security** | [Users, firewalls, passwords, CSRF](skills/symfony-best-practices/references/security/authentication.md); [JWT, refresh, revocation](skills/symfony-best-practices/references/security/jwt.md); [authorization, voters, RateLimiter](skills/symfony-best-practices/references/security/authorization-and-rate-limiting.md) |
| **Architecture and components** | [Services, domain, CQRS, ports/adapters](skills/symfony-best-practices/references/architecture/architecture.md); [modules, bundles](skills/symfony-best-practices/references/architecture/bundle-organization.md); [Console](skills/symfony-best-practices/references/architecture/console-commands.md); [DI, Kernel, Events](skills/symfony-best-practices/references/architecture/container-and-events.md); [Workflow, Lock](skills/symfony-best-practices/references/architecture/workflow-and-locks.md); [Filesystem, UID, YAML, ExpressionLanguage](skills/symfony-best-practices/references/architecture/framework-utilities.md); [AI Bundle, MCP Bundle](skills/symfony-best-practices/references/architecture/ai-integration.md) |
| **Presentation** | [Twig, Translation, escaping](skills/symfony-best-practices/references/presentation/twig-and-translation.md); [UX Twig Components](skills/symfony-best-practices/references/presentation/twig-components.md) |
| **Development and operations** | [Runtime, quality checks](skills/symfony-best-practices/references/workflow/workflow-and-quality.md); [configuration, env, secrets](skills/symfony-best-practices/references/workflow/configuration.md); [PHPUnit, Foundry, Panther/Playwright](skills/symfony-best-practices/references/workflow/testing.md); [logging, error pages](skills/symfony-best-practices/references/workflow/logging-and-errors.md); [deployment, performance, HTTP cache](skills/symfony-best-practices/references/workflow/deployment-and-performance.md); [AI Mate](skills/symfony-best-practices/references/workflow/ai-mate.md) |

## Compatibility

- **Symfony 8.x, PHP 8.4+.** Documentation was reviewed against Symfony 8.1 on 2026-10-15. Important 8.0 differences are noted.
- **Use installed APIs.** Check Doctrine, Foundry, UX, Lexik, and Symfony AI versions separately.
- **Follow the project's architecture.** Apply CQRS, DDD, ports, and separate buses when the task needs them.
- **Use the project's runtime.** Database, cache, and queue operations require the correct environment and authorization.
- **Verify each boundary.** Local tests, CI, deployment, and live provider checks establish different results.

## Installation

Copy the complete `skills/symfony-best-practices/` directory to your agent's skill directory. Keep its references, metadata, and licenses.

A typical project layout:

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

For a global Codex installation, use `${CODEX_HOME:-$HOME/.codex}/skills/`. Other agents may use different locations. Preserve local changes when updating.

Invoke with `$symfony-best-practices`. Codex metadata also allows automatic skill selection. Python is needed only to validate and build the package.

## Sources

The skill combines **42 donor skills** and **40 Symfony documentation pages**. All 43 requested URLs are recorded, including Security anchors. Source revisions and SHA-256 hashes are pinned.

[Donors and reference map](skills/symfony-best-practices/SOURCES.md) · [Manifest](skills/symfony-best-practices/sources.json) · [Source corrections](docs/source-review.md) · [Documentation review](docs/official-documentation-review-2026-10-15.md)

## Validation and build

From the repository root, with Python 3.11+:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python scripts/validate.py
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python scripts/build_release.py
```

On Windows, use `.venv\Scripts\python.exe`.

The build creates `dist/symfony-best-practices-0.1.0.tar.gz`, `.zip`, and `SHA256SUMS`. Both archives contain the `symfony-best-practices/` directory.

[Verification results and source-check commands](docs/verification-0.1.0.md) · [Design](docs/superpowers/specs/2026-10-13-symfony-skill-0.1.0-design.md) · [Plan](docs/superpowers/plans/2026-10-13-symfony-skill-0.1.0.md) · [Changelog](CHANGELOG.md)

## License

The authored package uses [MIT](LICENSE). Symfony Docs are a reference source under CC BY-SA 3.0. Manual text and examples are not included.

Full MIT notices for both donors and Symfony AI: [THIRD_PARTY_NOTICES.md](skills/symfony-best-practices/THIRD_PARTY_NOTICES.md).
