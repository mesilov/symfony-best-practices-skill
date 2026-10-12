# Schema and data migrations

Read for doctrine-migrations. Inspect installed DoctrineMigrationsBundle, doctrine/migrations, DBAL and database versions; their majors are independent.

## Prepare and review

Generate a diff using the project's `make:migration` or `doctrine:migrations:diff` target on the confirmed development DB. Read every SQL statement: renames can become drop/add, unrelated mapping changes can leak into a diff, and an index/constraint may lock a large table. Identify the manager/connection for every operation.

Never edit an already-applied migration. Keep schema changes and large backfills separable. Prefer expand/backfill/contract for changes that must coexist with old application instances. Backfills need bounded memory, checkpoints and idempotency; see [Doctrine performance](doctrine-performance.md).

Migration methods use `up(Schema $schema): void` and `down(Schema $schema): void`. Write and test a reverse operation when genuinely reversible. If removed data cannot be reconstructed, explicitly mark the migration irreversible using the installed library's helper and describe restore/roll-forward recovery. A `down()` that recreates an empty column does not restore its old data.

## Transactions and rollback

Verify transaction semantics on the actual DB platform. MySQL DDL can implicitly commit; `all_or_nothing: true` does not create rollback safety for it. Use `isTransactional(): bool { return false; }` for a migration that requires nontransactional DDL and a compatible all-or-nothing policy, following the installed library and project configuration. PostgreSQL also has operations that cannot run in a transaction: inspect the actual statements.

`migrate --dry-run` previews planned SQL; it does not prove permissions, data validity, runtime locks, duration, or rollback. Test application compatibility and a real up/down/up or restore/roll-forward path on a disposable representative DB. Test data survival, not just migration status. Record backup/restore evidence where the change depends on it.

## Commands and delivery

Console subcommands, with the verified project runner and installed options:

- `doctrine:migrations:status` / `doctrine:migrations:list`: establish current state.
- `doctrine:migrations:migrate --dry-run`: review the planned target.
- `doctrine:migrations:migrate`: apply only to the environment authorized for this task.
- `doctrine:migrations:execute <exact-version> --down`: a deliberate reversal of that migration, only when validated and authorized.

Check command help for manager selectors and use an exact version for rollback; `prev` is relative to the current state. Fixture loading and schema reset are not part of routine migration inspection. Deployment timing, old/new code compatibility, locks, expected duration and recovery procedure belong in the change's delivery notes.

## Verification

Run against the intended DB engine/version with representative constraints/data. Verify SQL scope, resulting schema, application reads/writes, and recovery. State separately which evidence came from dry-run, DB execution and deployment; a local rehearsal cannot establish production completion.

Primary guidance: [Symfony migrations](https://symfony.com/doc/8.0/doctrine.html#migrations-creating-the-database-tables-structure), [Doctrine migrations](https://www.doctrine-project.org/projects/doctrine-migrations/en/3.9/reference/managing-migrations.html), [implicit commits](https://www.doctrine-project.org/projects/doctrine-migrations/en/3.9/explanation/implicit-commits.html).
