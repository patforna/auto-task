# Auto-task transcripts

Each `/auto-task` run dumps its full session transcript here at the end of Step 8 (wrap-up). Kept as a corpus to mine later — patterns in subagent behaviour, common failure modes, plan→implementation drift, prompt quality, etc.

- **What:** `<NNN-slug>.<session-uuid>.md` — main-thread events (assistant text, Bash calls, subagent prompts + final responses) with each subagent's full inner trace inlined in a collapsible `<details>` block.
- **How it's generated:** `claude-replay --recurse-subagents "$CLAUDE_CODE_SESSION_ID"` — see `~/github/system/scripts/claude-replay`.
- **Why a `_` prefix:** sorts to the top and signals "infrastructure, not source"; mirrors the convention used elsewhere (e.g. `tasks/_archive/`).
- **Re-runs:** the session UUID disambiguates, so multiple transcripts for the same task coexist and `claude-replay <uuid>` round-trips back to the live JSONL.
