# Changelog

All notable changes to this specification are listed here.
The format follows [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/),
and versions follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-11-21

### Changed

- COD-706 cites the new SQL row of NAM-010 (naming 0.5.2) for the case of table and column names, instead of setting it here.

## [0.1.0] - 2026-11-18

### Added

- Scope, tools that decide, conformance of a repository and owner and review dates of each language page, COD-001 to COD-005: one pinned formatter and linter set per language with committed settings and a failing CI; each rule names its check, a tool or review; a review-by date at most 12 months after the last review.
- Common rules COD-010 to COD-023: suppressions that name the rule and give a reason; generated code excluded by path; high and critical security findings only through a SEC-016 exception; security analyzer rules kept on, with a map to the 2025 CWE Top 25; SPDX headers; a root `.editorconfig`; declared toolchains; one build command; style editions and how a repository states and moves edition; names in code; release file names; reproducible builds as a MUST for Java archives and Go binaries; `AGENTS.md` pointers.
- Java COD-100 to COD-114: Java 21 bytecode built and tested on Java 25; no preview features; the Quarkus formatter settings; JSpecify `@NullMarked` with NullAway; Error Prone, SpotBugs with Find Security Bugs and ArchUnit; sealed results and unchecked exceptions; Maven with a checked wrapper; enforcer rules for pinned versions; reproducible archives; japicmp; `Automatic-Module-Name`; no pooled virtual threads; Maven Central requirements; ports and adapters.
- Quarkus COD-200 to COD-213: the 3.40 long-term line with a path to 4.x; runtime and deployment modules; build items; `@ConfigMapping`; constructor injection and package-private members; rule modules without framework imports; no `CDI.current()`; native metadata through build items; extension status; digest-pinned Mandrel 25 builds with explicit limits; native integration tests; `quarkus-cyclonedx`; Dev Services; JBoss Logging in libraries.
- Kotlin COD-300 to COD-305, Go COD-400 to COD-407, Bash COD-500 to COD-506, PowerShell COD-550 to COD-558, JavaScript and TypeScript COD-600 to COD-607, HTML and CSS COD-650 to COD-654, SQL COD-700 to COD-706, container files COD-750 to COD-754, CI workflows COD-800 to COD-806, configuration files COD-850 to COD-852 and Python COD-900 to COD-904.
- Informative pages on style editions, with edition 2026; on overridable rules in Quarkus, marked for transfer to the future capability specification; and on guidance awaiting confirmation by the project lead.
- Example configuration files: `.editorconfig`, golangci-lint version 2, an ESLint flat configuration, PSScriptAnalyzer settings, a Maven Enforcer Plugin snippet, hadolint, yamllint and zizmor configurations, and a workflow that runs actionlint and zizmor. `examples/check-examples.py` checks them with the Python standard library, `examples/test-examples.sh` checks that it rejects broken copies, and the `examples` job of the continuous integration runs both.
- Comparison data with international rows, and rows for Canada, Québec and France.
- How-to guide that puts a repository under the specification.

### Known gaps

- The Québec row on control SA-15 of the security référentiel waits for an archived copy of its source.
- Twelve recorded resolutions on Java and Go wait for the project lead to confirm them.

[Unreleased]: https://github.com/fpsot-org/fpsot-spec-code/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/fpsot-org/fpsot-spec-code/releases/tag/v0.1.0
