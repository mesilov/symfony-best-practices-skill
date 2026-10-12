# Tests, fixtures, and browser isolation

Read for tdd-with-phpunit, functional-tests, test-doubles-mocking, doctrine-fixtures-foundry, and e2e-panther-playwright. Use the installed PHPUnit/Bridge/Foundry/Panther versions and configured runners; do not install a second test stack implicitly.

## Choose the boundary

| Test | Use for |
| --- | --- |
| PHPUnit `TestCase` | Pure domain rules and isolated application orchestration |
| `KernelTestCase` | Container wiring, repositories and real DB behavior |
| `WebTestCase` | HTTP contract, authentication, forms, response/DOM |
| Panther/Playwright | Critical flows requiring JavaScript or a real browser |

For new behavior or a regression, write the focused test, observe a failure for the relevant reason, make it pass, and refactor with relevant checks green. For a behavior-preserving extraction, first record the current contract. A broken test environment is not a successful RED test of application behavior.

Use compatible PHPUnit attributes/data providers rather than deprecated annotations; inspect the installed version. Avoid brittle assertions about every internal method call. Test outcomes and meaningful external interactions. A skipped test is not a passed test.

## Kernel, HTTP and CLI

Call `static::createClient()` directly in `WebTestCase`; do not boot the kernel first. Use `static::getContainer()` for the test container. Replace an external service with a double before it is used; request/kernel reboot can recreate services, so verify the replacement's lifetime.

Use `loginUser()` where the tested firewall supports it; stateless firewalls require their actual authentication mechanism. Test allowed, forbidden, anonymous, invalid, missing-resource and successful paths as appropriate. Confirm status, payload, redirects, side effects and query behavior.

```php
<?php
namespace App\Tests\Functional;

use Symfony\Bundle\FrameworkBundle\Test\WebTestCase;

final class MissingRouteTest extends WebTestCase
{
    public function testUnknownRouteReturns404(): void
    {
        $client = static::createClient();
        $client->request('GET', '/__missing_route_for_test__');

        self::assertResponseStatusCodeSame(404);
    }
}
```

The example is a smoke-test pattern; actual tests must assert the requested application's contract. For invalid submitted forms, assert 422 when the project's rendering contract uses it; `assertResponseStatusCodeSame(422)` avoids depending on a newer convenience helper.

For CLI, `CommandTester` is the baseline option: check success/failure exit code, output and persisted effects. Test interactive branches explicitly. If Console events are part of the contract, use `ApplicationTester`: `CommandTester` does not dispatch them. A helper method on CommandTester can exist even when a similarly named test-case helper is newer; check the owning class as well as the method name. Use newer command helpers only after checking the exact Symfony minor; an 8.1 helper is not assumed on 8.0.

## Doubles and database fixtures

Stub values, use fakes for meaningful behavior and use mocks where interaction is the contract. Do not mock the system under test. A mocked EntityManager/repository can test orchestration, but cannot verify mappings, queries, constraints, locking, cascades or transactions; those need a real test DB. Fake repositories supplement DB adapter tests.

For Foundry v2, choose `Zenstruck\Foundry\Persistence\PersistentObjectFactory` for real objects. Existing `PersistentProxyObjectFactory` code still has proxy semantics depending on version; do not blindly remove `_real()`/refresh helpers from all v2 code. Object proxies are deprecated from v2.7; check the upgrade guide and PHP 8.4 auto-refresh configuration before migrating them.

Keep factory defaults minimal and deterministic. Use named states, explicit data for boundary cases, safe unique values and fixed Faker seeds when diagnosing random failures. A seeded factory does not replace explicit business input. Do not construct persistent objects in data providers before the proper boot/reset lifecycle.

Foundry's PHPUnit extension and `#[ResetDatabase]` require v2.9+ and compatible PHPUnit. Older installed versions can use their documented traits. Keep the project's existing DAMA/Foundry reset strategy coherent; do not blindly combine two full reset mechanisms. Reset commands can drop/create a DB: prove its isolation before running them. `.env.local` is skipped in test; inspect actual `.env.test`/runtime configuration without printing DSNs.

## Real browser tests

Choose the installed Panther or Playwright stack. Use stable selectors, explicit waits or Playwright web-first assertions, deterministic committed fixtures and per-worker DB/resource isolation. Fixed sleeps hide races. Keep screenshots/traces as ignored local files or controlled CI artifacts; redact sensitive data before sharing them. Do not disable the browser sandbox by default.

**DAMA transaction rollback in the PHPUnit process does not isolate a separately running browser application server.** Uncommitted fixtures may be invisible to that server, and its writes are outside the test's transaction. Use committed setup/cleanup or a dedicated resettable test DB, with isolated databases for parallel workers. Check which process/connection actually reads and writes; apply the same rule to async workers tested across processes.

Verify driver/browser setup and server lifecycle in CI. Cover critical user journeys in E2E and cheaper rules at unit/kernel/HTTP levels. State which layers actually ran.

Primary guidance: [Symfony testing](https://symfony.com/doc/8.0/testing.html), [Panther](https://symfony.com/doc/8.0/testing/end_to_end.html), [Foundry](https://symfony.com/bundles/ZenstruckFoundryBundle/current/index.html), [PHPUnit](https://docs.phpunit.de/), [Playwright assertions](https://playwright.dev/docs/test-assertions).
