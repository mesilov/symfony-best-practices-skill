# Filesystem, UID, YAML, and ExpressionLanguage

Read for these components when implementing a concrete use case. Do not add dependencies or replace working abstractions solely because a component exists.

## Filesystem

Use Filesystem/Path APIs for the intended file operation and catch relevant IO exceptions. Establish an authorized base directory, validate/resolve candidate paths, reject escapes and account for symlinks and race conditions. Concatenating a user path with an upload root does not establish containment. Recursive remove/mirror operations need explicit source/target ownership and a bounded scope; test dangerous boundaries in a temporary directory.

Use minimal necessary permissions, not mode 0777 as a generic fix. Understand overwrite/symlink behavior and partial failure. `dumpFile()` supports an atomic local replacement path; that does not provide a transaction across files, a database and remote storage. Use the application's storage abstraction for non-local files and a recoverable publication strategy where required.

## UID

Use the chosen UUID/ULID type consistently through DTOs, Doctrine mapping, URLs and serialization. Validate format at boundaries. UUIDv7 can help index locality compared with random UUIDs, but index size, database type and product requirements still matter. Do not migrate every integer ID without a justified design/migration. An unguessable ID is not authorization, a secret credential, or an idempotency guarantee.

## YAML

Use Yaml parse/dump APIs with explicit flags appropriate to the trust boundary. Do not enable object deserialization (`PARSE_OBJECT`) for untrusted input; constant/custom-tag handling also needs an explicit trusted policy. Bound input size, nesting and alias expansion using the installed component's supported controls; newer parser controls are minor-version dependent.

Preserve scalar semantics: booleans, nulls, numeric strings, timestamps and quoted values may parse differently. Test parse/dump round trips when exact types matter. Lint project configuration with the existing runner; successful syntax parsing does not prove the framework's configuration schema accepts it.

## ExpressionLanguage

Treat expressions as a programming/configuration surface. An evaluator is not an automatic sandbox for arbitrary end-user input, especially when variables expose service/domain objects and methods. Restrict who can author expressions, available variables/functions, input size and evaluation resources. Do not pass the container or sensitive objects into untrusted expressions. Check/lint trusted expressions and test both permitted decisions and rejection paths.

Sources: [Filesystem](https://symfony.com/doc/8.1/components/filesystem.html), [UID](https://symfony.com/doc/8.1/components/uid.html), [YAML](https://symfony.com/doc/8.1/components/yaml.html), [ExpressionLanguage](https://symfony.com/doc/8.1/expression_language.html).
