---
name: create-jira-ymir
description: Create a Jira card in the PACKIT project, component jotnar, based on the current conversation context. Use when the user wants to capture a task, finding, or decision as a Jira issue for the Ymir/ai-workflows project.
allowed-tools: Bash
---

# Create Jira Card for Ymir (PACKIT / jotnar)

Create a Jira issue in **project PACKIT**, **component jotnar**, based on what was discussed in the current conversation.

## Arguments

`$ARGUMENTS` may contain additional instructions or a summary hint. If empty, derive everything from conversation context.

## Workflow

### Step 1: Extract context

Analyze the current conversation to identify:
- **What** needs to be done (the task, bug, or decision)
- **Why** it matters (the motivation or triggering event)
- **Scope** — concrete deliverables or steps
- **Out of scope** — anything explicitly ruled out
- **Acceptance criteria** — how to know it's done

### Step 2: Choose issue type

Pick the most appropriate type based on context:
- **Story** — new capability, integration, or investigation (default)
- **Bug** — something is broken
- **Task** — operational or maintenance work

Do not use Spike — PACKIT has no Spike type. Use a `[SPIKE]` prefix in the summary instead when the work is exploratory.

### Step 3: Draft the card

Present the draft to the user in this format:

```
**Project:** PACKIT
**Component:** jotnar
**Type:** <Story|Bug|Task>

**Summary:** <short imperative title, under 80 chars>

**Description:**

### Context
<why this work exists — the problem, trigger, or decision>

### Scope
1. <numbered deliverables>
   - <sub-items if needed>

### Out of scope
- <bullets of what's excluded, if any>

### Acceptance criteria
- <bullets describing done state>
```

The `jira` CLI `--body` flag parses **Markdown**, not Jira wiki markup. Use standard Markdown:
- `###` for headings (not `h3.`)
- `1.` for ordered lists (not `#` — that renders as H1 headings)
- `-` for unordered lists (not `*`)
- `` `code` `` for inline code (not `{{code}}`)
- `[text](URL)` for links (not `[text|URL]`)
- `**bold**` and `*italic*`

### Step 4: Wait for approval

Ask the user to review. Do **not** create the issue until they confirm. Incorporate any requested changes first.

### Step 5: Create the issue

Create the issue **empty first (summary only, no `--body`), then attach the description in a second, separate `edit` call.** A single `create` call carrying the full multi-paragraph Markdown body is the slowest and least reliable of the `jira` CLI calls and is the one most likely to hang; splitting the work into two small calls avoids feeding a large `--body` payload into the same call that also has to create the issue, and each call individually is small and fast:

```bash
# 1. create empty (summary + type + component only)
timeout 10 jira issue create -p PACKIT --component jotnar -t <type> -s "<summary>" --no-input

# 2. fill in the body on the issue key returned above
timeout 10 jira issue edit <ISSUE-KEY> -C jotnar --body "<description>" --no-input
```

Report the resulting issue URL back to the user only after both calls have succeeded.

Always wrap every `jira` CLI call in `timeout 10` — it can hang indefinitely (observed: 100s+ with no output) even when auth is fine and `--no-input` is set. This seems environmental, not caused by body content or length, and a short timeout surfaces it fast instead of burning minutes waiting. If a call hits the timeout:
1. Do not assume it failed.
   - For the empty-create call: run `jira issue list -p PACKIT -q '"component" = jotnar'` and check whether an issue with your summary already landed before retrying — a client-side timeout can still mean the server-side create succeeded, and blindly retrying risks a duplicate.
   - For the body-edit call: re-open the issue (`jira issue view <ISSUE-KEY>` or the browser URL) and check whether the description already landed before retrying — edits are idempotent to retry (re-sending the same `--body` is harmless), so when in doubt just retry once.
2. If nothing landed, retry once more with `timeout 10`. A hang is usually transient — a trivial retry with the same short timeout typically succeeds.
3. If a retry of the *create* call produces a throwaway placeholder issue (e.g. from a diagnostic call with a dummy summary), **do not delete it** — repurpose it in place: `jira issue edit <ISSUE-KEY> -s "<real summary>" -C jotnar --body "<real description>" --no-input`. Deleting issues is not the workflow here; editing a stray placeholder into the real card is.

### Step 6: Attachments (optional)

`jira-cli` has no `attach` subcommand. If the user wants a local file (e.g. an investigation doc) attached to the issue:
- Default to asking the user to attach it manually via the Jira web UI.
- Only attempt a direct Jira REST API upload (via `curl`, using the same token/auth jira-cli uses) if the user explicitly asks for that instead — locating or using that token needs their sign-off first, since it involves reading credential material.

## Notes

- Always use `--no-input` to avoid the interactive TUI editor.
- Do not use `ORDER BY` in any JQL queries.
- If the user specifies a parent epic or linked issue, use `jira issue link` after creation.
