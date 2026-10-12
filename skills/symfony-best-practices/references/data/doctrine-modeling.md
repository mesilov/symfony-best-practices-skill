# Doctrine relations, transactions, and locking

Read for doctrine-relations, doctrine-transactions, doctrine-orm, and transactional-patterns. Determine ORM, DBAL, DoctrineBundle, DB server and entity-manager versions separately from Symfony.

## Relations

The owning side records association changes. In a bidirectional ManyToOne/OneToMany, set the ManyToOne reference and keep both sides coherent with add/remove helpers. Initialize collection properties and align nullability, FK constraints and removal behavior.

Choose `cascade: ['persist']` for objects saved as part of the same aggregate. Use `orphanRemoval` only for privately owned children that cannot be reused elsewhere; avoid `cascade: ['remove']` on shared entities or huge collections. Database `ON DELETE` and ORM removal have different listener/lifecycle behavior. Test the actual constraint and deletion contract.

Use LAZY by default; select data per query and use EXTRA_LAZY for appropriate large-collection operations. See [Doctrine performance](doctrine-performance.md). Associations cannot span entity managers. Identify the correct manager/repository using `ManagerRegistry` and the configured manager name; do not assume the default.

## Transaction boundary

A use case owns atomic writes, not the HTTP controller. A single ORM `flush()` wraps its queued writes in a transaction. Use `EntityManager::wrapInTransaction()` when several ORM/DBAL steps must commit together; it flushes before commit. Avoid a redundant explicit flush unless an intermediate generated value or other verified constraint requires it.

`Connection::transactional()` is for DBAL work and does not flush ORM changes. ORM `transactional()` is removed in ORM 3; DBAL's method remains valid. Do not copy an obsolete API merely because Symfony's version matches.

Keep transactions and pessimistic locks short. Remote HTTP calls, emails and other external effects are not rolled back by a DB transaction: put them outside the lock/transaction and use an idempotency/outbox contract when needed. Nested transactions/savepoints do not create independently committed business operations.

## Failure and recovery

A failed ORM flush or `wrapInTransaction()` can close the EntityManager. **`clear()` does not reopen a closed manager.** Discard failed managed objects and obtain a fresh manager via the project's lifecycle/`ManagerRegistry::resetManager()`; reacquire repositories and dependencies that held the old manager before retrying. Objects' in-memory state is not reverted by DB rollback.

Retry only explicitly classified transient conflicts, with a bounded policy and a fresh unit of work. Do not catch every exception and continue with stale entities. Never translate a uniqueness race into success without verifying the business outcome.

## Concurrency

Use an integer `#[ORM\Version]` field for optimistic locking where users edit potentially stale data. Carry the version they actually read through the update request; checking a freshly reloaded version alone misses lost updates. Map conflicts to the project's response/CLI contract.

Acquire `PESSIMISTIC_WRITE`/`PESSIMISTIC_READ` only inside an active transaction and on the intended rows. Add real unique constraints for invariants that must hold under concurrent requests. Define conflict/lease/retry behavior; an application-level pre-check is not a uniqueness guarantee.

## Verification

On an isolated DB of the intended platform, test owning-side persistence, aggregate deletion/orphan semantics, uniqueness, atomic rollback, and competing writes. Confirm manager recovery after failure rather than mocking `flush()`. Run relevant schema validation and migration review through the project runner; never repair production with `doctrine:schema:update --force`.

Primary guidance: [Doctrine associations](https://www.doctrine-project.org/projects/doctrine-orm/en/3.5/reference/working-with-associations.html), [transactions/concurrency](https://www.doctrine-project.org/projects/doctrine-orm/en/3.5/reference/transactions-and-concurrency.html), [multiple managers](https://symfony.com/doc/8.0/doctrine/multiple_entity_managers.html).

## Entity conventions and lifecycle

Prefer typed PHP attribute mappings and compatible immutable date/backed-enum types where they match the domain. String-backed and integer-backed enums are both valid when their values are intentional; do not confuse a stable integer backing value with an ordinal. ID choice follows existing schema/API contracts; UUID v7 can help particular allocation/indexing needs, but neither UUIDs nor private constructors are universal ORM requirements. Factories/behavior methods help invariants; verify hydration/proxies and fixture tooling before changing construction.

A flush synchronizes the whole pending unit of work; it is not the outer commit boundary when an explicit transaction is already active. postFlush is also not proof of that outer commit. Use a real after-commit/outbox lifecycle for external effects. Avoid recursive flushes from lifecycle callbacks.
