---
name: pull-facebook-birthdays
description: Use when Codex needs to pull friends' birthdays from Facebook in the user's already logged-in browser and add them to Google Calendar through the user's already logged-in browser using the local background-computer-use runtime. Trigger for requests about Facebook birthdays, friend birthday extraction, birthday calendar sync, or adding Facebook friend birthdays to Google Calendar.
---

# Pull Facebook Birthdays

## Overview

Use the user's existing browser sessions to transfer Facebook friend birthdays into Google Calendar. Do not ask for, collect, or store credentials; the user must already be logged into Facebook and Google Calendar in the chosen browser.

## Required Flow

1. Ask which browser to use unless the user already specified one. Accept browser names such as Safari, Chrome, Arc, Edge, or Firefox.
2. Tell the user the chosen browser must already be logged into both Facebook and Google Calendar.
3. Start or connect to `/Users/suns/Developer/background-computer-use` and read `$TMPDIR/background-computer-use/runtime-manifest.json` for the runtime `baseURL`; never assume a fixed port.
4. Call `/v1/bootstrap` and stop if Accessibility or Screen Recording permissions are not ready.
5. Use `/v1/list_apps`, `/v1/list_windows`, and `/v1/get_window_state` with `imageMode: "path"` to target the chosen browser.
6. Navigate to Facebook's birthday surface and collect visible friend birthday records.
7. Navigate to Google Calendar and add annual all-day birthday events after checking for likely duplicates.
8. Verify a sample of created events in Google Calendar and report counts: found, skipped duplicates, created, failed or ambiguous.

## Background-Computer-Use Helper

Prefer the bundled helper for API calls:

```bash
python3 pull-facebook-birthdays/scripts/bcu_client.py bootstrap
python3 pull-facebook-birthdays/scripts/bcu_client.py list-apps
python3 pull-facebook-birthdays/scripts/bcu_client.py list-windows --app "Google Chrome"
python3 pull-facebook-birthdays/scripts/bcu_client.py state --window "WINDOW_ID" --image-mode path
```

If the runtime is not running, start it from its repo:

```bash
cd /Users/suns/Developer/background-computer-use
./script/start.sh
```

Read `references/background_computer_use.md` when route shapes, startup checks, or action payload examples are needed.

## Browser Navigation Notes

- In Chrome, prefer `https://www.facebook.com/friends/birthdays` over `https://www.facebook.com/events/birthdays/`. The events URL can render the generic Events dashboard without birthday records, while the friends birthday URL exposes sections such as `Today's birthdays`, `Recent birthdays`, and `Upcoming birthdays`.
- If Chrome address-bar typing appends instead of replacing the current URL, use Chrome's native scripting interface to set the active tab URL, then return to `background-computer-use` for screen-visible extraction:

```bash
osascript -e 'tell application "Google Chrome" to set URL of active tab of front window to "https://www.facebook.com/friends/birthdays"'
```

- Continue to treat the rendered Facebook page as the source of truth after navigation. Do not use browser scripting to read private page data or session tokens.

## Extraction Rules

- Prefer Facebook's own birthdays/events UI over private endpoints or credential/session-token scraping.
- Treat screen-visible friend names and dates as the source of truth.
- Scroll incrementally and keep a running structured list of `name`, `month`, `day`, and any visible `year` only if Facebook displays it.
- Stop extraction when repeated scrolls show no new birthday entries or the page clearly ends.
- If Facebook only exposes upcoming birthdays, sync only the visible/upcoming entries and state that limitation.
- If a name/date is ambiguous, skip it and include it in the ambiguous count rather than guessing.

## Calendar Creation Rules

- Create all-day events titled `Birthday: {Friend Name}` unless the user gave another naming rule.
- Use yearly recurrence when Google Calendar exposes it reliably; otherwise create the next occurrence only and report the limitation.
- Do not add reminders unless the user requests reminders.
- Before creating, search/check the target date for an existing event with the same friend name or equivalent birthday title.
- Skip likely duplicates rather than creating parallel events.
- For birthdays without a year, use the next upcoming occurrence for the initial date and yearly recurrence.
- Preserve privacy: do not export the birthday list to external services or files unless the user explicitly asks.

## One-Event Calendar Pilot

Use this path when the user asks for a single-birthday test before a full sync:

1. Extract exactly one visible Facebook birthday record. Example visible record shape: `Sheetal Dandge, 25 April`.
2. Open Google Calendar's event editor with a template URL. Use an all-day end date one day after the start date and include yearly recurrence:

```text
https://calendar.google.com/calendar/render?action=TEMPLATE&text=Birthday:%20{URL_ENCODED_NAME}&dates=YYYYMMDD/YYYYMMDD_PLUS_ONE&recur=RRULE:FREQ=YEARLY
```

3. Verify the editor shows:
   - title `Birthday: {Friend Name}`
   - start and end date matching the birthday day
   - `All day`
   - `Annually on {Month Day}`
4. Google Calendar may insert a default notification. Remove it before saving unless the user explicitly requested reminders. If the semantic `Remove notification` button click does not take effect, inspect the screenshot and click the visible `x` by coordinate; verify the page says `Notification removed. 0 remaining.` or the notification row is gone.
5. Save with the visible `Save` button. If the semantic click does not verify, use a coordinate click from the screenshot.
6. Verify the saved event in the calendar grid. A successful one-event pilot should show an all-day event such as `Birthday: Sheetal Dandge` on the expected date.

## Interaction Pattern

Keep user interruptions minimal. Ask only for the browser choice or for login/permission completion when blocked. Continue execution after the user confirms the browser is logged in and permissions are ready.

## Failure Handling

- If `background-computer-use` permissions are missing, report the exact missing permission and wait for the user to grant it.
- If Facebook blocks or hides birthdays, report the blocker and do not invent data.
- If Google Calendar rejects creation, inspect the page state, retry once with a simpler event creation path, then report unresolved failures with enough detail to resume.
- If navigation changes or AX state is incomplete, use screenshots as the visual ground truth.
