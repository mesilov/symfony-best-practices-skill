# Twig templates and translation

Read for server-rendered pages, template composition, internationalization and locale-sensitive output. Pair with [Twig components](twig-components.md), [sessions](../http/sessions.md), and [cache](../data/cache.md).

Use template inheritance for page structure and includes/components for focused reusable views. Pass a small explicit view model; avoid database queries, HTTP calls and business decisions in Twig. Keep template paths/names consistent with installed bundle/namespace conventions. Controllers should select the view and prepare data before rendering.

## Output safety

Keep autoescaping enabled and match escaping to the actual HTML, attribute, JavaScript or URL context. `raw` marks content trusted; it does not sanitize it. Only render rich HTML after the application's explicit sanitization policy. Build JavaScript values through a suitable JSON/escaping path instead of concatenating user input into executable script. Validate permitted URL schemes separately from escaping.

Avoid rendering secrets and unrestricted entity graphs. Fragment/subrequest rendering can execute controllers and interact with sessions/cache; test the actual request chain. Template errors in production must use the application's safe error response rather than exposing debug output. Use Twig lint and functional rendering checks when markup/data contracts change.

## Translation and locale

Use stable translation IDs, explicit domains when needed, and parameter substitution; do not build sentences by concatenating translated fragments. Use ICU message syntax for plural/select logic where configured and test representative values. Supply placeholders as data; do not treat user content as trusted translated HTML. Twig autoescaping and translated-message trust are separate concerns.

Choose locale at the defined boundary (route, authenticated preference, request or explicit job input). Validate supported locales, fallback rules and locale persistence. CLI/async work has no implicit browser locale; include the intended locale in its contract. Do not leak a previous request/job's locale through shared mutable state. Keep cache keys/HTTP variants aware of all locale/user distinctions that affect output.

Use installed extraction/catalogue/debug commands and review extracted changes; do not overwrite translator work blindly. Test missing keys, fallback, pluralization, date/number formatting and escaping. Translation cache warming/invalidation follows the deployment process. A catalogue existing does not prove every locale variant renders correctly.

Sources: [templates](https://symfony.com/doc/8.1/templates.html), [translation](https://symfony.com/doc/8.1/translation.html).
