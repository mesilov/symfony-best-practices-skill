# Forms, validation, authorization, and rate limits

Read for form-types-validation, symfony-voters, and rate-limiting. These are different boundaries: input validity does not grant access, and a rate limit does not grant a permission.

## Forms and input validation

Declare explicit form field types and map only intended writable fields. Place reusable constraints on input models/domain data; keep UI-only constraints on the form. Select validation groups for differing use cases rather than duplicating constraints. A data transformer rejects unconvertible values with `TransformationFailedException`; listeners belong only where input/model adaptation requires them.

Handle the request and check `isSubmitted() && isValid()` before delegating to business work. On the 8.0 baseline, passing the Form object directly to the standard controller `render()` supports 422 for an invalid submitted form. Passing a prebuilt view or a custom response may use a different contract; assert the actual status. Use an appropriate redirect after successful browser writes.

Keep CSRF enabled for browser forms where applicable; stateless APIs need their chosen authentication/request protection contract. Validate uploaded content, size and storage rules at the appropriate boundary. `UniqueEntity` improves user feedback but a DB unique constraint is required to settle concurrent writes. Input validation does not replace parameter binding, authorization or escaping.

Do not persist a plaintext password from a registration DTO/form. Hash through the project's password hasher and avoid returning sensitive values. Check installed minor/bundle APIs before adopting new multi-step form features.

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
