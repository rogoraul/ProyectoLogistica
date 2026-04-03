# Communication Protocol — IA↔IA

This document defines the rules for structured communication between AI systems in this folder.

---

## Message Files

- All messages go into the `messages/` subfolder
- Naming convention: `from-<ai-name>-<NN>.md` (e.g., `from-claude-01.md`, `from-gpt-02.md`)
- `NN` is a zero-padded sequence number per AI (01, 02, 03...)
- Update `messages/INBOX.md` with a one-line pointer every time you add a message

---

## Message Format

Each message file must begin with this header:

```
---
from: <AI name and model, e.g. "Claude claude-sonnet-4-6">
date: <ISO date, e.g. 2026-04-03>
in-reply-to: <filename of the message you are responding to, or "none">
subject: <short title for this message>
status: open | acknowledged | implemented | rejected
---
```

Followed by the message body in Markdown.

---

## Message Body Guidelines

Structure your messages using these optional sections as needed:

### Analysis
Observations about the current state of the project — what works, what doesn't, what's missing.

### Proposal
A concrete proposal for improvement. Be specific:
- What to change (file, function, concept)
- Why (motivation, expected benefit)
- How (pseudocode, algorithm sketch, or description)

### Code
If proposing code changes, include them as fenced code blocks with the target file path noted above the block:

```
# File: algorithms/new_algorithm.py
<code here>
```

### Open Questions
Things you are uncertain about and want the other AI (or the human) to clarify.

### Action Items
A checklist of concrete next steps:
- [ ] Item 1
- [ ] Item 2

---

## Status Lifecycle

| Status | Meaning |
|--------|---------|
| `open` | Message sent, awaiting response |
| `acknowledged` | Other AI has read and responded |
| `implemented` | The proposal was implemented in the codebase |
| `rejected` | The proposal was decided against (with reason noted) |

Update the `status` field in the header as things progress.

---

## Rules

1. **Be concrete.** Vague ideas are less useful than rough pseudocode.
2. **Be honest about uncertainty.** If you don't know something, say so.
3. **Respect the human.** The student has final say on what gets implemented.
4. **Cite the code.** When referring to specific files or functions, name them explicitly.
5. **No unnecessary complexity.** Proposals should be proportionate to the project's scope.
6. **Sign your messages.** Always include your AI identity in the header.
