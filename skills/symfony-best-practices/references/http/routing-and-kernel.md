# Routing, controllers, and HttpKernel

Read when matching/generating URLs, changing request listeners, controller arguments, or response behavior. Pair with [REST errors](rest-api.md) and [container/events](../architecture/container-and-events.md).

## Routing and controller contracts

Use the project's route format; attributes are a suitable default for new controller routes. Give routes stable names and explicit HTTP methods. Constrain dynamic placeholders so `/articles/{slug}` cannot swallow a static endpoint such as `/articles/search`; verify order/priority and requirements with `debug:router` and `router:match` through the project runner. Optional placeholders must form a trailing chain; defaults and input validation have different purposes.

Host, scheme, locale, prefix and parameter requirements affect matching/generation. Route conditions affect matching **only**; URL generation does not evaluate them. Generate links with the router and encode parameters; do not assemble paths from untrusted strings. For CLI/worker absolute URLs, configure the intended request context/default URI instead of trusting an absent HTTP request or a caller's Host header. Review trusted hosts/proxies with deployment configuration.

Controllers translate input, authorize, delegate, and build a Response. Use typed argument resolvers/DTO mapping supported by the installed minor. Missing entities and mapping/validation failures have observable status codes; preserve the declared contract. Avoid exposing ORM entities through automatic serialization. Keep streamed/file responses, redirects and downloads on supported response APIs with explicit headers and safe file ownership/path checks.

## Lifecycle and request boundaries

HttpKernel dispatches `kernel.request`, resolves the controller, dispatches `kernel.controller`, resolves arguments, and dispatches `kernel.controller_arguments`. It invokes the controller; a non-Response result needs a `kernel.view` listener or is an error. It then dispatches `kernel.response` and `kernel.finish_request`. Exceptions take the `kernel.exception` path; a listener can supply a response. Some early responses skip controller stages. Event priorities and propagation determine which listeners run.

A subrequest is another traversal, not a separate authenticated client request. Check `isMainRequest()` when policy is intended only for the main request. When subrequests matter, test both paths; do not accidentally replace fragments' content or run an audit action twice. Services are shared by default: do not retain a tenant, user, Request or response-derived state across requests/jobs. Prefer passing context explicitly; stateful services need a verified reset lifecycle in persistent runtimes.

Use request attributes for per-request metadata with a collision-safe key and validated origin. A caller-controlled tenant value does not establish tenant access. Inspect listeners with `debug:event-dispatcher` and verify their ordering against Security, routing and error handling. Use `kernel.terminate` only for work whose execution/loss contract allows it; it is not a durable queue or a guarantee of work after every response.

## Verification

Test competing static/dynamic routes, method mismatch, parameter requirements, locale/host generation and the CLI absolute URL context. For listeners, test early responses, main/subrequests, exception responses and consecutive requests/jobs with different actors/tenants. A controller unit test does not exercise the kernel event chain.

Sources: [routing](https://symfony.com/doc/8.1/routing.html), [controllers](https://symfony.com/doc/8.1/controller.html), [HttpKernel](https://symfony.com/doc/8.1/components/http_kernel.html). Version-specific APIs such as controller metadata must be checked against installed packages.
