# Skill application scenarios

These are read-only decision simulations, not executed Symfony integration tests. Use a fresh agent: read SKILL.md and only relevant references, propose a concrete change/test plan, name the reference used, then assess against the expected decision. Do not mutate an application/DB or claim real runtime evidence.

| ID | Concrete scenario | Expected decision and routing |
| --- | --- | --- |
| S1 | Symfony 8.0/PHP 8.4; README requires make; make test uses a custom Compose file/app service; article proposes 8.1 runCommand helpers | Keep make test; CommandTester baseline, inspect owning class/minor for helpers; ApplicationTester for Console events. testing + workflow-and-quality |
| S2 | Four million Orders; toIterable query fetch-joins lines; flush/clear every 100; closed EM after failure | Bounded root/keyset pages, relations separately; ORM checkpoint before final flush in same transaction; fresh manager after closure; test last page/restart/RSS. doctrine-performance + doctrine-modeling |
| S3 | Concurrent duplicate payment messages, provider 429, max_retries 3; proposed Recoverable exception | Ordinary bounded retry policy, Retry-After; recoverable forces retry on baseline; atomic unique claim/recovery, provider idempotency/reconciliation, short DB transactions, outbox if needed. messenger |
| S4 | MySQL DDL with all_or_nothing true deletes populated column; dry-run called rollback proof | Nontransactional DDL policy, real disposable DB execution and data-aware recovery; irreversible when data cannot be restored. migrations |
| S5 | Authenticated dashboard cached under global dashboard key; user subtitle rendered raw; application RateLimiter called DoS protection | User/tenant/permission key isolation and invalidation, correct HTTP cache policy, escaping/sanitizer contract, separate edge limits. cache + twig-components + security-and-forms |
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
