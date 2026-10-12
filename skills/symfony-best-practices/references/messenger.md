# Messenger, retries, and failure handling

Read for symfony-messenger and messenger-retry-failures; read [architecture](architecture.md) for CQRS/multiple buses.

## Messages and routing

Use small serializable message contracts with scalar IDs and stable business/event keys; re-fetch current entities in a typed `#[AsMessageHandler]` handler. Do not serialize managed Doctrine entities/proxies or secret payloads. Preserve message compatibility when old queued messages can survive a deployment.

Inspect existing buses, middleware, serializer and transport configuration. YAML routing is available on the 8.0 baseline; choose attributes/options only when supported by the installed minor. Define which messages are synchronous and which are asynchronous. An in-memory transport tests routing/envelopes; it does not prove broker delivery, redelivery or durable serialization.

```yaml
framework:
    messenger:
        failure_transport: failed
        transports:
            async:
                dsn: '%env(MESSENGER_TRANSPORT_DSN)%'
                retry_strategy:
                    max_retries: 3
                    delay: 1000
                    multiplier: 2
                    max_delay: 30000
            failed: 'doctrine://default?queue_name=failed'
        routing:
            App\Message\RebuildReport: async
```

This is an illustrative policy, not a replacement for the project's transports. Three retries mean up to four attempts in the configured retry sequence, including the initial attempt; broker redelivery and concurrent duplicates can add deliveries outside that sequence. Review infrastructure timeouts/redelivery settings and access to the failure store.

## Idempotency and atomicity

Assume redelivery and concurrent duplicates. A read-then-check status followed by work is not race-safe. Use a stable business idempotency key, a real unique constraint/atomic claim and a documented state machine with recovery for abandoned claims. Test duplicate concurrent deliveries.

DB transactions cannot roll back a successful external HTTP side effect. Use the same provider idempotency key on retries and reconciliation when the outcome is unknown. Local deduplication alone cannot guarantee one provider effect across a crash after the provider succeeds but before the local commit. Keep remote calls outside DB locks/transactions, and record intent/result in short transactions. Use an outbox when data changes and message publication must be recoverable together; ordinary bus dispatch plus flush does not establish atomicity.

## Failure classification

- Ordinary retryable exception: transport retry strategy controls the finite budget/backoff; use this for bounded transient failure handling.
- `UnrecoverableMessageHandlingException`: prevents normal retries; with a configured failure transport, the failed message can still be retained there.
- `RecoverableMessageHandlingException`: on Symfony 8.0 it **forces retries and ignores `max_retries`**. Do not use it for a bounded retry contract. Its `retryDelay` argument is available on the 8.0 baseline; that delay alone does not restore the budget. Check the exact installed signature/strategy before using later controls such as `forceRetry`.

Treat invalid requests/permanent business declines differently from provider downtime, 429, timeouts and unknown outcomes. Use bounded exponential backoff/jitter and provider Retry-After according to the actual policy. A custom `RetryStrategyInterface` is appropriate when built-in policy cannot express the contract; test its budget/delay logic including forced-retry exceptions. Never classify every failure as recoverable.

## Workers and failed-message runbook

Through the verified runner, inspect `debug:messenger`, transport stats and installed command help. An authorized worker can use `messenger:consume <receiver>` with relevant time/memory/message limits under the project's process supervisor. Consuming shared queues performs application work: inspection does not authorize it. Restart workers on deployment through the established `messenger:stop-workers` lifecycle; inspect stateful services and their reset behavior.

Inspect failed messages with `messenger:failed:show` before an explicitly scoped `retry` or `remove`. Verbose payloads may contain personal data/secrets; redact output. Removal is data loss and retry can repeat an external effect: identify the message, root cause and idempotency/recovery status. Do not replay the entire store as routine diagnosis.

Monitor processing/final failures, retries, backlog, age and relevant business outcomes. `WorkerMessageFailedEvent::willRetry()` can distinguish scheduled retry from final failure in the installed version.

## Verification

Test handler success, permanent/transient failure, finite retries and failure transport; then concurrent duplicates, crash/restart and provider-unknown outcomes where effects matter. Separately identify in-memory tests and actual transport integration. Verify message serialization and old-payload behavior when changing a contract.

Primary guidance: [Symfony 8.0 Messenger](https://symfony.com/doc/8.0/messenger.html), especially retries, idempotent handlers, worker lifecycle and middleware order. Inspect the installed component source for later minor-version APIs.
