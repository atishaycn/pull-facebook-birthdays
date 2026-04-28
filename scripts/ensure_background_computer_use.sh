#!/usr/bin/env bash
set -euo pipefail

repo_url="https://github.com/actuallyepic/background-computer-use"
repo_dir="${BACKGROUND_COMPUTER_USE_DIR:-$HOME/Developer/background-computer-use}"
manifest="${TMPDIR:-/tmp}/background-computer-use/runtime-manifest.json"

if [[ ! -d "$repo_dir/.git" ]]; then
  mkdir -p "$(dirname "$repo_dir")"
  git clone "$repo_url" "$repo_dir"
fi

current_url="$(git -C "$repo_dir" remote get-url origin 2>/dev/null || true)"
if [[ "$current_url" != "$repo_url" && "$current_url" != "git@github.com:actuallyepic/background-computer-use.git" ]]; then
  echo "background-computer-use exists at $repo_dir but origin is $current_url" >&2
  echo "Expected $repo_url. Set BACKGROUND_COMPUTER_USE_DIR to another checkout or fix the remote." >&2
  exit 1
fi

current_branch="$(git -C "$repo_dir" branch --show-current 2>/dev/null || true)"
if [[ "$current_branch" == "main" ]]; then
  git -C "$repo_dir" pull --ff-only --quiet origin main
else
  echo "Using existing background-computer-use checkout on branch ${current_branch:-detached} at $repo_dir" >&2
fi

"$repo_dir/script/start.sh"

if [[ ! -f "$manifest" ]]; then
  echo "Runtime manifest was not written at $manifest" >&2
  exit 1
fi

python3 - <<'PY'
import json
import os
from pathlib import Path

manifest = Path(os.environ.get("TMPDIR", "/tmp")) / "background-computer-use" / "runtime-manifest.json"
data = json.loads(manifest.read_text())
base_url = data.get("baseURL")
if not isinstance(base_url, str) or not base_url.startswith("http"):
    raise SystemExit(f"Manifest does not contain a usable baseURL: {manifest}")
print(base_url)
PY
