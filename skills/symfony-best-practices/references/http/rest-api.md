# REST contracts and RFC 9457 errors

Read for rest-controller-conventions, problem-details-rfc9457, and controller-cleanup. Preserve the consuming application's published HTTP contract; this reference does not mandate changing every existing API to a new format.

## Resource endpoints

Use explicit route names, methods and identifier requirements matching the actual public identifier type. Group resource routes where helpful; do not force UUIDs onto an existing integer/opaque-ID API. Keep controllers responsible for mapping/auth/response and delegate business behavior. A simple read may use a query/repository service without an extra pass-through service; see [Architecture](../architecture/architecture.md).

Use request/query DTO mapping where appropriate and explicit output fields/serialization groups. Prevent mass assignment and accidental lazy-association/sensitive-field serialization. Pagination needs a capped limit, deterministic order and a documented envelope/cursor contract; do not wrap an existing bare-array response without a compatibility decision. Deep pages can use indexed keyset pagination; see [Doctrine performance](../data/doctrine-performance.md).

| Outcome | Usual response, subject to the established contract |
| --- | --- |
| Read/update with representation | 200 |
| Resource created | 201 with an actual routable Location when applicable |
| Work accepted asynchronously | 202 with an observable job/result contract; not a claim of completion |
| Success without representation | 204 with an empty body |
| Malformed input / unsupported media | 400 / 415 |
| Payload constraint failure | Usually 422 for MapRequestPayload; query mapping differs |
| Missing credentials / denied authenticated actor | 401 plus required challenge / 403 |
| Missing resource / conflicting state | 404 / 409 |
| Rate refusal | 429 with Retry-After |

Use [Validation and forms](validation-and-forms.md) for exact mapping defaults and missing/null semantics.

## Problem Details

When the API adopts RFC 9457, emit `application/problem+json` through one consistent API error-mapping mechanism. Reuse an existing framework/API Platform normalizer instead of layering a competing blanket subscriber.

Define a stable problem `type` URI, human-readable `title`, safe occurrence `detail` and optional safe `instance`/extensions according to the API contract. The RFC does not require all five members in every response; `type` defaults to `about:blank`. If a `status` member is present, it must agree with the actual HTTP response generated. With `about:blank`, use the corresponding HTTP-status title (localized if applicable). Extensions such as violation paths and a correlation ID need stable documented semantics.

Map domain/application failures to HTTP at the HTTP adapter/error mapper. A pure domain exception does not need HTTP status codes or Symfony Response dependencies. Never copy an exception's message into public detail indiscriminately: even a 4xx can expose SQL, filesystem paths, account/resource existence or personal data. Expose only allowlisted safe messages; log diagnostic context server-side with the project's redaction/correlation policy.

Preserve status and protocol headers from HttpExceptionInterface, including relevant WWW-Authenticate, Allow and Retry-After, while setting the problem content type. A global mapper must not flatten authentication failures, method errors or rate refusals into generic 500/JSON without their headers. Cover security entry-point, authentication-failure and access-denied handlers as well as kernel exceptions; their execution paths can differ.

Scope the formatter to the agreed API routes/formats and negotiate error content according to the API policy. HTML pages/login redirects, CLI commands and async handlers retain their own contracts. MapRequestPayload may wrap ValidationFailedException inside an HTTP exception; inspect the actual exception/cause chain and preserve its status/violations rather than assuming every validation failure arrives as a top-level exception.

## Verification

Functional tests should cover success, malformed JSON, type/constraint/query errors, 401/403, 404/405, conflict, 429 and sanitized 500 where relevant. Assert content type, actual/body status agreement, required headers, safe detail/extensions and unchanged HTML behavior. A unit test of the mapper alone does not prove firewall/error ordering.

Primary guidance: [Symfony controller mapping](https://symfony.com/doc/8.0/controller.html), [error pages](https://symfony.com/doc/8.0/controller/error_pages.html), [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457.html), [HTTP semantics](https://www.rfc-editor.org/rfc/rfc9110.html).
