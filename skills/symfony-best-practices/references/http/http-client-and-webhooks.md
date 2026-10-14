# HTTP clients and webhooks

Read for outbound APIs, callback endpoints, retries, SSRF boundaries and provider integration. Pair with [Messenger](../async/messenger.md), [authentication](../security/authentication.md), and [REST errors](rest-api.md).

## Outbound HTTP

Inject HttpClientInterface or an existing scoped client. Centralize base URI, credentials and bounded transport settings; keep secrets out of logs and cross-host redirects. Preserve peer/host TLS verification. User-controlled destinations need explicit protocol/host/port and redirect policy plus private-network protection; use NoPrivateNetworkHttpClient when appropriate. Check installed support before relying on its 8.1 allowlist argument. An allowlist must not accidentally exempt arbitrary user URLs.

Responses are lazy: exceptions can arise when reading status, headers/body, decoding, or during response cleanup/destruction. Explicitly consume/handle the response and its status; do not assume `request()` returning proves success. Understand which `getHeaders()`, `getContent()` and `toArray()` calls throw on HTTP errors and which opt out. Avoid swallowing transport/decode failures as an empty successful result.

Set both idle `timeout` and total `max_duration` according to the operation; also bound response size and concurrency. Stream large bodies rather than buffering them unconditionally. A 429/503 Retry-After may inform a bounded retry policy; retries for writes require a stable provider idempotency key or an explicit safe contract. A timeout can mean the provider succeeded and the response was lost. Reconcile that state; a local transaction cannot roll back a remote effect. Do not stack unbounded HTTP and Messenger retries.

Use MockHttpClient/MockResponse for request/status/body/error behavior. Separately verify actual DNS/TLS/proxy/timeout/provider semantics when those are material; mocks do not establish connectivity.

## Incoming webhooks

Use the installed provider RequestParser and RemoteEvent/consumer flow where it fits. Configure the production secret: some provider parsers skip signature verification when it is absent. Verify the signature over the exact raw bytes required by that provider before transforming/normalizing content. Validate timestamp/freshness, expected event/account identity and replay rules; IP filtering is supplementary, not signature verification.

Record a durable unique provider event ID or equivalent replay key atomically. Test concurrent duplicates and crash/retry paths. Signature validity does not grant a callback arbitrary tenant/resource access. Acknowledge only after the event is durably accepted according to the provider's retry contract; an async 2xx acknowledgement does not mean business processing completed. Keep business work recoverable in the worker and bound permanent/transient retries.

Test a real signed fixture including exact bytes, invalid/missing signatures and secrets, stale timestamps, duplicate deliveries, tenant mismatch and worker failures. Do not substitute a parsed JSON-body test for signature-byte verification. Outbound webhook endpoints need the same destination, signing, retry and idempotency analysis as other HTTP integrations.

Sources: [HttpClient](https://symfony.com/doc/8.1/http_client.html), [Webhook](https://symfony.com/doc/8.1/webhook.html).
