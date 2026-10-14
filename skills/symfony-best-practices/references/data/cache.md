# Application and HTTP cache

Read for symfony-cache. Decide the freshness, isolation and invalidation contract before picking a backend.

## Pools and values

Cache expensive reads/computations whose staleness is acceptable. Use the existing named pool and the deployment-appropriate adapter. APCu/filesystem state is local to a process/host topology; shared Redis can coordinate instances. Do not introduce infrastructure without a concrete need.

Prefer scalar arrays/DTO projections over managed entities/proxies or serialized services. Include every input that changes the result in the key: resource/query/version and, when relevant, tenant, user, locale and permission context. Hash canonicalized variable inputs to satisfy backend key restrictions and avoid leaking sensitive identifiers. A hashed key alone does not make globally cached personalized data safe.

## TTL and invalidation

Use an explicit TTL matching permitted staleness or a justified immutable/versioned-key policy. TTL alone does not satisfy immediate invalidation after a write or permission change. Specify which committed writes invalidate which entries/tags, and who owns that action.

Use `CacheInterface::get()` with a callback for read-through computation. Tag-based invalidation requires a tag-aware pool and `TagAwareCacheInterface`; ordinary PSR-6 pools do not gain tags automatically. An individual key can be deleted without tags. Invalidate after a successful write under the application's transaction/outbox policy, considering the stale-repopulation race if coherence matters.

Cache Contracts provide locking and probabilistic early expiration to reduce stampedes. Verify the adapter/topology and recomputation latency; a process-local lock is not proof of cross-host coordination. Async recomputation requires the actual callback/handler and worker integration, not just changing a beta value. Do not claim early expiration always serves stale data with zero request latency.

## HTTP cache

Private user-specific responses must not be shared across users/tenants. Choose `private`/`no-store`, validators or `Vary` deliberately according to the response's sensitivity and intended cache behavior. Application cache keys and reverse-proxy/CDN caching are separate controls. Do not mark authenticated dashboard responses public by copying a generic HTTP-cache example.

## Verification

Test cache miss/hit, expiration, intended key/tag invalidation and cross-user/tenant isolation. Test permission changes and post-commit invalidation where required. Measure hit rate/recomputation and stampede behavior under representative concurrency when performance is the goal.

Use pool inspection through the project runner. `cache:pool:clear` and `cache:clear` mutate state and can cause cold starts or reset limiter/schedule state: scope them to the requested environment/operation. Do not clear every shared pool as routine diagnosis.

Primary guidance: [Symfony Cache and invalidation](https://symfony.com/doc/8.0/cache.html), [HTTP cache](https://symfony.com/doc/8.0/http_cache.html).

## Session and reverse-proxy boundaries

Session reads, flashes and stateful CSRF can turn otherwise anonymous-looking pages private. Keep that safeguard for personalized output; inspect [sessions](../http/sessions.md) before changing it. Test freshness/304/Vary and actual proxy behavior with [deployment and HTTP caching](../workflow/deployment-and-performance.md).

Reviewed current-line sources: [Cache](https://symfony.com/doc/8.1/cache.html), [HTTP cache](https://symfony.com/doc/8.1/http_cache.html).
