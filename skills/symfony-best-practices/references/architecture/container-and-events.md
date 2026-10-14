# Container, kernel configuration, and events

Read for service registration, autowiring, framework extensions and request/job lifecycle hooks. Pair with [architecture](architecture.md), [configuration](../workflow/configuration.md), and [routing/kernel](../http/routing-and-kernel.md).

## Dependency injection

Use constructor injection and private services. Autowiring resolves types; autoconfiguration adds supported tags/interfaces. Neither invents a choice between competing implementations: use explicit aliases, bindings or installed attributes when that choice is ambiguous. Keep environment/configuration values typed at the boundary. Inspect `debug:container`, `debug:autowiring` and effective configuration before adding service-locator access.

Honor the project's resource/exclude rules. Avoid registering entities, DTOs, tests or every file as a service accidentally. Use tagged iterators/locators for intentional plugin sets; define tag/index/priority and duplicate handling. Service decoration preserves an existing contract while adding behavior; test order and the decorated inner service. Do not make all services public to silence a wiring error.

Do not capture Request/user/tenant state in a constructor of a shared service. Inject RequestStack only at a real HTTP boundary, handle the absence of a request in CLI, and keep domain logic independent of it. Inspect reset behavior for workers/persistent HTTP runtimes; container lifetime is not request lifetime.

## Kernel and configuration

The Kernel selects environment/debug, bundles and configuration and builds the container. Use the existing MicroKernel/configuration conventions. Understand `kernel.project_dir`, cache/build/log directories and environment-specific imports before changing paths or permissions. Use `debug:config`, `config:dump-reference`, container/YAML/Twig lint commands when relevant; do not guess a configuration key from another minor.

Build-time configuration and runtime environment resolution differ. A compiled container, dotenv dump or warmed cache belongs to its release/environment contract. Do not read request state while compiling services or assume changing an env file updates already-running workers. Keep build and runtime configuration consistent with [deployment](../workflow/deployment-and-performance.md).

## Events

Use a listener/subscriber for a real extension point with a clear event type and owner. `#[AsEventListener]` and EventSubscriberInterface are alternatives; follow existing registration rather than registering both and executing twice. Inspect priorities, propagation and dispatch timing. Dispatching an event is synchronous unless a separate Messenger path explicitly makes work asynchronous.

Observers should not hide mandatory business steps or change the transaction contract silently. Use an explicit application service when the caller needs the result. Separate domain events from HttpKernel hooks. Exceptions in listeners affect the caller; database rollback cannot undo an external email/HTTP effect. Use post-commit delivery/outbox when required, as described in [Messenger](../async/messenger.md).

Test actual container compilation/autowiring for changed wiring, and event delivery/order/absence for changed listeners. Include failure and worker-reset paths when state or side effects matter.

Sources: [service container](https://symfony.com/doc/8.1/service_container.html), [EventDispatcher](https://symfony.com/doc/8.1/event_dispatcher.html), [kernel parameters](https://symfony.com/doc/8.1/reference/configuration/kernel.html).
