# Application architecture and dependency injection

Read for controller-cleanup, cqrs-and-handlers, interfaces-and-autowiring, ports-and-adapters, strategy-pattern, value-objects-and-dtos, and layered-architecture.

## Thin entry points

Controllers and console commands adapt input, validate/authorize, call a use case, and adapt its outcome. Move business decisions and reusable orchestration into focused services; put query details in repositories/read services. Preserve status codes, response shape, validation errors and CLI exit behavior when refactoring. Line counts are review signals, not hard acceptance criteria.

For structured JSON input, a typed input DTO plus `#[MapRequestPayload]` can connect serializer and Validator; define the route's JSON format and test invalid input. Mapping is not authorization. Forms and simple routes need not gain a DTO layer merely to satisfy a pattern. Explicit output DTOs are useful for stable API boundaries; do not silently replace an existing serialization contract.

On the Symfony 8.0 baseline, invokable `#[AsCommand]` classes are available. Keep an existing `Command::execute()` implementation when that is clearer or required by the project. Delegate both HTTP and CLI paths to the same use case when they perform the same business operation.

## Services and interfaces

Use constructor/action injection, autowiring and autoconfiguration. Avoid arbitrary container lookups that hide dependencies. A purpose-built Symfony service locator for a keyed collection is appropriate when that collection is the dependency.

An interface is valuable at a replaceable external boundary or where multiple implementations are needed; a single ordinary service can be injected directly. With ambiguous implementations, declare an explicit alias, or select a named alias through `#[Target]`. Inspect `debug:autowiring <Type>` and `debug:container <service>` through the project runner. Use `#[Autowire]` for deliberate scalar/service binding and `#[AsDecorator]` for behavior wrapping where appropriate.

Keep stateless dependencies `private readonly` when suitable and follow the project's `final` convention. Do not mark ORM entities, framework-hydrated props, or intentionally stateful services readonly/final without checking their lifecycle.

## CQRS and handlers

Separate commands that change state from queries that return data when it clarifies use cases. Multiple buses, dedicated read models and an async transport are separate choices; CQRS does not require them all. An ordinary application service is sufficient for simple CRUD.

If buses exist, inspect their middleware and handler routing. Query results require synchronous handling: `HandleTrait`/`HandledStamp` or a direct query service cannot produce an async worker's future result. A command handler owns the write use case; define one transaction boundary, avoiding an extra flush if `doctrine_transaction` already owns it. One handler per command/query is a design convention; Messenger events may deliberately have multiple handlers.

Publishing a message and committing business data are not automatically atomic. Use the project's outbox/after-commit contract where reliable publication is required; see [Messenger](../async/messenger.md).

## Ports, adapters, and strategies

For a domain with substantive rules and swappable infrastructure, place contracts with the consumers that own them; dependencies point toward the domain/application. A strictly pure domain does not import Symfony, Doctrine or provider SDKs; use adapters and supported external mapping where that purity is the chosen architecture. Existing Doctrine attribute entities in a CRUD module do not require wholesale conversion to XML or new layers.

For interchangeable algorithms, use a focused strategy contract and explicit selection. `#[AutoconfigureTag]` plus `#[AutowireIterator]` supports ordered candidates; a tagged locator supports keyed access. Define priority, duplicate-key/ambiguity behavior, no-match behavior and an intentional fallback. A two-case stable `match` need not become a strategy registry.

## Value objects and DTOs

A value object models a domain concept, enforces its invariants, compares by value and returns new values from operations. A DTO carries data across a boundary; validate input constraints using the boundary's normal error mapping. PHP readonly is shallow: mutable objects stored inside it can still change.

Store monetary amounts as integers in the currency's minor units or an explicit decimal representation, with currency and rounding rules; do not assume every currency has two fractional digits. Doctrine embeddables/custom types are persistence options, not a requirement for every value object. Separate input/output DTOs when their contracts differ; avoid heavy DTO constructor exceptions that bypass the intended validation response.

## Verification

Use plain unit tests for rules, container/integration checks for aliases/decorators/tag selection and repository adapters, and functional tests for retained HTTP/CLI behavior. Test invalid value-object inputs, equality, unsupported strategy and sync query returns. Verify architectural boundaries only for modules that adopt them.

Primary guidance: [best practices](https://symfony.com/doc/8.0/best_practices.html), [controllers](https://symfony.com/doc/8.0/controller.html), [DI](https://symfony.com/doc/8.0/service_container.html), [tags](https://symfony.com/doc/8.0/service_container/tags.html), [multiple buses](https://symfony.com/doc/8.0/messenger.html).

## Layer and mapping choices

Keep transport-specific Request/Response/Console types at adapters, business orchestration in application use cases, and query/persistence details in data-access adapters. Entity/output mapping may use a DTO factory or a dedicated mapper when useful; do not impose one service per aggregate, one service call per endpoint, or a mandatory pass-through service on simple reads. Internal DBAL rows can be valid data-access results when mapped deliberately at the public boundary.

Use [Bundle organization](bundle-organization.md), [Console](console-commands.md), and [REST](../http/rest-api.md) for their specific lifecycle/contracts. Domain invariants still belong in the domain, even when request-shape constraints live on input DTOs.
