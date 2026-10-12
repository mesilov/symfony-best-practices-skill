# JWT authentication and token lifecycle

Read for jwt-authentication. Use the installed supported JWT integration, such as LexikJWTAuthenticationBundle; do not implement signature verification or install a new auth stack implicitly.

## Trust and issuance

A decoded JWT payload is not authenticated. Verify signature with explicitly allowed algorithms and trusted keys, validate expiry/not-before and the issuer/audience/type claims required by the token contract, and apply a bounded clock-skew policy. Do not select algorithms or arbitrary key/JWK URLs solely from untrusted headers. Use the bundle/library's supported verification hooks/configuration and verify which checks it actually performs; decoding or one successful signature is not the full application policy.

Issue stable subject/business identifiers and minimal non-secret claims from the authenticated/trusted issuance path. A usual signed JWT payload is readable, not encrypted. Validate tenant membership and resource authorization even when a signed claim names the tenant; decide how role/account/tenant changes invalidate stale claims. Never elevate privileges using a caller-supplied field or an unverified payload.

Store signing private keys/passphrases in the project's secret mechanism. Public verification keys have a different role. Key rotation needs a deliberate trust set/overlap window and retirement plan for existing tokens; do not regenerate keypairs as routine diagnosis or commit private keys.

## Access, refresh, and logout

Choose access TTL according to risk and usability rather than forcing a universal number. Short-lived access tokens bound exposure but do not define immediate logout/revocation. A self-contained access JWT remains valid until expiry unless the server enforces a mechanism such as a supported blocklist/token version/account lookup. Lexik 3.x includes a configurable jti-based blocklist with logout integration: inspect installed support, enable/check the real path, and use shared durable-enough storage until expiry when multiple instances validate tokens.

Revoke refresh credentials on the application's required logout/compromise/account-change paths. Refresh-token rotation/reuse detection and server-side storage belong to the installed refresh integration; rotation alone does not guarantee detection or race-safe replay rejection. Define concurrent refresh behavior and test that old tokens cannot be reused according to policy. Do not assume a refresh bundle is installed or copy obsolete route/controller IDs.

Client storage depends on the client. Browser localStorage is exposed to XSS; HttpOnly cookies reduce script access but introduce automatically sent credentials and require deliberate CSRF/SameSite/path/domain handling. Review the whole browser request model before switching storage. Serve credentials over the trusted HTTPS path and keep tokens out of URLs, logs and public errors.

## Wiring and checks

For Lexik, inspect installed config, login handlers, firewall ordering, stateless/provider choices, key paths and transport extraction. Confirm login/refresh/public rules do not bypass actual credential validation; see [Authentication](authentication.md). Claims or roles loaded from a token do not replace the resource policy in [Authorization](authorization-and-rate-limiting.md).

Functional/integration cases include valid signature, tampered token, expired/not-yet-valid token, wrong issuer/audience/type when required, disabled/stale identity, cross-tenant access, key rotation, concurrent refresh and logout/revocation across instances. Assert safe 401/challenge vs 403 and the declared [Problem Details](../http/rest-api.md) shape. Tests that simply decode a payload or mock the JWT manager cannot prove these checks.

Primary guidance: [Lexik JWT docs](https://symfony.com/bundles/LexikJWTAuthenticationBundle/current/index.html), [token invalidation](https://github.com/lexik/LexikJWTAuthenticationBundle/blob/8d614e1406ffabd36b1de5d3560e2dcc9db75e79/Resources/doc/11-invalidate-token.rst), [JWT BCP RFC 8725](https://www.rfc-editor.org/rfc/rfc8725.html).
