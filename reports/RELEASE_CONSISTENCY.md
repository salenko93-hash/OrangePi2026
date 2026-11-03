# Release consistency audit — 2026-11-03

Scope: supplied checkout, runtime version 3.7.5 from server/version.py.
Neither .git nor .github/workflows existed at initial inspection. Git status and
remote inspection returned "not a git repository". No AGENTS.md was found.
Release tags, ZIP publication and prior PR/CI claims cannot be confirmed here.
No release URLs or runtime version were invented or bumped.

README now describes the actual check-only installer default and explicit version
approval. Old artifact-branch links and personal board/IP/repair narrative were
removed; useful repair links, device limits and historical evidence remain in
the installation guide and reports/validation.json. That JSON remains a historical
3.7.4 report, not current-version validation. The prior 3.7.5-rc.1 report is marked
historical and its unsupported CI/publication claims are qualified.

Both app startup messages use VERSION. The native installer reads the installed
server/version.py for its completion message; the service description and repair
banner no longer embed an application version. Historical backup filenames remain
unchanged. No app decomposition was needed; tests execute main with mocked service
dependencies, avoiding app imports that initialize runtime data.

The minimal GitHub Actions workflow uses the existing VERIFY_PROJECT.py command,
Windows/Ubuntu, Python 3.12 and Node.js 22 with UTF-8 enabled. It neither publishes
nor deploys. Its inclusion restores the cross-platform verification described by
the project, but is not evidence of any GitHub Actions run. Python 3.10+ remains
the documented runtime minimum; the CI matrix is not proof of every runtime.

Repeat audit of the current files — 2026-11-03:

README is the canonical Windows installation/upgrade sequence: confirmed package
and tag, CheckOnly, then the same tag with the exact approved runtime version.
Both guides link to it. Speculative rc-tag examples and direct native-install
instructions were removed from the operator path. Historical repair observations
are labelled; diagnostic scripts come from the confirmed package, not an assumed
main-branch download. Old full-installer recommendations were removed.

The release builder excludes .github from ZIPs. Consequently, absence of workflows
in a supplied archive does not establish their absence in the upstream repository.
The README no longer links to a workflow file missing from its own release ZIP.
The workflow currently in this source tree was reviewed without modification:
push/pull_request/manual triggers, contents:read, Windows/Ubuntu matrix, Python
3.12, Node.js 22, UTF-8, dependency installation from requirements.txt and the
existing full verification command. No confirmed workflow defect was found.

Previous local verification on Windows, Python 3.15.1 and Node.js 24.22.1
(before the final documentation/test corrections below):

- `python -B -m unittest discover -s tests -p test_release_consistency.py -v`:
  4 passed, including a guard against pinned unconfirmed tags/old installer advice.
- Git Bash `bash -n scripts/install.sh`: passed.
- `python -B VERIFY_PROJECT.py`: success; 131 tests discovered, 112 passed,
  19 skipped for platform/optional native dependencies. All 16 JavaScript files
  passed syntax checks; all 8 JavaScript runtime scenarios passed. Runtime version,
  initial-data manifest and offline demo checks passed.
- Ruff is unavailable in this environment; no lint success is claimed.
- YAML validation was not performed: actionlint/yamllint were not on PATH;
  PyYAML/ruamel were absent in both installed Python 3.15/3.14 environments;
  Node yaml/js-yaml were also unavailable. Manual review is not validator output.
- Only Python 3.15/3.14 were listed by `py -0p`; Python 3.12, Node.js 22 and
  Ubuntu were not executed locally. Local tests used the UTF-8 and no-bytecode
  environment settings used by the workflow.

These local results are not a GitHub Actions run or Linux verification. No physical
Orange Pi, HDMI, audio, cursor or Windows SSH installation was tested in this audit.

Readiness: ready to submit for the first CI run, with YAML validation and the
actual Windows/Ubuntu Python 3.12 matrix still unconfirmed. This is not evidence
that CI passed or that a release/device is ready.

Repository-owner steps still required:

1. Apply/review these files in the real Git repository; confirm its actual remote,
   commit, tag and workflow state. No remote or current commit was inferred here.
2. Validate verify.yml (for example with actionlint), run GitHub Actions and retain
   the run URL and results for both matrix jobs. CI here does not publish a release.
3. After checks, build with tools/build_release.py and verify the intended GitHub
   release tag, ZIP, .sha256 sidecar and asset digest. Give operators that confirmed
   tag only after publication; no release asset was built or published by this audit.
4. Perform separate Orange Pi installation/update/rollback and physical HDMI,
   audio, cursor/cold-start acceptance checks before declaring hardware readiness.

Final independent review — 2026-11-03:

Two documentation defects were confirmed and corrected without runtime changes:
INSTALL_ORANGEPI.md promised certificate renewal by rerunning the full installer,
although install.sh rejects an existing installation and transactional updates do
not run configure_https.sh. GITHUB_RELEASE_UPDATES.md now distinguishes CLI check
journaling from Windows CheckOnly, which uses download and read-only SSH preflight
without writing the installed updater journal. Exact approval, check-only default,
explicit tag requirement and prerelease opt-in agree with the inspected code.

Targeted regressions: the TLS documentation guard, actual CLI download/check
journal behavior on a disposable fixture, and existing version/consent checks.
Command (PYTHONUTF8=1, PYTHONDONTWRITEBYTECODE=1, PYTHONPATH=server;tests):
`python -B -m unittest test_release_consistency test_official_updates.OfficialUpdateTests.test_download_does_not_write_installed_journal_but_cli_check_does test_official_updates.OfficialUpdateTests.test_check_is_read_only_and_apply_requires_exact_consent_and_newer_version -v`
Result: 7 passed on Python 3.15.1. Git Bash `bash -n scripts/install.sh` passed.
These are auxiliary local checks, not a rerun of the CI matrix. The earlier full
VERIFY result above predates these final documentation/test changes.

Git inspection again found no .git: status/remote commands failed as not a Git
repository. Python enumeration again listed only 3.15/3.14; Node was 24.22.1.
No actionlint/yamllint, Python yaml/ruamel or Node yaml/js-yaml was available.
Nothing was installed; no YAML validation or Python 3.12/Node.js 22 CI-equivalent
run was performed. The workflow was read, not validated by a YAML tool.

The owner still needs both GitHub Actions jobs (Windows/Ubuntu with Python 3.12,
Node.js 22, PYTHONUTF8=1): `python -m pip install -r requirements.txt`, then
`python -B VERIFY_PROJECT.py`, plus workflow validation. No Actions outcome,
published tag/ZIP or physical Orange Pi acceptance is confirmed by this review.

GitHub CI access inspection — 2026-11-03:

New remote evidence, obtained without changing runtime code or dispatching a run:
`gh auth status` confirmed an authenticated account; `gh repo view
salenko93-hash/OrangePi --json nameWithOwner,defaultBranchRef,viewerPermission,isArchived`
confirmed access with ADMIN permission, default branch main, and no archive flag.
This repository was selected from the updater configuration, not from a local
remote: .git remains absent and git status/remote inspection still fails.

`gh workflow list --repo salenko93-hash/OrangePi --all` listed the active
verification workflow (ID 403410421) and a separate publication workflow. The
publication workflow was not invoked. Remote main was observed at
8497ff7764705513d537435c252c5a5c5a268ee7; this is not a commit assigned to the
local checkout.

The connector fetched .github/workflows/verify.yml from main and
feat/official-release-updates. Both use Python 3.12 but Node.js 24, install
requirements.txt plus Ruff, and run Ruff, VERIFY_PROJECT.py and Linux shell syntax
checks. The fix/windows-verification-rollback-watchdog branch returned 404 for
that workflow. Fetching tests/test_release_consistency.py from main also returned
404, confirming that the inspected upstream tree lacks a current local test.

Local verify.yml instead specifies Node.js 22, requirements.txt and
`python -B VERIFY_PROJECT.py` for both Windows/Ubuntu matrix entries. It was read,
not validated by GitHub Actions. Dispatching the inspected upstream workflow would
test another tree and Node.js version; no run was dispatched or represented as
verification of this checkout. Windows CI result: NOT RUN. Ubuntu CI result:
NOT RUN. No new local unit/full verification run was performed in this access check.

Owner action: review/synchronize the current checkout and Node.js 22 workflow into
a real Git branch first, keeping publication disabled. Then select that branch
in Actions / Verify / Run workflow (workflow_dispatch is available on main),
wait for both matrix entries and retain their run/job URLs and step results.
Required evidence remains Python 3.12 and Node.js 22 setup, requirements.txt
installation and a successful `python -B VERIFY_PROJECT.py` on each OS. No tag,
release or ZIP was created; no physical device verification was performed.
