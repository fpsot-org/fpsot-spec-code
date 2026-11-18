# Terms needed

Entries in the format of `termbase/terms.yaml` of fpsot-spec-writing, for a pull request to the term base.
The pages of this specification write these terms in plain text for now, and will use the term attributes once the term base has them.
The French forms marked "to confirm" have no record in the Grand dictionnaire terminologique that the writer checked.

```yaml
  - id: cwe
    kind: abbreviation
    en: {short: "CWE", full: "Common Weakness Enumeration", definition: "A list, kept by MITRE, of the kinds of weakness in software and hardware, each with a number."}
    fr: {short: "CWE", full: "Common Weakness Enumeration", definition: "Liste, tenue par MITRE, des types de faiblesses des logiciels et du matériel, chacun avec un numéro."}
    source: {name: "MITRE, CWE (proper name, kept in English)", url: "https://cwe.mitre.org/top25/archive/2025/2025_cwe_top25.html", checked: "2026-11-18"}
  - id: jdk
    kind: abbreviation
    en: {short: "JDK", full: "Java Development Kit", definition: "The set of tools that compiles, runs and packages Java programs."}
    fr: {short: "JDK", full: "Java Development Kit", definition: "Ensemble d’outils qui compile, exécute et emballe les programmes Java."}
    source: {name: "OpenJDK (proper name, kept in English)", url: "https://openjdk.org/jeps/12", checked: "2026-11-18"}
  - id: jvm
    kind: abbreviation
    en: {short: "JVM", full: "Java virtual machine", definition: "The program that runs Java bytecode on a given system."}
    fr: {short: "JVM", full: "machine virtuelle Java", definition: "Programme qui exécute le bytecode Java sur un système donné."}
    source: {name: "OpenJDK; French form to confirm", url: "https://openjdk.org/jeps/12", checked: "2026-11-18"}
  - id: jep
    kind: abbreviation
    en: {short: "JEP", full: "JDK Enhancement Proposal", definition: "A numbered proposal that describes one change to the JDK, such as a language feature."}
    fr: {short: "JEP", full: "JDK Enhancement Proposal", definition: "Proposition numérotée qui décrit une modification du JDK, comme une fonctionnalité du langage."}
    source: {name: "OpenJDK, JEP 12 (proper name, kept in English)", url: "https://openjdk.org/jeps/12", checked: "2026-11-18"}
  - id: cdi
    kind: abbreviation
    en: {short: "CDI", full: "Contexts and Dependency Injection", definition: "The Jakarta standard that creates objects, called beans, and gives each one the objects it depends on."}
    fr: {short: "CDI", full: "Contexts and Dependency Injection", definition: "Norme Jakarta qui crée des objets, appelés beans, et fournit à chacun les objets dont il dépend."}
    source: {name: "Quarkus, Contexts and Dependency Injection (proper name, kept in English)", url: "https://quarkus.io/guides/cdi-reference", checked: "2026-11-18"}
  - id: spdx
    kind: abbreviation
    en: {short: "SPDX", full: "System Package Data Exchange", definition: "An open standard of the Linux Foundation for license identifiers and for lists of software components."}
    fr: {short: "SPDX", full: "System Package Data Exchange", definition: "Norme ouverte de la Linux Foundation pour les identifiants de licence et les listes de composants logiciels."}
    source: {name: "SPDX project (proper name, kept in English)", url: "https://spdx.dev/learn/handling-license-info/", checked: "2026-11-18"}
  - id: slsa
    kind: abbreviation
    en: {short: "SLSA", full: "Supply-chain Levels for Software Artifacts", definition: "An OpenSSF framework of levels for the integrity of how software artifacts are built."}
    fr: {short: "SLSA", full: "Supply-chain Levels for Software Artifacts", definition: "Cadre de l’OpenSSF qui définit des niveaux d’intégrité de la construction des artefacts logiciels."}
    source: {name: "SLSA (proper name, kept in English); also used by the security specification", url: "https://slsa.dev/spec/v1.2/", checked: "2026-11-18"}
  - id: oci
    kind: abbreviation
    en: {short: "OCI", full: "Open Container Initiative", definition: "The Linux Foundation project that sets the formats of container images and runtimes."}
    fr: {short: "OCI", full: "Open Container Initiative", definition: "Projet de la Linux Foundation qui fixe les formats des images et des environnements d’exécution de conteneurs."}
    source: {name: "Open Container Initiative (proper name, kept in English)", url: "https://github.com/opencontainers/image-spec/blob/main/annotations.md", checked: "2026-11-18"}
  - id: yaml
    kind: abbreviation
    en: {short: "YAML", full: "YAML Ain’t Markup Language", definition: "A text format for structured data that uses indentation, common in configuration files."}
    fr: {short: "YAML", full: "YAML Ain’t Markup Language", definition: "Format texte pour les données structurées qui repose sur l’indentation, courant dans les fichiers de configuration."}
    source: {name: "yaml.org (proper name, kept in English)", url: "https://yaml.org/spec/1.2.2/", checked: "2026-11-18"}
  - id: toml
    kind: abbreviation
    en: {short: "TOML", full: "Tom’s Obvious, Minimal Language", definition: "A text format for configuration files, made of keys, values and tables."}
    fr: {short: "TOML", full: "Tom’s Obvious, Minimal Language", definition: "Format texte pour les fichiers de configuration, fait de clés, de valeurs et de tables."}
    source: {name: "toml.io (proper name, kept in English)", url: "https://toml.io/en/v1.0.0", checked: "2026-11-18"}
  - id: pep
    kind: abbreviation
    en: {short: "PEP", full: "Python Enhancement Proposal", definition: "A numbered document that proposes or describes a change to Python or its tools."}
    fr: {short: "PEP", full: "Python Enhancement Proposal", definition: "Document numéroté qui propose ou décrit une modification de Python ou de ses outils."}
    source: {name: "Python Software Foundation (proper name, kept in English)", url: "https://peps.python.org/pep-0723/", checked: "2026-11-18"}
  - id: posix
    kind: abbreviation
    en: {short: "POSIX", full: "Portable Operating System Interface", definition: "The IEEE and Open Group standard for the interfaces and the shell of Unix-like systems."}
    fr: {short: "POSIX", full: "Portable Operating System Interface", definition: "Norme de l’IEEE et de l’Open Group pour les interfaces et l’interpréteur de commandes des systèmes de type Unix."}
    source: {name: "The Open Group (proper name, kept in English)", url: "https://pubs.opengroup.org/onlinepubs/9799919799/", checked: "2026-11-18"}
  - id: formatter
    kind: term
    en: {full: "formatter", definition: "A tool that rewrites source code into one fixed layout."}
    fr: {full: "outil de mise en forme", definition: "Outil qui réécrit le code source selon une mise en page fixe."}
    source: {name: "FPSOT code specification, COD-002; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-code", checked: "2026-11-18"}
  - id: linter
    kind: term
    en: {full: "linter", definition: "A tool that reads source code without running it and reports errors, risky patterns and breaches of style."}
    fr: {full: "analyseur statique", definition: "Outil qui lit le code source sans l’exécuter et signale les erreurs, les constructions risquées et les écarts de style."}
    source: {name: "FPSOT code specification, COD-002; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-code", checked: "2026-11-18"}
  - id: finding
    kind: term
    en: {full: "finding", definition: "One problem that a linter or an analyzer reports at one place in the code."}
    fr: {full: "constat", definition: "Problème qu’un analyseur signale à un endroit du code."}
    source: {name: "FPSOT code specification, COD-010; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-code", checked: "2026-11-18"}
  - id: style-edition
    kind: term
    en: {full: "style edition", definition: "A named set of formatters and linters, with their versions and settings, that a project adopts as a whole."}
    fr: {full: "édition de style", definition: "Ensemble nommé d’outils de mise en forme et d’analyseurs statiques, avec leurs versions et leurs paramètres, qu’un projet adopte en bloc."}
    source: {name: "FPSOT code specification, COD-018, after the style editions of Rust; French form to confirm", url: "https://github.com/rust-lang/rust/blob/master/src/doc/style-guide/src/editions.md", checked: "2026-11-18"}
  - id: toolchain
    kind: term
    en: {full: "toolchain", definition: "The compiler or runtime of a language, with the tools that come with it, at one version."}
    fr: {full: "chaîne d’outils", definition: "Compilateur ou environnement d’exécution d’un langage, avec les outils qui l’accompagnent, à une version donnée."}
    source: {name: "Go Toolchains, for the English form; French form to confirm", url: "https://go.dev/doc/toolchain", checked: "2026-11-18"}
  - id: lock-file
    kind: term
    en: {full: "lock file", definition: "A committed file that records the exact version and checksum of each resolved dependency."}
    fr: {full: "fichier de verrouillage", definition: "Fichier versionné qui consigne la version exacte et l’empreinte de chaque dépendance résolue."}
    source: {name: "npm Docs, config; French form to confirm", url: "https://docs.npmjs.com/cli/v11/using-npm/config", checked: "2026-11-18"}
  - id: reproducible-build
    kind: term
    en: {full: "reproducible build", definition: "A build that gives the same bytes each time from the same source, tools and settings."}
    fr: {full: "construction reproductible", definition: "Construction qui donne les mêmes octets chaque fois, à partir de la même source, des mêmes outils et des mêmes paramètres."}
    source: {name: "Apache Maven, Configuring for Reproducible Builds; French form to confirm", url: "https://maven.apache.org/guides/mini/guide-reproducible-builds.html", checked: "2026-11-18"}
  - id: plugin
    kind: term
    en: {full: "plugin", definition: "A component that adds a function to a tool, such as a build tool or a linter."}
    fr: {full: "plugiciel", definition: "Composant qui ajoute une fonction à un outil, comme un outil de construction ou un analyseur statique."}
    source: {name: "Office québécois de la langue française, plugiciel; to confirm", url: "https://vitrinelinguistique.oqlf.gouv.qc.ca/", checked: "2026-11-18"}
  - id: framework
    kind: term
    en: {full: "framework", definition: "A body of code that calls the code of an application and gives it a structure, such as Quarkus."}
    fr: {full: "cadriciel", definition: "Ensemble de code qui appelle le code d’une application et lui donne une structure, comme Quarkus."}
    source: {name: "Office québécois de la langue française, cadriciel; to confirm", url: "https://vitrinelinguistique.oqlf.gouv.qc.ca/", checked: "2026-11-18"}
  - id: virtual-thread
    kind: term
    en: {full: "virtual thread", definition: "A light Java thread that the JDK schedules on a small number of platform threads."}
    fr: {full: "fil virtuel", definition: "Fil d’exécution Java léger que le JDK planifie sur un petit nombre de fils de la plateforme."}
    source: {name: "OpenJDK, JEP 444, for the English form; French form to confirm", url: "https://openjdk.org/jeps/444", checked: "2026-11-18"}
  - id: sealed-type
    kind: term
    en: {full: "sealed type", definition: "A class or interface that names every type allowed to extend or implement it."}
    fr: {full: "type scellé", definition: "Classe ou interface qui nomme chaque type autorisé à l’étendre ou à la mettre en œuvre."}
    source: {name: "OpenJDK, JEP 409, for the English form; French form to confirm", url: "https://openjdk.org/jeps/409", checked: "2026-11-18"}
  - id: long-term-support
    kind: term
    en: {full: "long-term support", definition: "A release line that its publisher fixes for a stated, longer period than other releases."}
    fr: {full: "soutien à long terme", definition: "Branche de versions que son éditeur corrige pendant une période annoncée, plus longue que pour les autres versions."}
    source: {name: "Quarkus releases, for the English form; French form to confirm", url: "https://quarkus.io/releases/", checked: "2026-11-18"}
  - id: workflow
    kind: term
    en: {full: "workflow", definition: "A file that tells a CI service which jobs to run, on which events."}
    fr: {full: "flux de travail", definition: "Fichier qui indique à un service d’IC quelles tâches exécuter, et à quels événements."}
    source: {name: "GitHub Docs, Secure use reference; French form to confirm", url: "https://docs.github.com/en/actions/reference/security/secure-use", checked: "2026-11-18"}
  - id: content-security-policy
    kind: term
    en: {full: "content security policy", definition: "A response header that tells the browser which sources of scripts, styles and other content a page may use."}
    fr: {full: "politique de sécurité du contenu", definition: "En-tête de réponse qui indique au navigateur les sources de scripts, de styles et d’autres contenus qu’une page peut employer."}
    source: {name: "MDN Web Docs, CSP: script-src; French form to confirm", url: "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/script-src", checked: "2026-11-18"}
  - id: progressive-enhancement
    kind: term
    en: {full: "progressive enhancement", definition: "Building a page that works in plain HTML first, then adding styles and scripts that improve it where they run."}
    fr: {full: "amélioration progressive", definition: "Façon de construire une page qui fonctionne d’abord en HTML simple, puis d’ajouter des styles et des scripts qui l’améliorent là où ils s’exécutent."}
    source: {name: "GOV.UK Service Manual; French form to confirm", url: "https://www.gov.uk/service-manual/technology/using-progressive-enhancement", checked: "2026-11-18"}
  - id: single-page-application
    kind: term
    en: {full: "single-page application", definition: "A web application that loads one page and then renders each view with scripts in the browser."}
    fr: {full: "application monopage", definition: "Application Web qui charge une seule page, puis affiche chaque vue au moyen de scripts dans le navigateur."}
    source: {name: "FPSOT code specification, COD-606; French form to confirm", url: "https://github.com/fpsot-org/fpsot-spec-code", checked: "2026-11-18"}
  - id: trusted-publishing
    kind: term
    en: {full: "trusted publishing", definition: "Publishing a package from CI with a short-lived identity token instead of a stored secret."}
    fr: {full: "publication de confiance", definition: "Publication d’un paquet depuis l’IC au moyen d’un jeton d’identité de courte durée, au lieu d’un secret conservé."}
    source: {name: "npm Docs, Trusted publishing; French form to confirm", url: "https://docs.npmjs.com/trusted-publishers/", checked: "2026-11-18"}
```
