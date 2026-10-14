# Authorization and rate limiting

Read for symfony-voters, rate-limiting, and security-authentication. For identity, read [Authentication](authentication.md); for input validity, read [Validation and forms](../http/validation-and-forms.md).

## Voters

Define an actor/resource/action decision matrix including anonymous users, owner, other tenant, privileged user and unsupported subject/action as applicable. Implement `supports()` and `voteOnAttribute()` with explicit decision logic, then enforce it via `#[IsGranted]`, controller/service boundary checks or the existing API integration.

Read the configured access-decision strategy: affirmative, unanimous, consensus or priority can change how multiple voters combine. An abstention is not a deliberate deny. Use `AccessDecisionManagerInterface` with the token passed into a voter for role decisions; avoid a new global `Security::isGranted()` decision that can use different token context or recurse.

Validate authorization in the use-case path that needs it; hiding a button is not enforcement. Avoid leaking privileged resource existence/data through error details. Keep policy logic consistent across HTTP, CLI and async entry points according to their explicit actor context.

## Rate limiting

Choose fixed/sliding window, token bucket or compound policy to match rate/burst requirements. Identify the caller using trusted authentication/tenant context or correctly trusted proxy-derived IP. Normalize/hash sensitive identifiers for keys. Use shared persistent storage/coordination when several instances must share the budget; changing/clearing limiter cache can reset the budget.

On the 8.0 baseline, inject `RateLimiterFactoryInterface`; `#[Target('limiter_name')]` selects a configured named factory. Call `create($identity)->consume()` and translate refusal to **429 plus Retry-After**, using a nonnegative delay from the returned retry time. Do not sleep a request worker waiting for tokens as the default web policy.

Symfony's application RateLimiter is **not DDoS protection**: PHP must run before it rejects a call. Edge/proxy/CDN limits are an independent infrastructure concern when relevant to the task. Do not assume an 8.1 controller attribute or new limiter option exists on 8.0; verify before use.

## Verification

Test valid/invalid form submissions and transformation errors, CSRF behavior where applicable, the allow/deny matrix and cross-tenant cases, and accepted/refused/reset/concurrent rate-limit requests. Use the real DB for uniqueness races. Check trusted-proxy behavior and rate keys under the intended deployment topology; mocks do not prove distributed storage.

Primary guidance: [forms](https://symfony.com/doc/8.0/forms.html), [validation](https://symfony.com/doc/8.0/validation.html), [voters](https://symfony.com/doc/8.0/security/voters.html), [rate limiter](https://symfony.com/doc/8.0/rate_limiter.html).
