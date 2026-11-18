#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Tests examples/check-examples.py: the repository passes, and each broken copy fails
# for the reason that its case names. Each case copies examples/, breaks one rule with
# a short Python script, and expects the check to report that rule.
set -uo pipefail
here=$(cd "$(dirname "$0")/.." && pwd)
check="$here/examples/check-examples.py"
fail=0
tmp=$(mktemp -d)
trap 'rm -rf "$tmp"' EXIT

if ! python3 -I "$check" "$here"; then
  echo "FAIL: the repository itself does not pass"
  fail=1
fi

# case_fails NAME EXPECTED-REGEX PYTHON: the script runs in a copy of the repository.
case_fails() {
  local name=$1 want=$2 script=$3 dir="$tmp/$1" out
  mkdir -p "$dir"
  cp -r "$here/examples" "$dir/"
  (cd "$dir/examples" && python3 -I -c "
def rd(p): return open(p, encoding='utf-8').read()
def wr(p, s): open(p, 'w', encoding='utf-8').write(s)
def sub(p, a, b):
    s = rd(p)
    assert a in s, (p, a)
    wr(p, s.replace(a, b, 1))
$script") || {
    echo "FAIL: case $name: the setup script failed"
    fail=1
    return
  }
  if out=$(python3 -I "$check" "$dir" 2>&1); then
    echo "FAIL: case $name passed but should fail"
    fail=1
  elif ! grep -qE -- "$want" <<<"$out"; then
    echo "FAIL: case $name failed for another reason:"
    echo "$out" | head -5
    fail=1
  else
    echo "ok: case $name fails"
  fi
}

case_fails golangci-version-1 'version must be the string "2" \(COD-401\)' \
  'sub(".golangci.yml", "version: \"2\"", "version: \"1\"")'
case_fails nolint-without-reason 'nolintlint require-explanation must be true \(COD-010\)' \
  'sub(".golangci.yml", "require-explanation: true", "require-explanation: false")'
case_fails gosec-missing 'linter gosec is not enabled \(COD-401\)' \
  'sub(".golangci.yml", "    - gosec\n", "")'
case_fails yaml-duplicate-key 'does not parse as YAML: line [0-9]+: duplicate key linters' \
  'wr(".golangci.yml", rd(".golangci.yml") + "linters:\n  default: none\n")'
case_fails yaml-tab-indent 'does not parse as YAML: line [0-9]+: tab in indentation' \
  'sub(".hadolint.yaml", "  error:", "\terror:")'
case_fails truthy-yes 'truthy must allow only true and false \(COD-850\)' \
  'sub(".yamllint.yaml", "allowed-values: [\"true\", \"false\"]", "allowed-values: [\"true\", \"false\", \"yes\"]")'
case_fails hadolint-root-user 'DL3002, a root last USER, must be an error \(COD-751\)' \
  'sub(".hadolint.yaml", "    - DL3002 # the last USER is not root\n", "")'
case_fails zizmor-ref-pin 'unpinned-uses must set the policy "\*": hash-pin \(COD-803\)' \
  'sub("zizmor.yml", "hash-pin", "ref-pin")'
case_fails action-by-tag 'action actions/checkout@v7 is not pinned to a full commit hash \(SEC-031\)' \
  'sub("workflow-lint.yml", "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1", "actions/checkout@v7")'
case_fails write-all-permissions 'top-level permissions must be \{\} or contents: read \(COD-800\)' \
  'sub("workflow-lint.yml", "permissions: {}", "permissions: write-all")'
case_fails no-timeout 'job zizmor sets no timeout-minutes \(COD-805\)' \
  's = rd("workflow-lint.yml"); i = s.index("  zizmor:"); wr("workflow-lint.yml", s[:i] + s[i:].replace("    timeout-minutes: 10\n", "", 1))'
case_fails persisted-credentials 'must set persist-credentials: false \(COD-801\)' \
  'sub("workflow-lint.yml", "persist-credentials: false", "persist-credentials: true")'
case_fails editorconfig-no-root 'root = true must come first \(COD-015\)' \
  'sub(".editorconfig", "root = true\n", "")'
case_fails editorconfig-crlf '\[\*\] must set end_of_line = lf \(COD-015\)' \
  'sub(".editorconfig", "end_of_line = lf", "end_of_line = crlf")'
case_fails enforcer-without-ranges-ban 'enforcer rule banDynamicVersions is missing \(COD-108\)' \
  'sub("maven-enforcer.xml", "          <banDynamicVersions/>\n", "")'
case_fails enforcer-release-17 'requireProperty must fix maven.compiler.release to 21 \(COD-100\)' \
  'sub("maven-enforcer.xml", "<regex>21</regex>", "<regex>17</regex>")'
case_fails enforcer-broken-xml 'does not parse as XML' \
  'sub("maven-enforcer.xml", "</plugin>", "</plugn>")'
case_fails eslint-no-description 'eslint-comments/require-description must be an error \(COD-010\)' \
  'sub("eslint.config.mjs", "\"@eslint-community/eslint-comments/require-description\": \"error\"", "\"@eslint-community/eslint-comments/require-description\": \"off\"")'
case_fails eslint-unbalanced 'eslint.config.mjs: does not parse' \
  'sub("eslint.config.mjs", "  prettier,\n]);", "  prettier,\n);")'
case_fails psd1-compat-off 'PSUseCompatibleSyntax must be on \(COD-551\)' \
  's = rd("PSScriptAnalyzerSettings.psd1"); i = s.index("PSUseCompatibleSyntax"); wr("PSScriptAnalyzerSettings.psd1", s[:i] + s[i:].replace("Enable         = $true", "Enable         = $false", 1))'
case_fails psd1-unbalanced 'PSScriptAnalyzerSettings.psd1: does not parse' \
  'sub("PSScriptAnalyzerSettings.psd1", "        PSUseCorrectCasing = @{\n            Enable = $true\n        }", "        PSUseCorrectCasing = @{\n            Enable = $true\n")'
case_fails eslint-js-type-checked 'JavaScript files must turn off the type-checked rules \(COD-603\)' \
  'sub("eslint.config.mjs", "    ...tseslint.configs.disableTypeChecked,\n", "")'
case_fails shellcheck-single-brackets 'enable=require-double-brackets is missing \(COD-502\)' \
  'sub(".shellcheckrc", "enable=require-double-brackets", "enable=quote-safe-variables")'
case_fails shellcheckrc-garbage 'line [0-9]+ is not a key=value setting' \
  'wr(".shellcheckrc", rd(".shellcheckrc") + "not a setting\n")'
case_fails missing-spdx 'zizmor.yml: no SPDX-License-Identifier line in the first three lines \(COD-014\)' \
  'sub("zizmor.yml", "# SPDX-License-Identifier: Apache-2.0\n", "")'
case_fails broken-toml 'does not parse as TOML' \
  'wr("extra.toml", "# SPDX-License-Identifier: Apache-2.0\n[tool\nname = 1\n")'

[ $fail -eq 0 ] && echo "PASS: every case"
exit $fail
