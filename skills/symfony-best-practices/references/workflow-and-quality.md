# Workflow and quality

Read for bootstrap-check, daily-workflow, effective-context, and quality-checks. All console commands below are subcommands: prepend the project's verified runner.

## Bootstrap without changing state

1. Inspect lock-file versions, enabled bundles, service registration, routes and package/test configuration. Distinguish an unavailable dependency from an incorrect configuration.
2. Find runtime wrappers and actual service names. Run existing inspection targets, or `about`, `debug:router`, `debug:autowiring`, and `lint:container` through that runner when available. These can boot/warm an application: confirm the local environment first.
3. Inspect environment variable names and required defaults without printing secret values. A missing `.env` alone is not proof of failure: real environment variables or a secrets vault may supply configuration.
4. For DB work, identify the connection, server version, entity manager and environment; use `doctrine:migrations:status` and `doctrine:schema:validate` only on the confirmed development/test database.
5. For optional stacks, check their configuration and corresponding `debug:messenger`, `debug:scheduler`, `debug:twig-component`, or cache inspection commands if installed.

Do not turn diagnosis into `composer install`, `cache:clear`, migrations, fixture loading, worker start, or automatic `git pull`. Check the existing checkout and requested scope before such changes. Correct cache ownership/ACLs in the appropriate runtime; do not prescribe `chmod 777`.

## Daily changes and diagnostics

Use the committed lock file for dependency installation when required; dependency updates change the task's scope. Preserve unrelated local work. Reproduce the symptom with the smallest relevant input and inspect the route/container wiring, profiler, sanitized log context, and generated SQL before changing code. Never patch `vendor/`.

For bug fixes, assert the reported failure. For refactoring, cover the existing behavior before moving responsibilities. Reuse the project's test framework, formatting rules, static-analysis configuration and CI targets. Avoid global formatter edits when only one module changes.

## Quality gates

Prefer documented `make`/Composer/CI targets. Where those do not exist, identify the installed tool and config before constructing a command:

| Concern | Evidence to collect |
| --- | --- |
| Composer metadata | Project's `composer validate` result |
| Style | Installed PHP-CS-Fixer/ECS/Pint check or dry-run diff |
| Types | Configured PHPStan/Psalm result, existing baseline policy |
| Container/config/templates | Relevant lint target for changed files/environment |
| Behavior | Focused test result and required suite result |
| Scope | Diff, removed debug code, no exposed secrets/generated noise |

Do not suppress a new type error, broaden ignore rules, or update a baseline solely to get a green run. Explain a justified exception. Apply formatting only within the intended scope. Repeat broader checks when required by the project or when new changes/failures justify them.

## Context and handoff

Record: goal and expected behavior; installed Symfony/PHP/package versions; runtime and exact wrapper; relevant files and existing pattern; sanitized error/stack/SQL; attempts; compatibility/performance constraints; test DB/transport; commands and their actual results. Include only material needed to reproduce the problem.

Report each check as passed, failed, or not run with its reason. A green linter cannot establish that DB tests, native CI or a live provider passed.

Primary guidance: [Symfony 8.0 setup](https://symfony.com/doc/8.0/setup.html), [debugging](https://symfony.com/doc/8.0/debugging.html), [testing](https://symfony.com/doc/8.0/testing.html).
