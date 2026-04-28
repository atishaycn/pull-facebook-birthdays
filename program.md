# Pull Facebook Birthdays Operating Brief

## Purpose

This repository packages a Codex skill for transferring screen-visible Facebook friend birthdays from a browser session the user is already logged into, then adding annual all-day events to Google Calendar through the same kind of browser session.

## Important Files

- `SKILL.md`: primary skill instructions and execution flow.
- `README.md`: short repository overview and validation command.
- `scripts/ensure_background_computer_use.sh`: clones, updates, starts, and verifies `https://github.com/actuallyepic/background-computer-use`.
- `scripts/bcu_client.py`: small CLI wrapper around the background-computer-use loopback API.
- `references/background_computer_use.md`: route and setup reference for the external runtime.
- `agents/openai.yaml`: skill metadata.

## Runtime Boundary

The skill depends on the external `actuallyepic/background-computer-use` repository. Do not vendor or reimplement that runtime here. Bootstrap it in `$HOME/Developer/background-computer-use` by default, or use `BACKGROUND_COMPUTER_USE_DIR` for another checkout.

The runtime writes `$TMPDIR/background-computer-use/runtime-manifest.json`; callers must read `baseURL` from that manifest instead of assuming a fixed port.

## Verification

Use the narrowest relevant check after edits:

```bash
python3 -m py_compile scripts/bcu_client.py
bash -n scripts/ensure_background_computer_use.sh
python3 /Users/sa/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/sa/Developer/pull-facebook-birthdays
```

Running the full birthday workflow additionally requires macOS Accessibility and Screen Recording permissions for the signed BackgroundComputerUse app, plus browser sessions already logged into Facebook and Google Calendar.
