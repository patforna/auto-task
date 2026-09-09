---
title: Amend a Task Mid-Flight and Re-Implement
date: 2026-09-09
status: ready-for-dev
type: research
---

## Amend a Task Mid-Flight and Re-Implement

Work out how auto-task should support changing a task's intent after implementation has finished — amend the task, extend its plan, re-run implementation.

Trigger: the human reviews the finished code and concludes the implementation itself needs to change, not just be fixed.

### Acceptance Criteria

- The report says whether the current workflow supports this, naming the closest existing affordances and exactly where they block.
- It separates this case from the existing review-feedback loop: here the human changes the task, not just the code.
- It covers both entry points — inside an auto-task run once implementation is done and before ship, and later in a fresh session against a task at ready-for-signoff. It says whether an already-shipped task is in scope.
- It covers intent changes that contradict an already-implemented AC, not just additive ones, and says how a retracted or replaced AC is recorded.
- It recommends one option — new skill, extending existing skills, or a named combination of both — and says how status transitions and plan/AC deltas are handled. Design-level: enough that a follow-up task needs no further research, but no drafted skill body.
- Alternatives considered are named with a one-line reason for rejecting them.
- Ends at the report.
- Findings land as a dated research doc in the repo's research folder, listed under an existing group in its index.

### Notes

- Run the research as a panel plus synthesis, like the existing proposal docs. Internal design analysis — reach for external prior art only where it would change the recommendation.
