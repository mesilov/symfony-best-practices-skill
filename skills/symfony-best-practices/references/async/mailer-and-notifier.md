# Mailer and Notifier delivery

Read for email, SMS/chat/push notifications, templated messages and asynchronous delivery. Pair with [Messenger](messenger.md), [Twig/translation](../presentation/twig-and-translation.md), and [configuration](../workflow/configuration.md).

## Transport and content

Choose the installed Mailer/Notifier transport/bridge and configure credentials through the existing secret mechanism. URL-encode reserved DSN credential characters; never log a complete credential-bearing DSN. Verify TLS/certificate and provider settings rather than disabling verification to fix connectivity. Sender, recipient, channel preferences and tenant ownership are application policy, not caller-controlled delivery instructions.

Use typed address/message APIs and explicit templates/context; avoid concatenating untrusted values into headers or trusted HTML. Validate recipient/content constraints at the appropriate boundary. Use explicit locale/timezone for jobs. Keep attachments bounded and sourced from authorized paths/storage; do not let arbitrary user input select a local file or remote URL for attachment fetching.

## Delivery contract

With the relevant Messenger integration/routing, Mailer or Notifier work may be queued. Inspect the actual bus, transport and worker configuration; returning from send/dispatch can mean queued, not delivered. An SMTP/provider acknowledgement also does not prove inbox delivery. Track provider delivery/bounce outcomes where product behavior requires them.

For asynchronous TemplatedEmail, context must be serializable. Pass stable scalar data/identifiers, not managed entities, closures or live services. Verify when rendering and attachment access occur: a worker may run later on another host after a temporary file disappears. Test serialization plus worker-side rendering/access for that contract.

Do not send mail/SMS inside a DB transaction and assume rollback cancels it. Record intent atomically with business state and deliver after commit through a reliable outbox/worker path when required. Duplicate delivery is possible; use stable deduplication/provider idempotency where supported and reconcile ambiguous outcomes. Retry transient failures with a finite policy; do not repeat permanent invalid-recipient failures indefinitely.

## Verification

Use framework mailer/notifier test facilities, a null transport or local catcher appropriate to the installed setup. Assert recipients, subject/content/template, locale, channel choice and queued/sent distinction. Add transport serialization/failure tests for async paths and actual provider tests only when authorized. A catcher/in-memory transport proves message construction or routing, not external delivery.

Sources: [Mailer](https://symfony.com/doc/8.1/mailer.html), [Notifier](https://symfony.com/doc/8.1/notifier.html).
