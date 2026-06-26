# Auto-Task Transcripts

Transcripts are **not** stored in this repo. Each `/auto-task` run writes its full session transcript to `~/Drive/code/tad/auto-task/transcripts/` (cloud-synced backup, kept out of git to avoid diff and grep noise).

Kept for inspection, debugging and mining - patterns in subagent behaviour, common failure modes, plan→implementation drift, prompt quality, etc.

Transcripts are generated using `claude-replay` (see `~/github/system/scripts/claude-replay`).
