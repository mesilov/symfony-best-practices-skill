# Console commands and typed input

Read for console-commands and controller-cleanup. The CLI is an adapter to application behavior; it must preserve its own input/output and automation contract.

## Version and form

Check installed `symfony/console`, not just a broad composer.json constraint. On the Symfony 8.0 baseline, a class-level `#[AsCommand]` with typed `__invoke()` is supported. Existing `Command::configure()`/`execute()` commands remain supported; keep them when refactoring would add no value or their lifecycle matters. Named attribute arguments are supported; positional descriptions are not a universal requirement.

Method-level command attributes and newer helper/resolver features require verifying the installed minor/source before use. Do not force every related command into a business service class. Prefer focused adapter classes or a cohesive command family according to the actual shared responsibilities, while keeping business logic callable from HTTP/async paths without Console types.

## Input and outcomes

Use `#[Argument]`/`#[Option]` or the existing InputDefinition for the command form selected. Specify required inputs, defaults, allowed formats and negative/empty cases. Use `Command::SUCCESS`, `FAILURE` or `INVALID` for the declared outcome. A user cancellation may be a successful no-op according to the contract; automation failures must not report success.

`#[MapInput]` can group arguments/options on the 8.0 baseline. Its DTO constructor is **not called**: values are assigned to public properties. Do not rely on constructor validation, promoted readonly-only state or initialization that this hydration skips. On 8.0, use supported PHP property hooks or explicit CLI conversion plus the Validator/use-case boundary as needed; constraint attributes alone are not proof they ran. The Console argument/value-resolver API introduced in 8.1 requires that installed component version; it is distinct from HttpKernel value resolvers for HTTP. Keep those resolver adapters at the transport boundary, not in shared domain classes.

Keep stdout machine-readable when the command promises JSON/CSV; diagnostics/progress should use the declared output channel and verbosity. Do not print credentials or personal provider payloads. Prefer injected services and SymfonyStyle for human-facing messages. Follow the project's strict typing/style conventions.

## Automation and long runs

Define behavior with `--no-interaction`: do not depend on an unanswered confirmation prompt or silently authorize a destructive action. Reuse the application's existing confirmation/force contract for the operation. A `--dry-run` must state which writes and external effects it omits; it must not trigger them through a helper service accidentally.

For imports/backfills, use bounded batches, durable checkpoints and idempotent retries; see [Doctrine performance](../data/doctrine-performance.md). Handle cancellation/signals using the supported command/process lifecycle and finish or roll back the current unit safely. Progress is not a checkpoint. State whether a cancelled run can be resumed and what was already committed. Memory/time limits and supervision belong to the runtime/deployment contract.

Test registration, valid/invalid input, exit codes, output, non-interactive branches, dry-run effects and restart/cancellation where applicable through the verified project runner. Use CommandTester, or ApplicationTester when Console events are part of the behavior; see [Testing](../workflow/testing.md).

Primary guidance: [Symfony Console](https://symfony.com/doc/8.0/console.html), [input/MapInput](https://symfony.com/doc/8.0/console/input.html), [8.1 Console argument resolvers](https://symfony.com/blog/new-in-symfony-8-1-console-argument-resolvers), [signals](https://symfony.com/doc/8.0/console.html#handling-signals).
