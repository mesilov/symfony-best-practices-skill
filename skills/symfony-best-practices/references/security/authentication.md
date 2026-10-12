# Authentication, firewalls, and credential handling

Read for security-authentication and jwt-authentication. Select the existing authentication contract before configuring Security.

## Identity and firewall boundaries

Authentication establishes a verified actor; voters/access-control decide what that actor may do. Read identity from Symfony's authenticated token/current user, not a caller-supplied user/tenant field. Account-enabled status, credential changes and role freshness must match the user-provider/lifecycle contract.

Firewalls are ordered: the first matching firewall handles a request. Access-control entries are also first-match. Place deliberately public login/refresh endpoints and more specific protected rules before broad patterns, and confirm their HTTP methods/route ownership. PUBLIC_ACCESS does not validate refresh credentials or make an endpoint trustworthy by itself.

Choose stateful browser sessions or stateless tokens according to the product; a JSON API can legitimately use a session. Do not impose JWT or stateless mode on every API. Verify which firewall/session/context actually authenticates each endpoint. Use the supported built-in form_login/json_login/other mechanism before writing a custom authenticator solely for routine login.

## Credentials and custom authenticators

Use PasswordAuthenticatedUserInterface and the configured Symfony password hasher. Persist only password hashes, keep plaintext out of logs/serialized output, and support the project's rehash/update flow. Hashing algorithm/cost are version/runtime/configuration choices; do not implement an unsalted fast hash or a home-grown password scheme. Existing getRoles defaults follow the application's privilege contract, not a rule that every identity gains ROLE_USER.

A custom authenticator's supports/authenticate/success/failure paths must establish a verified credential, load the intended user and integrate Security's user checks. SelfValidatingPassport skips a credential check; use it only when the trusted token/API-key lookup or previous mechanism actually validates the credential. Do not treat any supplied API-key header as proof of identity. Use the installed authenticator/provider APIs and explicit service wiring.

For API clients, return the declared 401/challenge and 403 format with safe messages. Browser flows may redirect through their configured entry point; preserve that behavior. Connect consistent API errors to [REST and errors](../http/rest-api.md), without leaking raw AuthenticationException messages.

## Browser protection

Session/cookie credentials are sent by the browser automatically. Evaluate CSRF for cookie-authenticated writes, including a stateless JWT delivered in a cookie; **stateless alone does not remove CSRF risk**. Keep the framework's CSRF/session fixation/cookie settings and trusted-proxy/HTTPS configuration appropriate to the application. Header bearer authentication has a different request/credential exposure model.

Use the existing login-throttling/rate-limit mechanism when login abuse is in scope; it is separate from authorization and edge DoS control. Define logout, remember-me, account disable/password change and token/session revocation behavior explicitly.

## Verification

Exercise the actual firewall: successful/failed login, missing/invalid credentials, disabled user, cross-tenant denial, entry-point behavior, password changes/rehash, logout and CSRF as applicable. Inspect first-match routing and negative paths with functional tests; a mocked current user does not prove authentication. Use [JWT](jwt.md) for token-specific trust/lifecycle and [Authorization](authorization-and-rate-limiting.md) for resource policy.

Primary guidance: [Symfony Security](https://symfony.com/doc/8.0/security.html), [custom authenticators](https://symfony.com/doc/8.0/security/custom_authenticator.html), [access control](https://symfony.com/doc/8.0/security/access_control.html), [passwords](https://symfony.com/doc/8.0/security/passwords.html).
