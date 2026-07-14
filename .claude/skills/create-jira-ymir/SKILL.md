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

```bash
jira issue create -p PACKIT --component jotnar -t <type> -s "<summary>" --body "<description>" --no-input
```

Report the resulting issue URL back to the user.

## Notes

- Always use `--no-input` to avoid the interactive TUI editor.
- Do not use `ORDER BY` in any JQL queries.
- If the user specifies a parent epic or linked issue, use `jira issue link` after creation.
