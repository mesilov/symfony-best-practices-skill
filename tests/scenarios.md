# Skill application scenarios

These are read-only decision simulations, not executed Symfony integration tests. Use a fresh agent: read SKILL.md and only relevant references, propose a concrete change/test plan, name the reference used, then assess against the expected decision. Do not mutate an application/DB or claim real runtime evidence.

| ID | Concrete scenario | Expected decision and routing |
| --- | --- | --- |
| S1 | Symfony 8.0/PHP 8.4; README requires make; make test uses a custom Compose file/app service; article proposes 8.1 runCommand helpers | Keep make test; CommandTester baseline, inspect owning class/minor for helpers; ApplicationTester for Console events. testing + workflow-and-quality |
| S2 | Four million Orders; toIterable query fetch-joins lines; flush/clear every 100; closed EM after failure | Bounded root/keyset pages, relations separately; ORM checkpoint before final flush in same transaction; fresh manager after closure; test last page/restart/RSS. doctrine-performance + doctrine-modeling |
| S3 | Concurrent duplicate payment messages, provider 429, max_retries 3; proposed Recoverable exception | Ordinary bounded retry policy, Retry-After; recoverable forces retry on baseline; atomic unique claim/recovery, provider idempotency/reconciliation, short DB transactions, outbox if needed. messenger |
| S4 | MySQL DDL with all_or_nothing true deletes populated column; dry-run called rollback proof | Nontransactional DDL policy, real disposable DB execution and data-aware recovery; irreversible when data cannot be restored. migrations |
| S5 | Authenticated dashboard cached under global dashboard key; user subtitle rendered raw; application RateLimiter called DoS protection | User/tenant/permission key isolation and invalidation, correct HTTP cache policy, escaping/sanitizer contract, separate edge limits. data/cache + presentation/twig-components + security/authorization-and-rate-limiting |
| S6 | Formatter/PHPStan passed; DB functional tests not run; report requests all-green wording | Report executed and not-run checks separately; identify isolated test DB/runner and execute needed suite when possible; no CI/live claim. workflow-and-quality + testing |
| S7 | Foundry 2.2 proxy factories/_real proposed for blanket replacement with real objects and 2.9 reset extension; Panther server separate from DAMA test connection | Preserve version/type-specific proxy semantics, installed traits/reset lifecycle; committed DB setup/cleanup or isolated resettable DB across server processes. testing |
| S8 | Two scheduler consumers; stateful + schedule lock; redispatch async work running 20 minutes every five | Separate emission coordination from job overlap; explicit catch-up contract, job claim/lease renewal/recovery, dedupe keys and capacity. scheduler |
| S9 | IMPORT_ENABLED is string false; provider token; raw env-vars report and commit of .env.local.php/private vault key proposed | Typed bool injection, redacted diagnostic output, secret storage, exclude generated secret dump/private key; check precedence and worker lifecycle. configuration |
| S10 | Simple CRUD with attribute entities, one service, stable two-case match; review demands CQRS/XML/interfaces/readonly props/ten-line controllers | Respect existing architecture and task need; reject blanket layers, keep mutable hydrated Twig props; verify behavior and boundaries. architecture + twig-components |

## Recorded runs on 2026-10-13

A baseline agent without the new skill answered six initial scenarios. It already made appropriate choices; no missing-rule failure was observed. Its first version scenario targeted Symfony 6.4, before the user narrowed the new skill to 8.x. This baseline is not a quantified comparison or proof of improvement.

The first with-skill run covered S1–S10 and found a textual defect in S2's pseudocode. Reviewer evidence: "при ручной транзакции и ORM persist/setLastKey после этого flush checkpoint не попадёт в commit". The reference was corrected: mutate/persist ORM checkpoint before final flush, then commit both; DBAL alternative inside the same transaction is explicit.

S1/S2/S3 were rerun after correction. The reviewer reported no remaining confirmed defects in the three revised references. Other scenario solutions matched the expected decisions. The scenarios assess routing and recommendations, not actual package/runtime compatibility under every combination of versions.

## Extension scenarios for the second donor

| ID | Scenario | Expected routing/decision |
| --- | --- | --- |
| B1 | Symfony 8.0 long CLI import, automation/cancel/resume; proposed 8.1 method/resolver API and constructor-only MapInput validation | architecture/console-commands + data/doctrine-performance + workflow/testing; supported API, explicit input validation, checkpoints and automation/cancellation contract |
| B2 | REST problem+json, raw exception details/status in domain, HTML login and auth/method/rate headers | http/rest-api + http/validation-and-forms + security/authentication; adapter mapping, safe messages, headers, API-only scope and actual security handlers |
| B3 | Multi-tenant Lexik API, decoded tenant/roles, refresh localStorage, claimed immediate stateless logout | security/jwt + authentication + authorization; verified claims, current resource membership, concrete revocation/refresh/cookie policy |
| B4 | AppBundle or mandatory layers for simple CRUD; excluding all Domain; genuinely reusable library | architecture/architecture + bundle-organization; conditional layout and explicit discovery, reusable library/bundle distinguished from application modules |
| B5 | PATCH missing/null, nested DTO cascade and malformed/payload/query errors | http/validation-and-forms + rest-api; presence representation, actual hydration/validation, explicit status/error matrix with MapQueryString baseline 404 |

Before extension, a separate baseline agent identified partial/missing addressable guidance for these five tasks. A fresh with-skill agent read only relevant references and proposed concrete solutions for B1–B5. It found a Console documentation URL error and a narrow resolver version ambiguity; both were corrected against official docs and the reviewer rechecked the updated Console reference without new findings. Neither run executed an application, DB or auth provider.

## Official documentation extension scenarios — 2026-10-15

| ID | Scenario | Expected routing/decision |
| --- | --- | --- |
| C1 | Public cached Twig page reads session flashes; translated user text uses raw; two users/locales | http/sessions + data/cache + presentation/twig-and-translation; preserve private session response, explicit anonymous/public split and locale variants, escape/sanitize |
| C2 | Tenant retained by shared kernel subscriber; fragment requests and tenant A→B persistent worker; /orders/{id} collides with /orders/export | http/routing-and-kernel + architecture/container-and-events; lifecycle/main request scope, explicit current context/reset, route requirements/priority and real matching tests |
| C3 | HttpClient 429/timeouts, webhook signature after JSON re-encode, mail inside DB transaction | http/http-client-and-webhooks + async/mailer-and-notifier + async/messenger; lazy response/error handling, bounded total/idle retry budget, raw bytes signature/secret/replay, durable post-commit delivery |
| C4 | Workflow can then apply races; 20-minute job has 5-second lock TTL; remove accepts user path | architecture/workflow-and-locks + framework-utilities; persisted concurrency control, lease renewal/loss, authorized path containment and symlink/race analysis |
| C5 | composer update on release; CLI cache clear assumed to refresh FPM/workers; secret provider headers logged and TLS disabled | workflow/deployment-and-performance + logging-and-errors + http/http-client-and-webhooks; locked install, actual runtime restart/supervision, redaction and TLS verification |
| C6 | Assess AI ecosystem; proposed autoinstall all packages, production MCP server, retrieved docs as system instructions and unrestricted write tools | workflow/ai-mate + architecture/ai-integration; dev CLI versus app bundles, installed package versions, scoped auth/authz/tool exposure, data trust, budgets and real invocation tests |

Baseline read the old 18-reference package and found partial addressable coverage C1–C5; C6 had no dedicated AI reference. It could propose some solutions from its own knowledge. This is a coverage comparison, not a quantified behavior benchmark or executed integration test. Fresh with-skill review uses the same six task descriptions without the expected-decision column.

## Repository maintainer scenarios

Read `AGENTS.md` and `.agents/skills/symfony-skill-maintainer/SKILL.md` for these read-only simulations. Do not open a real PR or mutate a repository.

| ID | Scenario | Expected decision |
| --- | --- | --- |
| M1 | A README wording fix is ready; local checks pass; opening a PR to main is authorized; CHANGELOG is unchanged | Add a truthful entry for this change, commit it with the branch, and inspect its diff before opening |
| M2 | A skill rule changes; open a draft now and add changelog notes before merge | Complete the meaningful entry before opening the draft; draft status does not bypass the gate |
| M3 | CHANGELOG appears in the file list, but its only change is whitespace | Inspect text and substantive target-to-head diff; whitespace does not meet the gate |
| M4 | The branch contains an unrelated changelog entry already present in main | Compare against refreshed actual target; baseline or unrelated history does not document this change; avoid filler or duplicates |

Before the maintainer skill existed, an independent baseline agent would open M1 without an entry and M2 as a draft with notes deferred. It found no opening gate in repository instructions or CI. It also rejected whitespace/unrelated entries as evidence of documentation but did not consider that a reason to block opening. This is observed text behavior, not a runtime or CI test.

A fresh evaluator using the new maintainer skill required the current change's committed, substantive changelog entry before opening in all four scenarios. It found no blocking ambiguity and confirmed that the actual new entry describes this skill truthfully. The gate is an agent instruction; no automatic semantic CI enforcement is claimed.
