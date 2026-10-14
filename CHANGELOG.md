# Changelog

## Unreleased

- Добавлен repository-local `symfony-skill-maintainer`: сопровождение репозитория, обновление provenance и лицензий, проверки и выпуск релизов с проверкой опубликованных assets.
- Добавлены canonical `.agents/skills/`, относительные aliases для Codex/Claude, маршрутизация в AGENTS.md и проверки discovery/ссылок в существующей unittest suite. Состав и версия распространяемого пакета не изменены.

## 0.1.0 — локальная подготовка, дополнено 2026-10-15

- Единый symfony-best-practices для Symfony 8.x с официальной проверкой 8.1 и оговорками для 8.0 / PHP 8.4+.
- Короткий SKILL.md и 31 справочник в 7 смысловых группах на основе 42 выбранных донорских скиллов из двух репозиториев.
- Версионные ограничения, проектные runners и проверяемые границы результата.
- Уточнения Doctrine recovery/batching, Messenger retry/idempotency, migrations, Foundry, browser isolation, cache, Scheduler и Twig.
- Pinned provenance, SHA-256 77 материалов и обе MIT-лицензии, MIT attribution и Codex UI metadata.
- Validator, негативные тесты, детерминированные tar.gz/zip с SHA256SUMS и CI workflow.

- Добавлены модули/bundles, Console input/lifecycle, REST/RFC 9457, DTO/PATCH semantics и authentication/JWT.
- Объединены пересечения Doctrine, migrations, queries, layered architecture и Messenger; provenance различает одинаковые skill names разных репозиториев.

- Сверены все 43 ссылки на официальную документацию: 40 страниц, два source repository commits, SHA-256 и исходные лицензии.
- Добавлены HttpKernel/routing, DI/events, sessions, Twig/Translation, Serializer, logs/errors, Mailer/Notifier, HttpClient/webhooks, Workflow/Lock/utilities и deployment/performance/HTTP cache.
- Добавлены самостоятельные guidance для AI Mate CLI и AI/MCP Bundle: installed versions, минимальный tool exposure, trust/authz и проверка реального вызова.
- Provenance schema 3 и offline/checkout validation официальных источников; архивы по-прежнему имеют версию 0.1.0.
