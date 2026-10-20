#!/usr/bin/env bash
set -euo pipefail
root=$(cd "$(dirname "$0")/.." && pwd)
output=$(mktemp -d)
trap 'rm -rf "$output"' EXIT
for site in neutral muted; do
  hugo --source "$root/examples/$site" --themesDir "$root/.." --destination "$output/$site" --quiet
  python3 "$root/tests/verify.py" "$root/examples/$site" "$output/$site" "$site"
done
mkdir -p "$output/minimal-source/content"
printf 'baseURL = "https://example.org/"\ntitle = "Minimal Site"\ntheme = "roxo-flex"\n' > "$output/minimal-source/hugo.toml"
printf '+++\ntitle = "Home"\n+++\n' > "$output/minimal-source/content/_index.md"
printf '+++\ntitle = "Contact"\nlayout = "contact"\n+++\n' > "$output/minimal-source/content/contact.md"
hugo --source "$output/minimal-source" --themesDir "$root/.." --destination "$output/minimal" --quiet
grep -q 'Minimal Site' "$output/minimal/index.html"
grep -q '©' "$output/minimal/index.html"
if grep -q '<form' "$output/minimal/contact/index.html"; then
  echo 'Minimal site rendered an unconfigured form.' >&2
  exit 1
fi
if command -v chromium >/dev/null 2>&1; then
  python3 "$root/tests/visual.py" "$output"
fi
printf 'Both examples passed.\n'
