# Проверка скилла мейнтейнера — 2026-10-15

Скилл: `.agents/skills/symfony-skill-maintainer/`. Ветка: `codex/add-project-maintainer`. Worktree: `/private/tmp/symfony-skill-maintainer`. Итоговая основа: `54c7b2024702b2a57bccab2333b00da34b5daf7b` (`origin/main`, локальный tracking ref). Основной checkout не изменялся.

Работа начата от `81fa983`; за время выполнения tracking ref обновился до merge полного пакета и английского README. Наш локальный коммит перенесён на `54c7b20`, конфликт README разрешён сохранением актуального английского текста и добавлением абзаца мейнтейнера. Изменения этой ветки не включают повторное внесение пакета или перевод README.

## Результаты

| Проверка | Результат |
| --- | --- |
| Исходная suite | PASS: 13 tests |
| RED новых структурных тестов | 3 tests, 4 ожидаемых assertion failures: отсутствовали скилл и два aliases |
| Итоговая suite | PASS: 16 tests, включая 3 проверки maintainer discovery/UI, ссылок и aliases |
| Product validator с четырьмя checkout | PASS: закреплённые HEAD, 77 донорских + 40 документационных raw files, лицензии; 31 reference / schema 3 |
| skill-creator quick_validate | PASS для обоих скиллов |
| Builder и архивы | PASS: tar.gz/zip по 37 файлов, canonical bytes и SHA256SUMS совпадают; maintainer исключён из payload |
| Воспроизводимость | PASS в существующем тесте двух rebuild в одном toolchain |
| Документированная проверка assets | PASS на отдельной копии candidate; испорченный ZIP отклонён |
| Agent aliases | Оба относительных symlink, tracked mode 120000; один canonical каталог |
| Whitespace / scope | git diff --check; version, product files, scripts, requirements, licenses и CI workflow не изменены |

Python: `/private/tmp/symfony-skill-checks-20261013/bin/python`, версия 3.14.7, PyYAML 6.0.3, zlib 1.2.12. Системный `python3` не имеет PyYAML; вместо установки глобальных зависимостей использован существующий подходящий venv.

Команды ниже выполнялись из worktree с указанным Python:

```sh
python -B scripts/validate.py \
  --upstream superpowers-symfony=/private/tmp/symfony-skill-donor-20261013 \
  --upstream symfony-skills=/private/tmp/symfony-skill-second-donor-20261013 \
  --docs-checkout symfony-docs=/private/tmp/symfony-docs-current-20261015 \
  --docs-checkout symfony-ai=/private/tmp/symfony-ai-official-20261015
python -B -m unittest discover -s tests -v
python -B /Users/mesilov/.codex/skills/.system/skill-creator/scripts/quick_validate.py .agents/skills/symfony-skill-maintainer
python -B /Users/mesilov/.codex/skills/.system/skill-creator/scripts/quick_validate.py skills/symfony-best-practices
python -B scripts/build_release.py
git diff --check
```

Команда проверки фактических assets из `references/checks.md` запущена без изменения её Python body на копии dist во временном каталоге. Первый запуск проверил digests, candidate bytes и каждый member обоих архивов. После добавления `corrupt` в скачанную копию ZIP второй запуск завершился ненулевым кодом. Это локальная симуляция проверки downloaded assets, а не скачивание из GitHub.

Локальные archive digests:

```text
b399befed5e3f99a6fd63e59ede29f3e08529d66cacd93261fc3935e9f0eb7da  symfony-best-practices-0.1.0.tar.gz
ed3ecbc8029664e43be7704d3286782bd051bf2996a31b24dc9bdb65421b0d66  symfony-best-practices-0.1.0.zip
```

## Сценарная оценка

[Три запроса и rubric](../tests/maintainer-scenarios.md) проверены двумя отдельными read-only агентами: сначала по исходному репозиторию без скилла, затем с новым entrypoint и адресными справочниками. Оба дали корректные решения по repository-qualified identity, offline/checkout evidence, согласованному version bump и запрету неподтверждённой замены assets. Baseline behavioral failure не наблюдался; улучшение модели в процентах не заявляется.

With-skill агент использовал все три процедуры и подтвердил соответствие raw scripts/tests. Он обнаружил практический пробел: архивный unittest проверяет собственные builds, а отдельной команды проверки выбранного candidate/download directory не было. В checks добавлена read-only команда, releases ссылается на неё. Focused статическое ревью не обнаружило ошибки; runtime PASS/отклонение corrupt ZIP подтверждены отдельными локальными запусками автора.

## Границы первичного создания

Для этой maintainer-ветки не выполнялись push, PR, remote CI, merge, tag или публикация GitHub Release. Локальный `origin/main` наблюдался после обновления другой работой; live GitHub release state в этой задаче не проверялся. Product VERSION остаётся 0.1.0. Проверка существующих source pins не является обновлением источников до upstream HEAD. Symfony runtime и provider operations не запускались.

## Подготовка merge PR #3 после обновления main

После публикации этой ветки PR #3 открыт в main; обе проверки CI на первоначальном head `9e76b73` завершились SUCCESS. До порученного merge в main вошёл PR #2 (`075d84a`) с тем же canonical skill, changelog gate и правилом сохранения существующих feature branches. Live readback PR #3 показал конфликт; в существующую ветку включён текущий main без переписывания опубликованной истории.

Разрешены конфликты в maintainer SKILL.md, AGENTS.md и CHANGELOG.md. Сохранены требования PR #2: содержательная committed changelog entry до любого PR, включая drafts/docs; проверка actual target-to-head diff; сохранение branch/worktree при продолжении существующей работы. Детали gate вынесены в checks.md и адресно загружаются из entrypoint. Existing changelog history и M1–M5 scenarios сохранены. Новый substantive entry описывает расширение procedures, aliases и tests.

Локальная повторная проверка объединённого дерева: 16/16 unittest tests, product validator, quick_validate maintainer, build и whitespace checks прошли. Entrypoint body — 398 слов. Независимое read-only ревью разрешения конфликтов не нашло blocking defects. Распространяемый продукт, source pins и VERSION не изменены. Этот раздел фиксирует подготовку: merge main и post-merge CI подтверждаются последующим live readback, а не исходным CI ветки.
