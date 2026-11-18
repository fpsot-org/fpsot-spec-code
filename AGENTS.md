# Instructions for agents

This repository holds the FPSOT code specification: how FPSOT projects write, format, lint and build their software. A common page sets the rules for every language: one pinned formatter and linter set per language, suppressions with reasons, SPDX headers, EditorConfig, declared toolchains, style editions, release file names and reproducible builds. Thirteen language pages follow: Java, Quarkus, Kotlin, Go, Bash, PowerShell, JavaScript and TypeScript, HTML and CSS, SQL, container files, CI workflows, configuration files and Python. Each names its tools, their versions, an owner role and a review-by date.

- The normative text is in `spec/en/` and `spec/fr/`. Every rule has an ID such as `COD-001`, and ends with a "Check:" line that names the tool or says "review".
- Follow `skill/SKILL.md` when you write or review code, build files, scripts, templates, container files, workflows or configuration in an FPSOT software repository. The spec text wins on any difference.
- Every page exists in English and in French, with the same file name and the same IDs.
- Terms and abbreviations come from the term base of `fpsot-spec-writing`. Add a missing term there first; `TERMS-NEEDED.md` lists the ones this spec waits for.
- This is a layer 1 specification. It may refer to the layer 0 specifications, to data types, vocabularies, data models, api-restful, testing, security, observability, identity, log and decisions. It never refers to the registry or capability specifications, except by topic.
- Other specifications own the outcomes: static analysis, secrets and the supply chain (security, SEC-012 to SEC-037), commits and tags (vcs), tests (testing), published names (naming), log records (observability), pages and themes (accessibility, style). Cite their rules; never restate them. This spec gives the per-tool mechanism.
- Override precedence, discovery, published BOMs and product assembly belong to the future capability specification. `overridable-rules.adoc` is informative and moves there later.
- The conflict resolutions on Java and Go listed in `to-be-confirmed.adoc` are not rules until the project lead confirms them.
- A version or tool fact that the research could not check at a primary source stays out of the rules, or is marked as unverified in the text.
- A tool change that reformats or newly fails existing code is a new style edition (COD-018): update `style-editions.adoc` and the tool tables, never change an edition in place.
- `examples/` holds conforming configuration files. When you change one, run `bash examples/test-examples.sh` (Python standard library only).
- Do not copy text from style guides, tool documentation or any other outside source. The PoshCode guide is CC BY-SA: summarize ideas only. Never cite books. Summarize in your own words and cite the exact version, with an archived copy.
- Commits follow Conventional Commits and are signed. Pull requests are squash-merged.
