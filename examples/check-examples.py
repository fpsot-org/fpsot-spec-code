#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Checks the example configuration files in examples/.

Each file must parse, and must hold the settings that the rules of the code
specification ask for. Python standard library only, no network.

Usage: python3 -I examples/check-examples.py [REPOSITORY]
"""

import configparser
import json
import re
import sys
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path


class YamlError(Exception):
    pass


# --- A small YAML reader -------------------------------------------------------
# The examples keep to a subset of YAML: block mappings and sequences, plain or
# quoted scalars, and one-line flow lists and mappings. The reader rejects tabs in
# indentation and repeated keys, like yamllint with key-duplicates.

def _strip_comment(line):
    quote = None
    for i, c in enumerate(line):
        if quote:
            if c == quote:
                quote = None
        elif c in "\"'":
            quote = c
        elif c == "#" and (i == 0 or line[i - 1] in " \t"):
            return line[:i].rstrip()
    if quote:
        raise YamlError("unterminated quote")
    return line.rstrip()


def _split_flow(text):
    items, depth, quote, cur = [], 0, None, ""
    for c in text:
        if quote:
            cur += c
            if c == quote:
                quote = None
            continue
        if c in "\"'":
            quote = c
        elif c in "[{":
            depth += 1
        elif c in "]}":
            depth -= 1
        elif c == "," and depth == 0:
            items.append(cur.strip())
            cur = ""
            continue
        cur += c
    if quote or depth:
        raise YamlError("unbalanced flow collection: " + text)
    if cur.strip():
        items.append(cur.strip())
    return items


def _split_key(text):
    """Returns (key, rest) when text is a mapping entry, else None."""
    quote = None
    for i, c in enumerate(text):
        if quote:
            if c == quote:
                quote = None
            continue
        if c in "\"'" and i == 0:
            quote = c
        elif c == ":" and (i + 1 == len(text) or text[i + 1] == " "):
            key = text[:i].strip()
            if len(key) >= 2 and key[0] == key[-1] and key[0] in "\"'":
                key = key[1:-1]
            return key, text[i + 1:].strip()
    return None


def _scalar(text):
    if text == "":
        return None
    if text[0] in "\"'":
        if len(text) < 2 or text[-1] != text[0]:
            raise YamlError("bad quoted scalar: " + text)
        return text[1:-1]
    if text[0] == "[":
        if text[-1] != "]":
            raise YamlError("bad flow sequence: " + text)
        return [_scalar(x) for x in _split_flow(text[1:-1])]
    if text[0] == "{":
        if text[-1] != "}":
            raise YamlError("bad flow mapping: " + text)
        out = {}
        for item in _split_flow(text[1:-1]):
            kv = _split_key(item)
            if kv is None:
                raise YamlError("bad flow mapping entry: " + item)
            if kv[0] in out:
                raise YamlError("duplicate key: " + kv[0])
            out[kv[0]] = _scalar(kv[1])
        return out
    if text in ("true", "false"):
        return text == "true"
    if text in ("null", "~"):
        return None
    if re.fullmatch(r"-?[0-9]+", text):
        return int(text)
    return text


def load_yaml(text):
    lines = []
    for n, raw in enumerate(text.split("\n"), 1):
        body = raw.rstrip()
        if body.strip() in ("", "---"):
            continue
        lead = body[: len(body) - len(body.lstrip())]
        if "\t" in lead:
            raise YamlError(f"line {n}: tab in indentation")
        try:
            content = _strip_comment(body.strip())
        except YamlError as e:
            raise YamlError(f"line {n}: {e}") from None
        if content:
            lines.append([len(lead), content, n])
    if not lines:
        return None
    value, i = _block(lines, 0, lines[0][0])
    if i != len(lines):
        raise YamlError(f"line {lines[i][2]}: unexpected indentation")
    return value


def _block(lines, i, indent):
    if lines[i][1] == "-" or lines[i][1].startswith("- "):
        return _sequence(lines, i, indent)
    return _mapping(lines, i, indent)


def _sequence(lines, i, indent):
    out = []
    while i < len(lines) and lines[i][0] == indent and (lines[i][1] == "-" or lines[i][1].startswith("- ")):
        rest = lines[i][1][1:].strip()
        if rest == "":
            if i + 1 >= len(lines) or lines[i + 1][0] <= indent:
                out.append(None)
                i += 1
            else:
                value, i = _block(lines, i + 1, lines[i + 1][0])
                out.append(value)
        elif _split_key(rest) is not None and not rest.startswith(("[", "{")):
            lines[i] = [indent + 2, rest, lines[i][2]]
            value, i = _mapping(lines, i, indent + 2)
            out.append(value)
        else:
            out.append(_scalar(rest))
            i += 1
    return out, i


def _mapping(lines, i, indent):
    out = {}
    while i < len(lines) and lines[i][0] == indent:
        n = lines[i][2]
        kv = _split_key(lines[i][1])
        if kv is None:
            raise YamlError(f"line {n}: expected a key")
        key, rest = kv
        if key in out:
            raise YamlError(f"line {n}: duplicate key {key}")
        i += 1
        if rest == "":
            if i < len(lines) and lines[i][0] > indent:
                out[key], i = _block(lines, i, lines[i][0])
            elif i < len(lines) and lines[i][0] == indent and lines[i][1].startswith("- "):
                out[key], i = _sequence(lines, i, indent)
            else:
                out[key] = None
        else:
            out[key] = _scalar(rest)
    if i < len(lines) and lines[i][0] > indent:
        raise YamlError(f"line {lines[i][2]}: unexpected indentation")
    return out, i


# --- Bracket balance for JavaScript and PowerShell data files --------------------

def balanced(text, line_comment, block_open=None, block_close=None):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack, i, quote = [], 0, None
    while i < len(text):
        c = text[i]
        if quote:
            if c == "\\" and quote != "'":
                i += 2
                continue
            if c == quote:
                quote = None
        elif text.startswith(line_comment, i):
            j = text.find("\n", i)
            i = len(text) if j < 0 else j
            continue
        elif block_open and text.startswith(block_open, i):
            j = text.find(block_close, i + len(block_open))
            if j < 0:
                return "unterminated block comment"
            i = j + len(block_close)
            continue
        elif c in "\"'`":
            quote = c
        elif c in "([{":
            stack.append(c)
        elif c in ")]}":
            if not stack or stack.pop() != pairs[c]:
                return f"unbalanced {c!r} at offset {i}"
        i += 1
    if quote:
        return "unterminated string"
    if stack:
        return f"unclosed {stack[-1]!r}"
    return None


# --- Checks --------------------------------------------------------------------

class Report:
    def __init__(self):
        self.errors = []

    def err(self, file, msg):
        self.errors.append(f"{file}: {msg}")


SPDX = re.compile(r"SPDX-License-Identifier: \S+")


def check_spdx(r, path):
    head = "\n".join(path.read_text(encoding="utf-8").split("\n")[:3])
    if not SPDX.search(head):
        r.err(path.name, "no SPDX-License-Identifier line in the first three lines (COD-014)")


def get(d, *keys):
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return d


def check_golangci(r, name, data):
    if data.get("version") != "2":
        r.err(name, 'version must be the string "2" (COD-401)')
    if get(data, "linters", "default") != "standard":
        r.err(name, "linters.default must be standard (COD-401)")
    enabled = set(get(data, "linters", "enable") or [])
    for linter in ("nolintlint", "gosec", "errorlint", "revive", "bodyclose", "contextcheck"):
        if linter not in enabled:
            r.err(name, f"linter {linter} is not enabled (COD-401)")
    for key in ("require-explanation", "require-specific"):
        if get(data, "linters", "settings", "nolintlint", key) is not True:
            r.err(name, f"nolintlint {key} must be true (COD-010)")
    formatters = set(get(data, "formatters", "enable") or [])
    for f in ("gofmt", "goimports"):
        if f not in formatters:
            r.err(name, f"formatter {f} is not enabled (COD-401)")


def check_yamllint(r, name, data):
    if get(data, "rules", "truthy", "allowed-values") != ["true", "false"]:
        r.err(name, "truthy must allow only true and false (COD-850)")
    if get(data, "rules", "key-duplicates") in ("disable", None) and data.get("extends") != "default":
        r.err(name, "key-duplicates must be on (COD-850)")
    if get(data, "rules", "key-duplicates") == "disable":
        r.err(name, "key-duplicates must be on (COD-850)")


def check_hadolint(r, name, data):
    if data.get("failure-threshold") not in ("warning", "info", "style"):
        r.err(name, "failure-threshold must be warning or stricter (COD-750)")
    errors = set(get(data, "override", "error") or [])
    if "DL3002" not in errors:
        r.err(name, "DL3002, a root last USER, must be an error (COD-751)")


def check_zizmor(r, name, data):
    if get(data, "rules", "unpinned-uses", "config", "policies", "*") != "hash-pin":
        r.err(name, 'unpinned-uses must set the policy "*": hash-pin (COD-803)')


PINNED = re.compile(r"^[^@\s]+@[0-9a-f]{40}$")


def check_workflow(r, name, data):
    if data.get("permissions") not in ({}, {"contents": "read"}):
        r.err(name, "top-level permissions must be {} or contents: read (COD-800)")
    for job_name, job in (data.get("jobs") or {}).items():
        if "timeout-minutes" not in job:
            r.err(name, f"job {job_name} sets no timeout-minutes (COD-805)")
        for step in job.get("steps") or []:
            uses = step.get("uses")
            if uses and not uses.startswith("./") and not PINNED.match(uses):
                r.err(name, f"action {uses} is not pinned to a full commit hash (SEC-031)")
            if uses and uses.startswith("actions/checkout@"):
                if get(step, "with", "persist-credentials") not in (False, "false"):
                    r.err(name, f"checkout in job {job_name} must set persist-credentials: false (COD-801)")
            run = step.get("run") or ""
            if "${{" in run and "github.event." in run:
                r.err(name, f"job {job_name} expands github.event in run (COD-801)")


def check_editorconfig(r, path):
    text = path.read_text(encoding="utf-8")
    parser = configparser.ConfigParser(interpolation=None, comment_prefixes=("#", ";"))
    try:
        parser.read_string("[__root__]\n" + text)
    except configparser.Error as e:
        r.err(path.name, f"does not parse: {e}")
        return
    if parser.get("__root__", "root", fallback="") != "true":
        r.err(path.name, "root = true must come first (COD-015)")
    want = {"charset": "utf-8", "end_of_line": "lf", "insert_final_newline": "true",
            "trim_trailing_whitespace": "true"}
    if not parser.has_section("*"):
        r.err(path.name, "no [*] section (COD-015)")
        return
    for key, value in want.items():
        if parser.get("*", key, fallback="") != value:
            r.err(path.name, f"[*] must set {key} = {value} (COD-015)")


def check_enforcer(r, path):
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        r.err(path.name, f"does not parse as XML: {e}")
        return
    ns = {"m": "http://maven.apache.org/POM/4.0.0"}
    if root.findtext("m:artifactId", namespaces=ns) != "maven-enforcer-plugin":
        r.err(path.name, "not the maven-enforcer-plugin (COD-108)")
    if not re.fullmatch(r"[0-9]+(\.[0-9]+)*", root.findtext("m:version", default="", namespaces=ns)):
        r.err(path.name, "the plugin version must be pinned (COD-108)")
    rules = root.find(".//m:configuration/m:rules", ns)
    names = {child.tag.split("}")[-1] for child in (rules if rules is not None else [])}
    for rule in ("requireMavenVersion", "requireJavaVersion", "requirePluginVersions",
                 "dependencyConvergence", "banDynamicVersions"):
        if rule not in names:
            r.err(path.name, f"enforcer rule {rule} is missing (COD-108)")


def check_eslint(r, path):
    text = path.read_text(encoding="utf-8")
    problem = balanced(text, "//", "/*", "*/")
    if problem:
        r.err(path.name, f"does not parse: {problem}")
    if "export default" not in text or "eslintrc" in text:
        r.err(path.name, "must be a flat configuration with a default export (COD-603)")
    if "strictTypeChecked" not in text:
        r.err(path.name, "must use the strictTypeChecked set of typescript-eslint (COD-603)")
    if not re.search(r"eslint-comments/require-description\"\s*:\s*\"error\"", text):
        r.err(path.name, "eslint-comments/require-description must be an error (COD-010)")


def check_psd1(r, path):
    text = path.read_text(encoding="utf-8")
    problem = balanced(text, "#", "<#", "#>")
    if problem:
        r.err(path.name, f"does not parse: {problem}")
    if not text.lstrip("﻿").split("\n", 3)[-1].lstrip().startswith("@{") and "@{" not in text:
        r.err(path.name, "must hold one hashtable (COD-551)")

    def enabled(rule):
        m = re.search(rule + r"\s*=\s*@\{(.*?)\}", text, re.S)
        return bool(m and re.search(r"Enable\s*=\s*\$true", m.group(1)))

    for rule in ("PSPlaceOpenBrace", "PSPlaceCloseBrace", "PSUseConsistentIndentation",
                 "PSUseConsistentWhitespace", "PSUseCompatibleSyntax"):
        if not enabled(rule):
            r.err(path.name, f"{rule} must be on (COD-551)")
    m = re.search(r"TargetVersions\s*=\s*@\(([^)]*)\)", text)
    if not m or "'5.1'" not in m.group(1):
        r.err(path.name, "PSUseCompatibleSyntax must target 5.1 (COD-550)")


YAML_CHECKS = {
    ".golangci.yml": check_golangci,
    ".yamllint.yaml": check_yamllint,
    ".hadolint.yaml": check_hadolint,
    "zizmor.yml": check_zizmor,
    "workflow-lint.yml": check_workflow,
}


def main(argv):
    root = Path(argv[1] if len(argv) > 1 else ".")
    ex = root / "examples"
    r = Report()
    expected = list(YAML_CHECKS) + [".editorconfig", "maven-enforcer.xml", "eslint.config.mjs",
                                    "PSScriptAnalyzerSettings.psd1"]
    for name in expected:
        if not (ex / name).is_file():
            r.err(name, "missing")
    for path in sorted(p for p in ex.iterdir() if p.is_file()):
        if path.suffix != ".json":
            check_spdx(r, path)
        if path.suffix in (".yml", ".yaml"):
            try:
                data = load_yaml(path.read_text(encoding="utf-8"))
            except YamlError as e:
                r.err(path.name, f"does not parse as YAML: {e}")
                continue
            if path.name in YAML_CHECKS:
                YAML_CHECKS[path.name](r, path.name, data if isinstance(data, dict) else {})
        elif path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except ValueError as e:
                r.err(path.name, f"does not parse as JSON: {e}")
        elif path.suffix == ".toml":
            try:
                tomllib.loads(path.read_text(encoding="utf-8"))
            except tomllib.TOMLDecodeError as e:
                r.err(path.name, f"does not parse as TOML: {e}")
    if (ex / ".editorconfig").is_file():
        check_editorconfig(r, ex / ".editorconfig")
    if (ex / "maven-enforcer.xml").is_file():
        check_enforcer(r, ex / "maven-enforcer.xml")
    if (ex / "eslint.config.mjs").is_file():
        check_eslint(r, ex / "eslint.config.mjs")
    if (ex / "PSScriptAnalyzerSettings.psd1").is_file():
        check_psd1(r, ex / "PSScriptAnalyzerSettings.psd1")
    for e in r.errors:
        print("error: " + e)
    if not r.errors:
        print("ok: every example parses and meets its rules")
    return 1 if r.errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
