# Scheduler and recurring work

Read for symfony-scheduler (the requested symfony-schedu path is an upstream path typo).

## Define the contract

Use the existing scheduler/cron mechanism unless the task asks to change it. Symfony Scheduler and its Messenger transport are available on the 8.0 baseline. Confirm installed Scheduler, Messenger, cache/lock services and cron-expression support.

Implement `ScheduleProviderInterface` with `#[AsSchedule('name')]`, returning a memoized `Schedule` containing `RecurringMessage::every()` or `RecurringMessage::cron()`. State the exact timezone for cron and test DST boundaries when relevant. The receiver is `scheduler_<name>`; a provider definition alone does not run jobs. The consumer/process supervisor must actually be configured.

## Downtime and coordination

Choose what happens during downtime: skip missed runs, catch up all, or keep only the most recent. `stateful($cache)` remembers schedule state; `processOnlyLastMissedRun(true)` changes catch-up behavior on the 8.0 baseline. Statefulness does not prove that the handler's external work completed successfully.

Use a stable shared cache when state must survive worker restarts or span instances. A schedule `lock(...)` with a shared lock store coordinates competing schedule consumers. A single scheduler consumer is the simplest topology when adequate; scaling with appropriate coordination is possible and is not categorically forbidden.

A scheduler lock does not automatically prevent overlapping business work once jobs are redispatched to an async queue. If overlap matters, implement a job/use-case lock or atomic claim, defined lease/expiry/renewal and a recovery policy. Derive deduplication keys from the business job/period where that is the intended contract. Scheduled work remains idempotent under retries/redelivery.

For expensive handlers, consider `RedispatchMessage` to an existing async transport so scheduling is not blocked by long processing. Capacity, interval, retry policy and overlap handling must fit together; a queue is not a guarantee of timely completion.

## Verification and operations

Use `debug:scheduler` and `debug:messenger` through the verified runner to inspect definitions without starting shared consumers. Start `messenger:consume scheduler_<name>` only in the authorized environment, under the established lifecycle and limits.

Test next-run times/timezone, empty schedule, downtime catch-up choice, repeated invocation, multi-consumer coordination and overlap of async execution where applicable. Use controllable clocks in tests rather than waiting for wall-clock cron. Monitor job start, completion, duration, errors and stale/abandoned work; schedule emission and business completion are different evidence.

Primary guidance: [Symfony 8.0 Scheduler](https://symfony.com/doc/8.0/scheduler.html), [Lock](https://symfony.com/doc/8.0/lock.html), [Clock](https://symfony.com/doc/8.0/components/clock.html).
