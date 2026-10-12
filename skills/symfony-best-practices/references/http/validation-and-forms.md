# Input DTOs, validation, and forms

Read for dto-and-validation, form-types-validation, and value-objects-and-dtos. Input shape, domain invariants, authorization and persistence constraints are separate checks.

## DTO mapping

Use separate input/output DTOs when their contracts differ; select immutable constructor-based DTOs where the actual serializer lifecycle supports them. Nullable data is valid when the input contract permits it; do not replace optional fields with arbitrary empty defaults just to make construction succeed.

For PATCH, represent **missing** separately from **explicit null** when omission means retain and null means clear. A nullable property alone may collapse those states. Use a deliberate presence-aware DTO/resolver or the project's patch representation and test both paths. Accept only intended writable fields; map to entity behavior/use cases rather than unconstrained entity hydration.

MapRequestPayload integrates body deserialization and validation; on the 8.0 baseline its default constraint-failure status is 422. MapQueryString's default validation-failure status is **404**; explicitly select validationFailedStatusCode if the API contract requires another status. Missing query, null/type construction errors, malformed JSON and unsupported content type have distinct behavior: test the actual resolver/configuration rather than treating everything as 422.

Declare JSON route format/accepted input formats where required by the API contract. Prefer built-in constraints and validation groups. Nested DTOs/collections need reliable element type metadata, the supporting PropertyInfo extractor/packages where necessary, and `Assert\Valid` at each intended cascade boundary. Check that the serializer really constructs DTO instances rather than untyped arrays. Allowlist discriminator mappings for polymorphic input.

Use a custom value resolver for genuine body/route/header composition that built-in mapping cannot express. Verify which values are trusted: a route/header tenant ID is not authenticated tenant membership. Explicitly run validation and map failures through the existing HTTP error contract; see [REST and errors](rest-api.md). Do not assume Validator attributes enforce themselves.

For public input, bound body size, collection lengths and decoding depth using the correct decoder/server options. Serializer object MaxDepth controls and JSON decoder depth are different mechanisms. Keep OpenAPI/schema and implemented DTO/error behavior aligned. `UniqueEntity` or a custom uniqueness check improves feedback but cannot replace a DB constraint under races.

## Forms

Declare explicit form field types and map only intended writable fields. Place reusable constraints on input models/domain data; keep UI-only constraints on the form. Select validation groups for differing use cases rather than duplicating constraints. A data transformer rejects unconvertible values with `TransformationFailedException`; listeners belong only where input/model adaptation requires them.

Handle the request and check `isSubmitted() && isValid()` before delegating to business work. On the 8.0 baseline, passing the Form object directly to the standard controller `render()` supports 422 for an invalid submitted form. Passing a prebuilt view or a custom response may use a different contract; assert the actual status. Use an appropriate redirect after successful browser writes.

Keep CSRF enabled for browser forms where applicable; stateless APIs need their chosen authentication/request protection contract. Validate uploaded content, size and storage rules at the appropriate boundary. `UniqueEntity` improves user feedback but a DB unique constraint is required to settle concurrent writes. Input validation does not replace parameter binding, authorization or escaping.

Do not persist a plaintext password from a registration DTO/form. Hash through the project's password hasher and avoid returning sensitive values. Check installed minor/bundle APIs before adopting new multi-step form features.

## Verification

Test nested/type failures, accepted formats, groups, missing and explicit null, unauthorized fields, custom resolvers, valid/invalid submitted forms and transformation errors. Verify domain invariants separately and concurrent uniqueness on a real DB. Input validation must not substitute for the authorization checks in [Authorization](../security/authorization-and-rate-limiting.md).

Primary guidance: [controller mapping](https://symfony.com/doc/8.0/controller.html), [Serializer](https://symfony.com/doc/8.0/serializer.html), [Validator](https://symfony.com/doc/8.0/validation.html), [forms](https://symfony.com/doc/8.0/forms.html).
