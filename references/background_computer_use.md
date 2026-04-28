# Background Computer Use Reference

Use [`https://github.com/actuallyepic/background-computer-use`](https://github.com/actuallyepic/background-computer-use) for macOS background browser control. This skill does not vendor the runtime; bootstrap it into `$HOME/Developer/background-computer-use` by default with:

```bash
scripts/ensure_background_computer_use.sh
```

Set `BACKGROUND_COMPUTER_USE_DIR=/path/to/background-computer-use` to use another checkout. The runtime exposes a loopback HTTP API and writes metadata to:

```text
$TMPDIR/background-computer-use/runtime-manifest.json
```

## Startup

```bash
scripts/ensure_background_computer_use.sh
```

Then read `baseURL` from the manifest and call:

```bash
curl -s "$BASE/v1/bootstrap" | python3 -m json.tool
curl -s "$BASE/v1/routes" | python3 -m json.tool
```

Proceed only when bootstrap says instructions are ready and permissions are available.

## Core Calls

List apps:

```bash
curl -s -X POST "$BASE/v1/list_apps" -H 'content-type: application/json' -d '{}'
```

List windows:

```bash
curl -s -X POST "$BASE/v1/list_windows" -H 'content-type: application/json' -d '{"app":"Google Chrome"}'
```

Get state:

```bash
curl -s -X POST "$BASE/v1/get_window_state" -H 'content-type: application/json' -d '{"window":"WINDOW_ID","imageMode":"path","maxNodes":6500}'
```

Click by element:

```bash
curl -s -X POST "$BASE/v1/click" -H 'content-type: application/json' -d '{"window":"WINDOW_ID","target":{"kind":"display_index","value":12},"clickCount":1,"imageMode":"path"}'
```

Type text:

```bash
curl -s -X POST "$BASE/v1/type_text" -H 'content-type: application/json' -d '{"window":"WINDOW_ID","target":{"kind":"display_index","value":4},"text":"hello","focusAssistMode":"focus_and_caret_end","imageMode":"path"}'
```

Press keys:

```bash
curl -s -X POST "$BASE/v1/press_key" -H 'content-type: application/json' -d '{"window":"WINDOW_ID","key":"return","imageMode":"path"}'
```

## Browser Automation Notes

Use a read-act-read loop. After every click, type, scroll, or key press, inspect refreshed state and screenshots before proceeding. AX trees are useful for element targeting, but screenshot paths are the visual ground truth.
