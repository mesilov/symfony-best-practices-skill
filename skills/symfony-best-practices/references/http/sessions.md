# Sessions, cookies, and stateful HTTP

Read when using login sessions, flashes, CSRF, user preferences, concurrent browser requests or public HTTP caching. Pair with [authentication](../security/authentication.md) and [cache](../data/cache.md).

A session starts lazily when it is read, written, or checked for data. Reading a flash or using a stateful CSRF token can start it too. Inject RequestStack at the HTTP adapter boundary and obtain the session only when needed; account for requests/CLI paths without a session. Do not put request/session state in shared services or call session APIs from domain objects.

## Caching and cookies

Starting a session normally makes the response private/non-cacheable for shared caches. Trace session access in the profiler before marking a page public. Do not disable that safeguard for personalized responses. Separate anonymous cacheable output from authenticated/personal output; test the actual Set-Cookie/Cache-Control behavior, including template flashes, fragments and CSRF forms.

Use appropriate secure, HttpOnly and SameSite cookie settings with a correct HTTPS/trusted-proxy setup. SameSite is one layer, not a substitute for the CSRF policy. Session-ID migration on authentication and invalidation/logout must match Security's lifecycle; do not disable fixation protection for convenience. Avoid logging session IDs or using them as business identifiers.

## Storage and concurrent requests

Choose a session handler/store supported by the deployment topology and failure contract. Shared deployments need appropriate shared persistence or an explicit affinity strategy. Cookie lifetime, storage TTL and garbage collection are separate; increasing one does not guarantee a longer authenticated session. Test expiry/logout and deployment behavior.

Handler locking differs. Symfony's RedisSessionHandler does not provide session locking; concurrent read-modify-write requests can overwrite each other. Do not use a session as a transactional shopping cart, balance or idempotency ledger. Put correctness-critical state in a store with explicit concurrency control. For long requests, release/save a session when the chosen handler/flow permits it and do not continue writing stale session state afterward.

Test two real requests sharing a cookie for persistence, logout and flashes; add concurrent requests when state can race. A mocked SessionInterface does not prove handler TTL, locking, cookies or HTTP cache safety.

Source: [Symfony sessions](https://symfony.com/doc/8.1/session.html).
