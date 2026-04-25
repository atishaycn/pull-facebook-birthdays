# Pull Facebook Birthdays

Codex skill for pulling visible Facebook friend birthdays from a browser session the user is already logged into, then adding annual all-day birthday events to Google Calendar through the user's already logged-in browser.

The skill uses the local `/Users/suns/Developer/background-computer-use` runtime and avoids collecting, storing, or requesting credentials.

## Files

- `SKILL.md`: primary skill instructions.
- `agents/openai.yaml`: skill UI metadata.
- `scripts/bcu_client.py`: helper CLI for the `background-computer-use` loopback API.
- `references/background_computer_use.md`: API and workflow reference.

## Validation

```bash
python3 /Users/suns/.codex/skills/.system/skill-creator/scripts/quick_validate.py /path/to/pull-facebook-birthdays
```
