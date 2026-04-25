#!/usr/bin/env python3
"""Small CLI wrapper for the local background-computer-use API."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


MANIFEST = Path(os.environ.get("TMPDIR", "/tmp")) / "background-computer-use" / "runtime-manifest.json"


def load_base_url() -> str:
    if not MANIFEST.exists():
        raise SystemExit(
            f"Runtime manifest not found at {MANIFEST}. Start /Users/suns/Developer/background-computer-use/script/start.sh first."
        )
    try:
        data = json.loads(MANIFEST.read_text())
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Runtime manifest is not valid JSON: {exc}") from exc
    base_url = data.get("baseURL")
    if not isinstance(base_url, str) or not base_url.startswith("http"):
        raise SystemExit("Runtime manifest does not contain a usable baseURL.")
    return base_url.rstrip("/")


def request(method: str, path: str, payload: dict[str, Any] | None = None) -> Any:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        f"{load_base_url()}{path}",
        data=body,
        method=method,
        headers={"content-type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            text = response.read().decode("utf-8")
    except urllib.error.URLError as exc:
        raise SystemExit(f"background-computer-use request failed: {exc}") from exc
    return json.loads(text) if text else None


def print_json(value: Any) -> None:
    print(json.dumps(value, indent=2, sort_keys=True))


def main() -> int:
    parser = argparse.ArgumentParser(description="Call background-computer-use routes.")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("bootstrap")
    sub.add_parser("routes")
    sub.add_parser("list-apps")

    list_windows = sub.add_parser("list-windows")
    list_windows.add_argument("--app", required=True)

    state = sub.add_parser("state")
    state.add_argument("--window", required=True)
    state.add_argument("--image-mode", default="path", choices=["path", "base64", "omit"])
    state.add_argument("--max-nodes", type=int, default=6500)

    click = sub.add_parser("click")
    click.add_argument("--window", required=True)
    click.add_argument("--element-index", type=int)
    click.add_argument("--x", type=float)
    click.add_argument("--y", type=float)
    click.add_argument("--click-count", type=int, default=1)
    click.add_argument("--image-mode", default="path", choices=["path", "base64", "omit"])

    type_text = sub.add_parser("type-text")
    type_text.add_argument("--window", required=True)
    type_text.add_argument("--element-index", type=int)
    type_text.add_argument("--text", required=True)
    type_text.add_argument("--image-mode", default="path", choices=["path", "base64", "omit"])

    press_key = sub.add_parser("press-key")
    press_key.add_argument("--window", required=True)
    press_key.add_argument("--key", required=True)
    press_key.add_argument("--image-mode", default="path", choices=["path", "base64", "omit"])

    args = parser.parse_args()

    if args.command == "bootstrap":
        print_json(request("GET", "/v1/bootstrap"))
    elif args.command == "routes":
        print_json(request("GET", "/v1/routes"))
    elif args.command == "list-apps":
        print_json(request("POST", "/v1/list_apps", {}))
    elif args.command == "list-windows":
        print_json(request("POST", "/v1/list_windows", {"app": args.app}))
    elif args.command == "state":
        print_json(request("POST", "/v1/get_window_state", {"window": args.window, "imageMode": args.image_mode, "maxNodes": args.max_nodes}))
    elif args.command == "click":
        payload: dict[str, Any] = {"window": args.window, "clickCount": args.click_count, "imageMode": args.image_mode}
        if args.element_index is not None:
            payload["elementIndex"] = args.element_index
        elif args.x is not None and args.y is not None:
            payload["x"] = args.x
            payload["y"] = args.y
        else:
            raise SystemExit("click requires --element-index or both --x and --y")
        print_json(request("POST", "/v1/click", payload))
    elif args.command == "type-text":
        payload = {"window": args.window, "text": args.text, "focusAssistMode": "focus_and_caret_end", "imageMode": args.image_mode}
        if args.element_index is not None:
            payload["elementIndex"] = args.element_index
        print_json(request("POST", "/v1/type_text", payload))
    elif args.command == "press-key":
        print_json(request("POST", "/v1/press_key", {"window": args.window, "key": args.key, "imageMode": args.image_mode}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
