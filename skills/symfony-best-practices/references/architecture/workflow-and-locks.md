# Symfony Workflow and Lock components

Read for business state transitions, shared-resource coordination and scheduled/job overlap. This concerns Symfony's Workflow component; the `workflow/` reference group concerns development/operations. Pair with [Doctrine transactions](../data/doctrine-modeling.md), [Messenger](../async/messenger.md), and [Scheduler](../async/scheduler.md).

## State transitions

Choose a state machine for a single current place, or a workflow for multiple concurrent places. Define places/transitions, marking store, guards and required persistence according to the business contract. Match the marking representation to storage: multi-place markings need a suitable mapping such as JSON, not a string/simple-array assumption. Check the installed minor for newer transition/marking options.

`can()` checks the current marking and guards; it does not reserve the transition. A concurrent request can change the subject before `apply()`/flush. Guard+apply+persist need an explicit concurrency strategy (optimistic version, row lock/transaction or atomic conditional update) appropriate to the store. Re-fetch/retry deliberately on conflicts and test simultaneous transitions.

Guards can be evaluated more than once, including availability/announce checks. Keep them free of external effects and avoid assuming one evaluation equals one transition. Transition events/listeners execute synchronously unless explicitly queued; sending a payment/email from a listener is not rolled back by a later DB failure. Persist state and publish effects through a reliable delivery contract.

Test valid/invalid transitions, guard reasons, persisted/reloaded marking, concurrent attempts and event effects. Workflow definitions do not enforce all domain invariants automatically.

## Shared locks

Choose a lock store shared by all participating processes/hosts; a local filesystem/semaphore store does not coordinate a multi-host deployment. Review TTL, refresh, serialization, blocking and ownership support of the actual store. Treat failure to acquire as an expected branch with defined retry/skip behavior.

Acquire, enter the protected section only on success, and release in `finally` through the same ownership/key contract. A lease can expire during work: set a realistic TTL, renew it when supported, and stop or recover if ownership is lost. A five-second lease does not protect a twenty-minute job by itself. `isAcquired()` describes ownership of this lock instance, not a global query for any process's lock.

A lock does not supply database constraints, durable idempotency or exactly-once delivery. Handle process death, lease expiry and concurrent retries in the underlying state transition/side-effect design. Cache clearing can remove locks if the selected backing storage overlaps; isolate infrastructure and inspect operational commands before clearing it.

Test acquisition contention, TTL expiration/renewal, lost ownership, exceptions/release and the actual shared store when correctness depends on it.

Sources: [Workflow](https://symfony.com/doc/8.1/workflow.html), [Lock](https://symfony.com/doc/8.1/lock.html).
