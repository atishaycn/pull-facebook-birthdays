# Pull Facebook Birthdays

Codex skill for pulling visible Facebook friend birthdays from a browser session the user is already logged into, then adding annual all-day birthday events to Google Calendar through the user's already logged-in browser.

The skill depends on [`actuallyepic/background-computer-use`](https://github.com/actuallyepic/background-computer-use) and avoids collecting, storing, or requesting credentials. The setup helper clones or updates that runtime in `$HOME/Developer/background-computer-use` by default, starts it, and reads the loopback URL from its runtime manifest.

## Files

- `SKILL.md`: primary skill instructions.
- `agents/openai.yaml`: skill UI metadata.
- `scripts/ensure_background_computer_use.sh`: clones/updates/starts the upstream runtime.
- `scripts/bcu_client.py`: helper CLI for the `background-computer-use` loopback API.
- `references/background_computer_use.md`: API and workflow reference.

## Setup

```bash
scripts/ensure_background_computer_use.sh
python3 scripts/bcu_client.py bootstrap
```

Set `BACKGROUND_COMPUTER_USE_DIR=/path/to/background-computer-use` to use an existing checkout somewhere other than `$HOME/Developer/background-computer-use`.

## Validation

```bash
python3 -m py_compile scripts/bcu_client.py
bash -n scripts/ensure_background_computer_use.sh
python3 /Users/sa/.codex/skills/.system/skill-creator/scripts/quick_validate.py /Users/sa/Developer/pull-facebook-birthdays
```
