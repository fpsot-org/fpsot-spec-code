---
name: fpsot-code
description: Coding rules for FPSOT software. Use when writing, formatting, linting, building or reviewing code, build files, scripts, templates, container files, GitHub Actions workflows or configuration files in an FPSOT repository, in Java, Quarkus, Kotlin, Go, Bash, PowerShell, JavaScript or TypeScript, HTML or CSS, SQL, YAML or Python.
---

# FPSOT code

Summary of the FPSOT code specification. It adds no rules of its own.
The spec text in `spec/` wins on any difference. Each line cites its requirement ID.
Each line keeps the strength of its rule: "must" and "must not" are MUST and MUST NOT, "should" is SHOULD, "may" is MAY.
Versions are those of style edition 2026; check the tool table of each page before you pin.

Other specs own the outcomes: static analysis, secrets and the supply chain (SEC-012 to SEC-037), commits and tags (VCS-001 to VCS-003, VCS-106), tests (TST-014, TST-065), published names (NAM-001 to NAM-023), log records (OBS-020, OBS-080), pages and themes (ACC-001, STY-001). Cite them; never restate them.

## Every language

- One pinned formatter and linter set per language, settings committed; CI fails on a formatter diff or a linter error (COD-002). If a tool can check a rule, the tool checks it in CI (COD-003).
- A repository meets the common page and the page of each language it holds (COD-004).
- A suppression names the rule, gives the reason in the same comment and has the smallest scope (COD-010). Generated and vendored code is excluded by path in the tool settings, never comment by comment (COD-011).
- Never silence a high or critical security finding with a comment alone: it needs a SEC-016 exception, cited in the comment (COD-012). Never turn off a rule of a named security analyzer (COD-013).
- `SPDX-License-Identifier` at the top of each file that allows comments (COD-014). Root `.editorconfig`: `root = true`, UTF-8, LF, final newline, no trailing white space except Markdown and AsciiDoc (COD-015).
- Toolchain versions live in committed files that CI reads (COD-016); one build command, the same locally and in CI, through the wrapper or pinned toolchain (COD-017).
- State the style edition in `CONTRIBUTING.md`; move edition with one reformat-only commit (COD-019).
- Names in code follow the language's conventions; names that leave the code follow the naming spec (COD-020).
- Release files: `<artifact>.cdx.json` SBOM, provenance, signature or a line in a signed `SHA256SUMS` (COD-021). Java archives and Go binaries must be reproducible; native executables, images and npm packages should be (COD-022).
- `AGENTS.md` should point to this skill and give the format, lint and test commands (COD-023).

## Java

- `maven.compiler.release` 21, fixed by the enforcer rule `requireProperty`; build and test on JDK 25; a non-blocking job on the latest feature JDK (COD-100). No preview features in published artifacts; CI searches for `--enable-preview` (COD-101). Tests run on JUnit Jupiter (TST-006).
- Quarkus formatter settings with `formatter:validate` and `impsort:check` in CI (COD-102).
- `@NullMarked` on every package; NullAway at error level with JSpecify support (COD-103). Error Prone, SpotBugs with Find Security Bugs and ArchUnit in the build (COD-104).
- Expected outcomes are sealed types handled by an exhaustive `switch`; exceptions extend `RuntimeException`, for bugs and infrastructure only; always pass the cause (COD-105). Never `null` for an empty collection or `Optional`; no Java serialization (COD-106).
- Maven only, through the wrapper with `distributionSha256Sum`; Gradle only for Kotlin Multiplatform (COD-107). Every version in `dependencyManagement` or a BOM; plugins pinned; enforcer rules `requireMavenVersion`, `requireJavaVersion`, `requirePluginVersions`, `dependencyConvergence`, `banDynamicVersions` (COD-108).
- `project.build.outputTimestamp`; release CI runs `artifact:compare` and publishes `.buildinfo` (COD-109). japicmp or Revapi against the last release (COD-110). `Automatic-Module-Name` without `module-info`, should follow NAM-022 (COD-111).
- Never pool virtual threads; should limit scarce resources explicitly (COD-112). Maven Central: signature, sources, Javadoc, full POM metadata (COD-113). Domain and ports never import adapters, checked by ArchUnit (COD-114).

## Quarkus

- Main line on the current LTS, 3.40; should test the latest release (COD-200).
- Extensions: runtime never depends on deployment (COD-201); build steps talk only through build items, read classes through Jandex (COD-202); `@ConfigMapping` under `quarkus.<extension>`, Javadoc on each property; applications never use the `quarkus.` prefix (COD-203).
- Constructor injection; injected and producer members package-private, not private (COD-204). Domain and port packages of a PSC library import no `jakarta.*` or `io.quarkus.*`, checked by ArchUnit (COD-205, with COD-114). No `CDI.current()` or `Arc.container()`; a bean that only code outside CDI injection reaches carries `@Unremovable`, or its extension produces an `UnremovableBeanBuildItem` (COD-206).
- Native metadata through build items; `@RegisterForReflection` only in applications; review agent-generated metadata (COD-207). Honest `status` in `quarkus-extension.yaml`, one feature, capabilities not class path probes, `QuarkusExtensionTest` (COD-208).
- Native builds: Mandrel 25 builder pinned by digest under SEC-031, same JDK major, explicit `native-image-xmx` and `--parallelism` (COD-209); release CI runs `@QuarkusIntegrationTest` on the executable (COD-210); SBOM from `quarkus-cyclonedx`; libraries and extensions ship Java archives only (COD-211).
- Should use Dev Services, Testcontainers in plain libraries, `@QuarkusComponentTest` for beans (COD-212). Libraries and extensions should log through `org.jboss.logging.Logger`; `io.quarkus.logging.Log` only in applications (COD-213).

## Kotlin

- In Quarkus: the platform's Kotlin version, `all-open`, constructor injection (COD-300). ktlint with `ktlint_official`, detekt 1.23.8 (COD-301). Explicit API mode in libraries (COD-302).
- Sealed results; no `kotlin.Result` or `Either` in public domain APIs; `@Throws` for Java callers (COD-303). Shared code in a framework-free `commonMain`; Wasm only in pilots while Beta (COD-304). Should use `@JvmOverloads`, `@JvmStatic` and explicit types for Java callers (COD-305).

## Go

- Build with the latest 1.27.x; `go` line at 1.26; move to a new major within 6 months (COD-400).
- `govulncheck` 1.10.0; tests with `go test` (TST-006).
- `golangci-lint fmt` and `run`, config `version: "2"`, `standard` plus `nolintlint`, `gosec`, `errorlint`, `revive`, `bodyclose`, `contextcheck`; `gofmt` and `goimports` (COD-401). `go vet`, `go test -race`, `govulncheck` (COD-402).
- Exact `GOTOOLCHAIN` in CI; `go mod tidy` leaves no diff; `go mod verify`; commit `go.sum` (COD-403). Releases: `CGO_ENABLED=0`, `-trimpath`, built twice and compared (COD-404).
- `errors.Is`, `errors.As`, `errors.AsType`, never `==` on a wrapped error; never `%w` on a pointer to a value-receiver error type; should use `%w` only when callers inspect the cause, `%v` otherwise (COD-405). Should log with `log/slog` JSON, fuzz parsers (COD-406). CLIs should exit 0, 1 or 2, write errors to stderr, offer `--help` and `--version` (COD-407).

## Bash

- `#!/usr/bin/env bash`, Bash 4.4+; POSIX `sh` only where no Bash exists (COD-500). ShellCheck clean; `shfmt -d` with 2 spaces (COD-501).
- Quote every expansion; `"$@"`, `[[ ]]`, `$( )`; no `eval`, found by a CI search; commit `.shellcheckrc` with `enable=require-double-brackets` (COD-502). Should start with `set -Eeuo pipefail` and `shopt -s inherit_errexit`; still check critical commands; errors to stderr (COD-503).
- `mktemp` plus a `trap` on `EXIT`; no fixed temp paths (COD-504). Over 100 lines by `wc -l`, or parsing JSON or XML: rewrite in Go (COD-505). Should test with bats-core (COD-506).

## PowerShell

- `#Requires -Version 5.1` or `7.6`; CI tests each declared edition (COD-550). PSScriptAnalyzer with committed settings: formatting rules on, `PSUseCompatibleSyntax` with `'5.1'` and `'7.0'` (COD-551).
- Approved verbs, no aliases, named parameters, no `Invoke-Expression`, no plain-text secrets (COD-552). Modules export by explicit name, never dot-source; `PSUseToExportFieldsInManifest` helps check it (COD-553).
- Authenticode-signed releases; never tell users to set `Bypass` machine-wide (COD-554). `[CmdletBinding()]`, `try`/`catch` with `-ErrorAction Stop`, no empty `catch` (COD-555).
- Should pass `PSUseConstrainedLanguageMode` for App Control hosts (COD-556), test with Pester on each edition (COD-557), read secrets through SecretManagement (COD-558).

## JavaScript and TypeScript

- Node.js 26 for new work; only active or maintenance LTS lines; `engines` and `.node-version` (COD-600).
- TypeScript 6.0.x for type checks and lint while typescript-eslint lacks TS 7; TS 7 may compile (COD-601). `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, `noImplicitOverride`, `verbatimModuleSyntax`; ESM only (COD-602).
- ESLint flat config, typescript-eslint `strictTypeChecked`, eslint-comments `require-description`; Prettier (COD-603).
- Commit the lockfile, `npm ci`; `.npmrc` with `ignore-scripts=true`, `allow-git=none`, `engine-strict=true`, `min-release-age` of 3 days or more (COD-604). Tests run on Vitest or `node:test` (TST-006). Publish through trusted publishing with provenance (COD-605).
- Server-rendered HTML with progressive enhancement; a SPA framework needs a recorded decision (COD-606). Keyed data from outside goes in `Map` or `Set`; no unchecked key copies into plain objects (COD-607).

## HTML and CSS

- Rendered pages pass the Nu HTML Checker in CI (COD-650). No inline scripts, `style` attributes or event-handler attributes; scripts work under a CSP without `'unsafe-inline'` or `'unsafe-eval'` (COD-651).
- Never `raw` or `safe` on data a person supplied in Qute (COD-652). stylelint with `stylelint-config-standard`; colors, spacing and type only from design-system custom properties, with `stylelint-declaration-strict-value` (COD-653). Should use `@layer` layering, BEM-style block names, PatternFly first (COD-654).

## SQL

- PostgreSQL 18, or 17; no end-of-life major (COD-700). Flyway; no Liquibase 5 before a license review (COD-701).
- Never change an applied migration; `quarkus.flyway.clean-disabled=true` outside tests; migrate in a separate job (COD-702). Backward-compatible migrations, expand then contract; `CREATE INDEX CONCURRENTLY`, `NOT VALID` then `VALIDATE CONSTRAINT`, `lock_timeout` (COD-703).
- Parameters for every value; allow-list dynamic identifiers (COD-704). sqlfluff with the `postgres` dialect (COD-705). Should use identity columns, `timestamptz`, `NOT NULL`; table and column names in snake_case per NAM-010, meeting NAM-004, NAM-009 and NAM-013 (COD-706).

## Container files

- `Containerfile` (Quarkus may keep `src/main/docker/Dockerfile.jvm` and `Dockerfile.native`), hadolint at `warning` (COD-750). `FROM` carries the SEC-031 digest with the tag in a comment; multi-stage; numeric non-root last `USER`, checked by a CI search (COD-751).
- OCI labels `source`, `revision`, `version`, `licenses` (COD-752). Rootless Podman or Buildah builds; secrets through secret mounts only (COD-753). Should use `--source-date-epoch`, `--rewrite-timestamp` and snapshot package repositories (COD-754).

## CI workflows

- Top-level `permissions: {}` or `contents: read`; raise per job (COD-800). `persist-credentials: false`; no outside-controlled `${{ }}` in `run`, pass it through `env` (COD-801). Never check out PR code under `pull_request_target` or `workflow_run` (COD-802).
- actionlint and zizmor as required checks; zizmor asks for hash pins (COD-803). Releases in a reusable workflow with artifact attestations; should call the shared FPSOT release workflow once it exists (COD-804). `timeout-minutes` on each job with steps, found by a CI search; `concurrency` on deploy and release workflows (COD-805). Should run OpenSSF Scorecard (COD-806).

## Configuration files

- yamllint with `truthy` limited to `true` and `false` and duplicate keys as errors (COD-850). check-jsonschema on every file with a published schema (COD-851). FPSOT-defined formats ship a JSON Schema 2020-12 (COD-852).

## Python

- Tooling only, never a shipped service (COD-900). `requires-python = ">=3.12"`; CI on 3.14 (COD-901).
- `ruff check` with `S` rules and `ruff format --check`; `mypy --strict` or strict pyright (COD-902). Locked dependencies: `uv.lock`, PEP 723 metadata or hashed requirements (COD-903).
- No `shell=True`, `eval` or `exec` on outside data; no `pickle`, unsafe YAML loaders or entity-resolving XML parsers on outside data (COD-904).
