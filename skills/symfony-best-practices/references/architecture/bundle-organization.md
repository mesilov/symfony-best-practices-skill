# Application modules and reusable bundles

Read for bundle-organization and layered-architecture. Start with the established layout and ownership of each capability.

## Application structure

A modern Flex application normally keeps its code under `src/` and `App\`; it does not need an application AppBundle. Flat technical directories remain suitable for small applications. For a larger domain, organize by cohesive features/modules, then introduce Domain/Application/Infrastructure/UI boundaries only when they clarify responsibility and independent change.

Use the layering model already selected by the project. A module owns a business capability; a layer expresses a technical responsibility. Avoid a large Shared module that imports every feature or silently couples modules. Cross-module interaction should use explicit application contracts/events rather than unrelated entity/repository internals. New CQRS buses, XML mapping and repository ports are independent decisions; see [Architecture](architecture.md).

Application configuration stays in `config/`: package configuration, routes/imports, environment overrides, service wiring and bundle registration. When a class moves, update namespace/autoload, service resources, controller route imports, Doctrine mapping discovery, templates and tests together. A directory move alone does not preserve behavior.

## Autodiscovery

Prefer autowiring/autoconfiguration and configure deliberate exceptions. Exclude plain entities, value objects, input DTOs and other data-only objects from service autodiscovery where needed. **Do not exclude all Domain code** if it contains actual services used by the application. Resolve ambiguous interfaces through explicit aliases and verify relevant service registrations.

## Reusable bundles

Create a bundle for shareable library capabilities with their own configuration/integration lifecycle. Do not convert application modules into bundles merely to group files. Use supported `AbstractBundle` configuration/load APIs for the installed version. Keep reusable code independent of the consuming application's namespace, containers, connection names and filesystem paths; declare dependencies and configurable integration points explicitly.

Verify the bundle's default/invalid configuration, service/route loading and behavior in a minimal consuming application. For an application-only reorganization, run container/router/mapping checks and existing behavior tests; confirm that POJOs are excluded without removing required services.

Primary guidance: [Symfony best practices](https://symfony.com/doc/8.0/best_practices.html), [bundle best practices](https://symfony.com/doc/8.0/bundles/best_practices.html), [bundle extension](https://symfony.com/doc/8.0/bundles/extension.html).
