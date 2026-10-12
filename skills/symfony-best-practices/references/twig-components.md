# UX Twig components

Read for twig-components. Confirm `symfony/ux-twig-component`, Twig and any LiveComponent/HTML-extra packages in the lock file; UX versions are independent of Symfony's minor.

## Component selection

Use anonymous components for small markup/prop contracts, `#[AsTwigComponent]` classes for render-specific behavior, and existing slots/blocks for reusable composition. Keep business queries/authorization in application services and pass the needed presentation data. Do not adopt LiveComponent or a new asset/build stack just to reuse markup.

A component's public props are normally assigned after instantiation. Keep them writable under standard hydration; readonly injected service dependencies are a different concern. If using readonly props with `mount()`, explicitly consume and initialize the matching props there and verify the installed lifecycle; do not make all component classes readonly by default.

```twig
{# templates/components/Notice.html.twig: anonymous component #}
{% props message, tone = 'info' %}
<section class="notice" data-tone="{{ tone }}" {{ attributes }}>
    {{ message }}
</section>
```

Validate/allowlist prop values when they influence selection or behavior. Use the project's existing CSS/variant convention; CVA/Tailwind helpers require their own installed packages and versions.

## Escaping and interactive state

Preserve autoescaping and the correct HTML/attribute/JS context. Do not render user-supplied text with `|raw`; an intentional rich-HTML contract needs explicit sanitization and tests. Review dynamic URLs/attributes separately from text escaping.

A Twig component is not automatically reactive. If LiveComponent is installed and needed, mark only intended writable state, validate it server-side and enforce authorization on every relevant action. Client-writable IDs must not become arbitrary resource access. Use installed URL-sync/debounce APIs rather than assuming them from a donor example.

## Verification

Run the project's Twig lint, inspect `debug:twig-component` when available, and test rendered output, props/defaults, slots and escaping. Pure PHP class tests alone do not prove template rendering/hydration. Use functional/browser tests for interactive behavior or JS-dependent changes.

Primary guidance: [UX TwigComponent](https://symfony.com/bundles/ux-twig-component/current/index.html), [LiveComponent](https://symfony.com/bundles/ux-live-component/current/index.html), [Twig escaping](https://twig.symfony.com/doc/3.x/filters/escape.html).
