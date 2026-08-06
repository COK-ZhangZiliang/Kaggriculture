# AGENTS.md

These instructions apply to the entire repository.

## Project Mission

Build, test, and submit reliable autonomous agents for the Kaggle
Kaggriculture simulation. The first milestone is a deterministic baseline that
completes a 720-turn local episode, produces a replay, and passes Kaggle's
submission validation.

## Repository Map

- `main.py`: Kaggle submission entrypoint. It must expose `agent(obs)` and stay
  self-contained unless the submission archive explicitly includes helpers.
- `scripts/`: local evaluation and packaging utilities.
- `tests/`: deterministic unit and environment smoke tests.
- `assets/`: README and project branding assets only.
- `replays/`, `logs/`, `runs/`, `data/`, `datasets/`: local-only generated or
  downloaded artifacts; never commit them.

## Runtime and Development Rules

- Use the CPython version recorded in `.python-version` and a repository-local
  `.venv`.
- Treat `requirements.txt` and `requirements-dev.txt` as the portable top-level
  dependency inputs. `requirements.lock` is the exact development snapshot for
  the Python, operating system, and architecture documented in its header.
- Do not treat `requirements.lock` as cross-platform. It intentionally excludes
  `pip`, `setuptools`, and `wheel`; recreate it from a clean matching environment
  when a top-level dependency changes, then run `python -m pip check` and the
  applicable tests.
- Keep the submission policy deterministic and lightweight enough for Kaggle's
  per-turn execution limit.
- Treat observations as untrusted mappings: use defensive lookups where doing
  so does not hide schema errors.
- Return only actions accepted by the current Kaggriculture action schema.
- Invalid actions are often silent no-ops; add tests for position, tile state,
  inventory, seeds, and end-of-season liquidation logic.
- Do not depend on network access, local absolute paths, environment secrets,
  or files outside the submission bundle.
- Keep credentials outside the repository. Never print, copy, stage, or commit
  Kaggle or GitHub tokens.
- Keep README commands runnable from the repository root and update README
  evidence whenever the verified runtime or submission state changes.

## Documentation Rules

- `README.md` must describe only the currently promoted agent strategy, its
  current verification evidence, and its current Kaggle delivery.
- Do not retain superseded strategy descriptions, prior submission tables, or
  version-to-version evolution narratives in `README.md`.
- Record the chronological strategy evolution only in the `Strategy Evolution
  Log` section of this file. When a new strategy is promoted, replace the
  strategy and delivery content in `README.md` and append one concise history
  entry here in the same documentation change.
- Keep detailed reproducibility evidence in `docs/` when needed; the evolution
  log should summarize and link to evidence rather than duplicate raw results.

## Strategy Evolution Log

### V1: deterministic carrot baseline — 2026-08-05

- Used the north-west quadrant as a carrot field, hired four hands daily,
  assigned units by row, replenished seeds, and liquidated at the end.
- Established the first complete 720-state local, packaging, Kaggle validation,
  and public-GitHub delivery path.
- Kaggle submission `55268182`, message `baseline-v1 deterministic carrot
  planner`, reached `COMPLETE`; code commit `ec8bdba50701653e4c3b884cce65897e6fc68f3e`,
  archive SHA-256
  `d3781fb452c1ec3c85579c9c22f8dac860c307c3d4b57701eaef796c58d9f448`.
- Its public score was observed at 471.3 on `2026-08-05T11:25:21Z`; simulation
  ratings are dynamic, so this is only a historical snapshot.

### V2: market-aware mixed farm — 2026-08-06 (current)

- Replaced the single-crop planner with a three-quadrant wheat, melon,
  strawberry, cow, and sheep supply chain.
- Added worker alignment, actor-local weed recovery, projected-stock sell
  clipping, sustained mirror detection, premium-sale front-running,
  collision-aware order sorting, and step-718 liquidation.
- Frozen holdout evidence: 38 wins in 40 both-seat games, all 720 states and
  `DONE/DONE`, with a positive mean margin against every evaluated public
  policy artifact. See `docs/evidence/v2-holdout.json`.
- Kaggle submission `55292510`, message `v2 market-aware mixed-farm route
  c587ec5`, reached `COMPLETE`; code commit
  `c587ec54eb5e46e560f21797507b1e759ba7ccf6`, archive SHA-256
  `3967ea31aa2da69e0be8b5af0dc07b70d9f5f5384c3f8a1ae74ffa12173ca3ef`.
- Its public score was 754.8 after public episode `90378552`, verified at
  `2026-08-06T07:40:21Z`; this remains a dynamic snapshot.

## Verification Gates

Before treating a baseline change as complete, run all applicable checks:

1. `python -m pip check`
2. `python -m pytest -q`
3. `python scripts/run_local_match.py --opponent starter --seed 20260805`
4. `python scripts/run_local_match.py --opponent random --seed 20260805`
5. `python scripts/package_submission.py`
6. Import and syntax checks for every file included in the submission.

For documentation changes, check formatting, links, and example commands. If an
applicable check cannot be run, record the reason in the commit body, pull
request description, or delivery note.

The full 720-turn episode must end with both agents in a terminal status. A
Kaggle upload is only "submitted" until the remote submission status confirms
validation; a local win or successful upload is not evidence of a scored bot.

## Kaggle Submission Rules

- `main.py` must be at the submission root and expose `agent(obs)`.
- Keep the archive below the competition's 100 MiB submission limit.
- Review the exact archive contents before upload.
- Do not include replays, datasets, logs, caches, credentials, or the virtual
  environment.
- Use descriptive submission messages such as `baseline-v1 deterministic
  carrot planner`.
- Record the submission ID, timestamp, message, and remote status in the
  delivery evidence, but do not fabricate a score or validation result.
- Every code revision submitted to Kaggle must also be committed and pushed to
  GitHub in the same delivery cycle. Record the Kaggle submission ID together
  with the corresponding Git commit SHA so the uploaded `main.py` is traceable
  to the public repository.

## Git Rules

The rules below are adapted from
[`COK-ZhangZiliang/Git-Rules`](https://github.com/COK-ZhangZiliang/Git-Rules/blob/ae0e80bb4a18a40c60ca514f0ce9d8f2a4c338af/README.md)
at commit `ae0e80bb4a18a40c60ca514f0ce9d8f2a4c338af`.

- Create commits only when explicitly requested by the user or maintainer.
- Each commit must contain one logical, testable change. Split unrelated
  features, fixes, refactors, tests, and documentation changes.
- Do not bypass checks with `--no-verify` and do not rewrite shared history.
- Prefer topic branches such as `codex/<topic>`, `feature/<topic>`,
  `fix/<topic>`, or `docs/<topic>`, with an English kebab-case topic.
- Use Conventional Commits: `<type>(<scope>): <subject>`, or omit the scope for
  repository-wide changes.
- Recommended common types are `feat`, `fix`, `refactor`, `test`, `docs`, `chore`,
  and `perf`.
- Write the subject in English, imperative mood, lowercase, without a trailing
  period, and at most 72 characters when practical.
- Behavioral, schema, data-format, or compatibility-sensitive commits need a
  body covering motivation, implementation, impact, verification, and
  rollback.
- Stage files by explicit path. Never use `git add -A` or `git add .`.
- Before committing, inspect `git status --short` and `git diff --cached`, then
  run verification matching the change scope.
- Never stage credentials, `.env` files, caches, local experiment outputs,
  model weights, datasets, or large generated artifacts.
- Before the first commit, inspect repository-local author configuration. If
  either value is absent, use only the repository-local fallback:

  ```bash
  git config --local user.name "ziliang"
  git config --local user.email "ziliangzhangcok@gmail.com"
  ```

- Do not change global Git identity unless explicitly requested.
- Push user-requested commits to the verified remote unless the user asks to
  keep them local. Do not push when no remote is available. Confirm the branch
  and remote before pushing.
- Pull request descriptions, when requested, must cover background, solution,
  compatibility or data impact, test results, safety/privacy/cost impact, and
  rollback.
- Keep pull requests focused; do not combine unrelated topics in one pull
  request.
