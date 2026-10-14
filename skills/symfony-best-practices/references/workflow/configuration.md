# Configuration, environment, and secrets

Read for config-env-parameters. Prefer the project's existing configuration format and deployment mechanism.

## Choose a home for a value

Use code constants for genuine invariants, container parameters for application configuration, environment variables for deployment differences, and the project's secret store/vault for credentials. Avoid a new feature-flag platform for a single existing toggle. Inject configuration into services instead of reading `$_ENV`/`getenv()` throughout business logic.

A committed `.env` contains safe defaults and names, never operational credentials. Dotenv file precedence is `.env`, `.env.local`, `.env.<environment>`, `.env.<environment>.local`; `.env.local` is skipped in `test`. Real environment variables normally take precedence over files; inspect bootstrap/custom override behavior if results differ. A generated `.env.local.php` can replace normal file loading.

Do not commit local overrides, decrypted dumps, generated credential-bearing files, or vault decryption keys. Encrypted vault files can be committed according to the project's deployment policy; public/encryption keys and private/decryption keys have different roles. A plain file protected by permissions is not encryption.

## Typed injection

```yaml
# config/services.yaml; illustrative binding for an existing application service
services:
    App\Service\ImportService:
        arguments:
            $batchSize: '%env(int:IMPORT_BATCH_SIZE)%'
            $enabled: '%env(bool:IMPORT_ENABLED)%'
```

`"false"` is a string until processed. Choose `int:`, `bool:`, `json:` or another supported processor for the actual contract. Use parameters for defaults shared by several services; `#[Autowire]` is an alternative when it matches project conventions. Validate required values at the appropriate boundary and produce errors that identify the variable without disclosing its value.

Use `config/packages/<environment>/` or `when@<environment>` for differing behavior. Test configuration must point to independent DB/cache/transport resources; the environment name alone does not ensure isolation.

## Workers and deployment

Long-lived services can retain values resolved at construction. Restart workers according to the deployment contract when configuration changes. Do not assume dynamic env closures or a new config option exists on every 8.x minor; inspect installed code and matching docs before adopting them. Keep the current AssetMapper/Encore/build pipeline unless frontend tooling is part of the request.

## Verification

Check the presence and injection of new variables in development, test and deployment configuration. Validate casts and missing/invalid inputs, run the project's container/config lint, and verify service wiring through the chosen runtime. Commands such as `debug:container --env-vars`, `--parameters`, `debug:dotenv`, secrets reveal/decrypt operations and verbose configuration output may expose values: do not paste their raw output into reports. Use filtered/redacted diagnostics.

Primary guidance: [configuration](https://symfony.com/doc/8.0/configuration.html), [env processors](https://symfony.com/doc/8.0/configuration/env_var_processors.html), [secrets](https://symfony.com/doc/8.0/configuration/secrets.html).

## Effective configuration and kernel boundaries

Inspect import order, environment-specific overrides and configuration references for the installed bundle. Parameters, env processors and service bindings solve different problems. Use lint/container checks without exposing secret values; syntax-valid YAML can still violate a bundle's schema. Kernel project/cache/build/log paths follow the actual release topology, not a fixed directory assumption. See [container/kernel configuration](../architecture/container-and-events.md) and [deployment](deployment-and-performance.md).

Reviewed current-line source: [Symfony 8.1 configuration](https://symfony.com/doc/8.1/configuration.html).
