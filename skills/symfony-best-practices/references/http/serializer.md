# Serialization and API representations

Read for JSON/XML representations, DTO hydration, Serializer groups and circular references. Pair with [validation/forms](validation-and-forms.md), [REST](rest-api.md), and [Doctrine performance](../data/doctrine-performance.md).

Normalization converts objects into data; encoding converts data into a wire format. Deserialization/denormalization is not validation or authorization. Use dedicated request/response DTOs and an explicit allowlist of writable/readable fields; a client must not set owner, roles, status or tenant through automatic entity hydration.

## Shape and limits

Choose groups/context per use case, not directly from a client-supplied arbitrary group name. Review names, null handling, dates/timezones, enum/UID representation, missing versus null fields, and backwards compatibility. Supply type metadata supported by the installed normalizer/property-info configuration for nested DTOs and collections. Readonly/constructor requirements must still establish valid objects; do not bypass invariants by setting private properties indiscriminately.

Entity traversal may initialize lazy relations and expose large/cyclic graphs or confidential properties. Prefer deliberate response projections; use circular-reference handling and max-depth deliberately when object graphs are unavoidable. `MaxDepth` metadata is a graph-normalization concern, not the JSON decoder's nesting/size limit. Bound request bytes, decoder nesting, collection size and output separately.

Handle malformed syntax, unsupported formats/content types, type errors and validation violations through the declared safe API error contract. Partial denormalization can collect errors while leaving an incomplete object; do not persist that object as if validation succeeded. Inspect supported exception/context APIs rather than treating every Serializer exception as an internal 500 or exposing its raw details.

## Verification

Test exact stable fields/formats, forbidden-field rejection or exclusion, null/missing behavior, malformed input, nested type failures and depth/size limits. Include authorization and tenant cases independently of serialization groups. For ORM responses, observe queries and lazy loading under realistic collection sizes; serializer unit tests do not detect an N+1 query caused by getters.

Source: [Serializer](https://symfony.com/doc/8.1/serializer.html).
