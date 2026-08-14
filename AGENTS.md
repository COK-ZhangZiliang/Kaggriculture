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

### V2: market-aware mixed farm — 2026-08-06

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
- Its public score was observed at 1,531.5 on `2026-08-13T13:26Z`; simulation
  ratings are dynamic, so this is only a historical snapshot.

### V3A: observable-state execution control — 2026-08-13

- Preserved the V2 production route while adding actor-ordered field and shed
  shadow execution, atomic-plant repair, conservative market-flow inference,
  evidence-gated H1–H5 premium-sale timing, and capacity-safe terminal recovery.
- Final local candidate SHA-256
  `541d6a13e6d10ca61c00ffe5c46fd3722ea29f22b5b8ea8de6dd550f8f61a001`
  passed 40 automated tests, both required 720-state smoke matches, and
  deterministic three-file archive verification.
- In a fixed four-seed, both-seat paired diagnostic, it improved the margin in
  all 8 games against Kaito v27 and all 8 against Breaking Tie, but still lost
  every game; this is an execution-hardening result, not evidence of a large
  leaderboard gain. The V3A evidence was superseded by the V3B evidence file.
- V3A has not been uploaded to Kaggle or committed to GitHub. The current remote
  delivery remains V2 until a later explicitly authorized delivery cycle.

### V3B: adaptive 8C/4S market counter — 2026-08-13

- Replaced the V2/V3A economic tape with an 8-cow/4-sheep route reconstructed
  by majority vote from three public episodes, while retaining bounded weed and
  cow-placement recovery.
- Extended quantity-conserving one-turn sale leads to all scheduled products
  and added an evidence-gated second-order premium counter for observed H4
  market opponents.
- The frozen `main.py` candidate SHA-256
  `257d74f613f80607fba6fa68482e9db1eb07cb98618add47d45415b4f9079f54`
  swept 80/80 local games against four hash-pinned public strong artifacts,
  using unseen deterministic seeds, both seats, 720 states, and `DONE/DONE`.
  See `docs/v3b-strategy.md` and `docs/evidence/v3b-strong-holdout.json`.
- This is a fixed local artifact-panel result, not proof against future or
  hidden opponents and not a Kaggle score.
- Kaggle submission `55484203`, message
  `v3b adaptive 8c4s market counter 9bd601c`, reached `COMPLETE`; the uploaded
  `main.py` maps to Git commit
  `9bd601cb60150192986313049ce2a609644243e1`, and the archive SHA-256 is
  `b60f48ab876480c850821398ea52486ffc7e7da1a67faba657cbd665de1d67e0`.
- Its initial public score was observed at 600.0 on `2026-08-13T13:30Z`;
  simulation ratings are dynamic, so this is only a delivery snapshot.

### V3C: failure-driven execution and H7 repayment — 2026-08-14 (current)

- Reproduced all 17 captured V3B online losses exactly with engine `1.32.6`,
  then separated production-route deficits, market mirrors, and a cash-starved
  partial-purchase cascade. See `docs/v3c-strategy.md` and
  `docs/evidence/v3c-failure-analysis.json`.
- Kept the 8C/4S route; added first-day seed-surplus clipping, observable cow
  purchase reconciliation, a tightly gated ninth cow, and a seven-turn premium
  prepayment whose exact quantity is excluded from H1 and removed from the
  original sale.
- The final local `main.py` SHA-256 is
  `d9e26d7e45a944dd4e46adc28f66f7d9ae5c6974e71755debe6b291029aa79e0`.
  On fixed opponent tapes it improved 9 of 17 historical losses, left 8
  unchanged, regressed none, and flipped 3; this is an open-loop diagnostic,
  not a policy rematch.
- A final-hash fresh closed-loop holdout swept 64/64 both-seat games against
  four hash-pinned public artifacts, all 720 states and `DONE/DONE`, with a
  minimum margin of +116. The seeds do not overlap the V3B holdout.
- Kaggle submission `55500863`, message
  `v3c failure-driven h7 recovery 6aadc96`, reached `COMPLETE`; the uploaded
  `main.py` maps to Git commit
  `6aadc968f3cb0e81839532ff7f1ec0499b061f81`, and the archive SHA-256 is
  `90c800d2d51705a8662ed5d33d60f2953180f192f8091f2ab20d4886b29d13ef`.
- Its initial public score was observed at 600.0 on `2026-08-14T07:54:14Z`;
  simulation ratings are dynamic, so this is only a delivery snapshot.

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
