---
name: synthesize
description: "use to combine N independent perspectives on a prompt into a single synthesis without forcing consensus."
---

# Synthesize

## Goal

Combine N independent perspectives on a prompt into a single synthesis without forcing consensus.

## Usage

`/at:synthesize <prompt> <perspective-1> <p-2> [p-...]`

## Instructions for the Merger

- Re-read the original prompt and flag any content in the perspectives that violates, ignores, or goes beyond what was instructed.
- Do not force consensus - unresolved disagreements are signals.
- Apply the merge rubric below point by point:

  | Pattern                            | Treatment                                                            |
  | :--------------------------------- | :------------------------------------------------------------------- |
  | Agreement (≥2 perspectives concur) | High confidence, take directly                                       |
  | Unique to one perspective          | Re-examine against source; keep if valid, discard if speculative     |
  | Contradiction                      | Assess evidence quality each side; decide on substance, do not vote  |
  | Gap (none caught)                  | Flag as a panel limitation                                           |
