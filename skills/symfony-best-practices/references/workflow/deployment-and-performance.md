# Deployment, performance, and HTTP caching

Read when preparing a release, changing production configuration or optimizing a measured bottleneck. Pair with [configuration](configuration.md), [migrations](../data/migrations.md), [cache](../data/cache.md), and [Messenger](../async/messenger.md).

## Release preparation

Follow the project's existing build/release pipeline and verified runner. Install from the committed lock file (`composer install` with project production options), rather than resolving new dependencies with `composer update` on production. Build frontend assets through the established pipeline. Set production environment/debug explicitly, provide required runtime secrets safely, and prepare/warm the container/cache for the intended release/environment.

Separate build-time and runtime inputs; ensure paths, generated assets, env dumps and permissions match the target topology. Review database migration SQL and compatibility with both old and new application/worker versions during rollout. Cache warming, migrations and traffic switch must have a defined order. Plan rollback around database/configuration/message compatibility; swapping application files does not reverse every migration or external side effect.

Persistent PHP workers, Messenger/Scheduler consumers and other services need supervised, graceful restarts appropriate to their runtime. Verify old workers drain/stop and replacements are healthy. `cache:clear` via CLI does not reset PHP-FPM's OPcache; use the deployment's actual FPM/OPcache restart/reset mechanism. If OPcache timestamp validation is disabled, changed code requires an explicit refresh. Inspection or a suggested runbook does not authorize executing production changes.

Verify health, relevant business smoke checks, errors and worker backlog after an authorized deployment. A successful archive/build or local cache warmup proves neither a deployed release nor a working provider integration.

## Measure before tuning

Profile the actual bottleneck with representative data and an appropriate environment: queries, serializer/template work, HTTP calls, container boot, memory and queue latency. Compare a baseline and a changed measurement; do not enable profiler/debug in public production to measure casually. Apply production debug=false, appropriate Composer autoload and OPcache configuration through the established runtime. Preloading/JIT/locale reduction/cache topology are workload and deployment choices, not universal speed switches.

## HTTP cache contract

Use explicit freshness/validation semantics for safe GET/HEAD representations. ETag/Last-Modified validators can produce 304; test conditional requests and correct representation/authorization. Distinguish browser `max-age` and shared-cache `s-maxage`; use `private` or `no-store` as required for sensitive/personal data. A session typically makes a response private. Do not force a public response merely to improve a hit rate.

`Vary` declares request-header representation dimensions; include all relevant variants without creating unbounded keys. Authorization, cookies, locale and tenant boundaries must remain safe in the selected proxy/CDN. Confirm invalidation and trusted-proxy behavior in the actual topology. HTTP response caching, application Cache pools and OPcache are different mechanisms with separate invalidation/restart contracts.

Test status/body/headers for anonymous and authenticated users, two tenants/locales, conditional requests and stale/invalidation behavior. A unit test of a cache callback does not verify reverse-proxy response caching.

Sources: [deployment](https://symfony.com/doc/8.1/deployment.html), [performance](https://symfony.com/doc/8.1/performance.html), [HTTP cache](https://symfony.com/doc/8.1/http_cache.html).
