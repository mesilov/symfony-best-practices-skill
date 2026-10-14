# Logging, diagnostics, and error pages

Read for operational evidence, exception reporting and safe production responses. Pair with [REST/RFC 9457](../http/rest-api.md), [Messenger](../async/messenger.md), and [deployment](deployment-and-performance.md).

Inject a PSR LoggerInterface or the project's named channel. Use structured context with stable fields (operation, correlation/message ID, safe business key) and appropriate levels. Keep request IDs/correlation IDs distinguishable from authenticated identity. Validate externally supplied correlation data and constrain size. Never log passwords, access/session tokens, raw Authorization headers, decrypted configuration or unrestricted request/message bodies.

Inspect installed Monolog channels, handlers, processors, buffering and environment configuration before adding a handler. A channel selects routing; a processor enriches records; a handler writes/forwards them. Ensure production output reaches the actual collector with retention/access controls. A debug log written locally does not establish production observability.

Long-running workers can retain buffered log records/context between jobs. Verify the existing reset/flush lifecycle, including failure paths, before adding mutable processors or memory-buffered handlers. Do not retain tenant/user state across messages. Capture useful diagnostics while keeping sensitive business payloads out of failure transports and verbose reports.

## HTTP failures

Production must run with debug disabled. Customize supported Twig error templates/error renderer according to the response format; HTML error pages do not define JSON API errors. Keep safe status/message behavior, existing authentication entry points and protocol headers. Log internal exceptions with a correlation ID while returning a safe response. Do not turn every Throwable into 200/400 or expose exception class, trace, SQL, filesystem path or provider body.

Preview/test error pages in an appropriate non-debug test environment. Test the real exception listener/error renderer path for 404/403/500 and the API contract separately. Debug toolbar/profiler visibility in development does not prove safe production configuration. An exception raised while rendering an error page needs a tested fallback.

Test emitted log level/channel/context with sensitive-field assertions when changed; test actual handler wiring if routing is the change. Logging failure must not silently change a transaction/payment contract. Observability records outcomes but does not provide idempotency or durable execution.

Sources: [logging](https://symfony.com/doc/8.1/logging.html), [error pages](https://symfony.com/doc/8.1/controller/error_pages.html).
