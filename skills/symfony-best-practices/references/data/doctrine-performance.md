# Doctrine fetching and bounded processing

Read for doctrine-fetch-modes, doctrine-batch-processing, and doctrine-query-optimization. Establish a query/memory baseline before changing a mapping.

## Query shape

Use the profiler/generated SQL to distinguish N+1, excessive columns, slow predicates and missing indexes. Prefer per-use-case fetch joins (`leftJoin()` plus `addSelect()`) to global EAGER mapping. EXTRA_LAZY allows selected collection operations without loading the full collection; iteration still loads data. Verify generated SQL and pagination, especially with collection fetch joins.

For read-only views, select scalar rows or `SELECT NEW` DTO projections rather than managed entities with partially initialized fields. Constructor types/order must match the projection. A read-only hint changes tracking behavior; it does not make an object immutable. DQL PARTIAL support varies across ORM 3 minors; it is not the default recommendation.

Use DBAL `fetchAssociative()`, `fetchAllAssociative()`, `fetchOne()` or `executeStatement()` according to the result needed. An unbounded `fetchAllAssociative()` still loads the entire result. Bind values and allowlist dynamic identifiers/order expressions; parameter binding does not make an arbitrary column name safe.

## Batch strategy

Never `findAll()` on an unbounded table. Use `toIterable()` for suitable queries or keyset pages with stable ordering and a persisted checkpoint. **A query that fetch-joins a collection-valued association cannot be streamed with `toIterable()`.** Page root IDs/objects and load needed relations in a separate bounded query.

```text
upper_bound := initial maximum stable key
last_key := committed checkpoint
repeat:
    load at most batch_size roots where last_key < key <= upper_bound, ordered by key
    if empty: finish
    in one short transaction:
        process this page's DB changes
        update/persist the ORM checkpoint for this page before the final flush
        flush once (or let wrapInTransaction flush after the callback)
        commit both page changes and checkpoint
    clear managed state; discard entity references
    last_key := committed page key
```

A direct DBAL checkpoint update is another option inside the same transaction; ORM checkpoint changes must be included in the final flush. Never commit page writes with an unflushed ORM checkpoint.

Choose bounds/order for the actual key type and desired consistency. If processed rows can move in or out of the predicate, document the traversal semantics. A batch run is partly committed after each successful page; it is not one atomic transaction over millions of rows.

Flush before clear when preserving ORM updates, including the final incomplete batch. Clear detaches all entities; retain scalar IDs, not managed references, between pages. Re-fetch dependencies as needed. Where the driver cannot write while a read cursor remains open, materialize only the bounded page before writing.

DQL bulk UPDATE/DELETE and DBAL can avoid hydration but bypass normal unit-of-work state, ORM lifecycle behavior and optimistic-lock checks. Confirm required domain effects, then clear/reload affected managed state. Bound transaction size when locks/log growth matter. Use driver/configuration-appropriate logging controls; `setSQLLogger()` is not a DBAL 4 API.

## Recovery and measurement

Define restart behavior, stable idempotency keys for external effects, progress/checkpoint persistence and an interruption policy. A PHP memory-limit check alone misses memory buffered by the DB driver. Measure RSS, PHP peak memory, query count, elapsed time and batch size on representative data.

Test zero rows, an exact page, the final partial page, failure before commit, restart from checkpoint, and concurrent claim behavior when multiple workers run. Compare before/after query counts and memory; do not claim a performance improvement from a rewritten query alone.

Primary guidance: [Doctrine batch processing](https://www.doctrine-project.org/projects/doctrine-orm/en/3.5/reference/batch-processing.html), [DQL](https://www.doctrine-project.org/projects/doctrine-orm/en/3.5/reference/dql-doctrine-query-language.html), [pagination](https://www.doctrine-project.org/projects/doctrine-orm/en/3.5/tutorials/pagination.html).

## Pagination and indexes

For to-many fetch joins, ordinary LIMIT/OFFSET can truncate root results or their collections. Use a supported Doctrine Paginator strategy or separate root-ID paging/fetching; inspect the generated SQL and counts rather than assuming a fixed two-query plan. For keyset traversal on a nonunique timestamp, include a stable unique tie-breaker and seek on the corresponding ordered tuple. Use suitable composite indexes and bound page sizes. Measure database plans/query count; keyset cost is not guaranteed constant for every filter/index.

Use bounded existence queries where only existence is needed. ORM persist/flush batching limits unit-of-work memory; it does not imply JDBC-style SQL multi-row inserts. Use the DBAL/database bulk path deliberately when that behavior is needed.
